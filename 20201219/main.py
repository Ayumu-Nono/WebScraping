import math
from time import sleep, time
from typing import List, Optional, Tuple
from tqdm import tqdm
import itertools

from bs4 import BeautifulSoup
from selenium import webdriver

import pandas as pd


class CommentGather:
    def __init__(self) -> None:
        df1 = pd.read_csv("sheet1.csv")
        df2 = pd.read_csv("sheet2.csv")
        df3 = pd.read_csv("sheet3.csv")
        self.df_list: List[pd.DataFrame] = [df1, df2, df3]
        self.driver: webdriver.Chrome = webdriver.Chrome("chromedriver")

    def sequence(self) -> None:
        file_num: int = 1
        for df in self.df_list:
            for i in tqdm(range(len(df))):
                self.__each_article(
                    landing_url=df.loc[i, "url"],
                    file_num=file_num
                )
                file_num += 1

    def __each_article(
        self,
        landing_url: str,
        file_num: int
    ) -> None:
        page_num: int = 1
        comment_list: list = []
        comment_num: Optional[int] = None
        # まずはコメント数を取ってくる
        comment_url = landing_url + "/comments"
        comment_num, temp_list = self.__get_comment_list(url=comment_url)
        if comment_num is None or comment_num == "":
            comment_list = []
        else:
            max_page: int = math.ceil(int(comment_num) / 10)
            for page_num in range(max_page):
                comment_url = landing_url + "/comments?page={0}&t=t&order=recommended".format(page_num)
                comment_num, temp_list = self.__get_comment_list(url=comment_url)
                sleep(2)
                for item in temp_list:
                    comment_list.append(item)
        new_df = pd.DataFrame(comment_list, columns=["comment"])
        new_df["info"] = ""
        new_df.loc[0, "info"] = "url: {0}".format(comment_url)
        new_df.loc[1, "info"] = "comment num: {0}".format(comment_num)
        new_df.to_csv("comments/comment_sheet{0}.csv".format(file_num))

    def __get_comment_list(
        self,
        url: str,
    ) -> Tuple[int, List[str]]:
        self.driver.get(url)
        iframe = self.driver.find_element_by_class_name("news-comment-plguin-iframe")
        self.driver.switch_to.frame(iframe)
        comment_boxes = self.driver.find_elements_by_class_name("root")
        try:
            num_text = self.driver.find_element_by_class_name("num").text.strip()
            comment_num = num_text[5:]
        except ValueError:
            pass
        comment_list: List[str] = []
        for comment_box in comment_boxes:
            elem_comment = comment_box.find_element_by_class_name("cmtBody")
            comment = elem_comment.text.strip()
            comment_list.append(comment)
        return comment_num, comment_list


if __name__ == "__main__":
    cg = CommentGather()
    cg.sequence()