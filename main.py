from typing import List, Optional, Tuple
import re
import time
from pandas.core.frame import DataFrame
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

import pandas as pd


class ArticleAtom:
    def __init__(self, url: str) -> None:
        self.url: str = url
        self.title: str = ""
        self.text: str = ""
        self.date: str = ""
        self.comment_url: str = ""
        self.comment_num: Optional[int] = None
        self.comment_list: List[str] = []


class WebScraper:
    def __init__(self, platform: str, url: str) -> None:
        if platform != "Yahoo":
            raise KeyError("検索フォーム {0} には対応していません".format(platform))
        self.item_list: list = []
        self.atom_list: List[ArticleAtom] = []
        self.landing_url: str = url
        self.driver: webdriver.Chrome = webdriver.Chrome("chromedriver")

    def __get_soup(self, url: str) -> BeautifulSoup:
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        return soup

    def sequence(self):
        self.driver.get(self.landing_url)
        # self.__button_click(url=self.landing_url, button_text="もっと見る")
        html = self.driver.page_source
        soup = BeautifulSoup(html, "lxml")
        tug_ol = soup.find("ol", class_="newsFeed_list")
        self.__set_item_list(soup=tug_ol)
        for item in self.item_list:
            self.__sequence_particle(item=item)
            self.__output()

    def __sequence_particle(self, item):
        atom = self.__make_article_atom(item)
        atom.comment_num, atom.comment_list = self.__get_comment_list(
            url=atom.comment_url
        )
        self.__print_atom_info(atom=atom)
        self.atom_list.append(atom)
        self.__sleep(t=1)

    def __sleep(self, t: int) -> None:
        time.sleep(t)

    def __print_atom_info(self, atom: ArticleAtom) -> None:
        print("url: ", atom.url)
        print("title: ", atom.title)
        print("date: ", atom.date)
        print("text: ", atom.text)
        print("comment_url: ", atom.comment_url)
        print("comment_num: ", atom.comment_num)
        print("comment_list: ", atom.comment_list)

    def __set_item_list(self, soup: BeautifulSoup) -> None:
        # viewableWrap newsFeed_item newsFeed_item-normal newsFeed_item-ranking 
        self.item_list = soup.find_all("li", class_="newsFeed_item-ranking")

    def __make_article_atom(
        self,
        item,
    ) -> ArticleAtom:
        tug_a = item.find("a", class_="newsFeed_item_link")
        tug_time = item.find("time")
        url = tug_a.get("href")
        date = tug_time.text
        atom = ArticleAtom(url=url)
        atom.date = date
        # go detail page
        soup = self.__get_soup(url=url)
        article = soup.find("article")
        atom.title = article.find("h1").text
        atom.text = article.text
        # 詳細ページに入る
        self.driver.get(atom.url)
        atom.comment_url = self.driver.current_url + "/comments"
        return atom

    def __get_comment_list(
        self,
        url: str,
    ) -> Tuple[int, List[str]]:
        self.driver.get(url)
        iframe = self.driver.find_element_by_class_name("news-comment-plguin-iframe")
        self.driver.switch_to.frame(iframe)
        comment_boxes = self.driver.find_elements_by_class_name("root")
        num_text = self.driver.find_element_by_class_name("num").text.strip()
        comment_num = num_text[5:]
        comment_list: List[str] = []
        for comment_box in comment_boxes:
            elem_comment = comment_box.find_element_by_class_name("cmtBody")
            comment = elem_comment.text.strip()
            comment_list.append(comment)
        return comment_num, comment_list

    def __button_click(self, url: str, button_text: str):
        self.driver.get(url)
        buttons = self.driver.find_elements_by_tag_name("button")
        for button in buttons:
            if button.text == button_text:
                button.click()
                break

    def __output(self) -> None:
        df_list: list = []
        # 文字列へ変換
        for atom in self.atom_list:
            row: list = [
                atom.url,
                atom.title,
                atom.text,
                atom.date,
                atom.comment_num,
                atom.comment_list
            ]
            df_list.append(row)
        df: pd.DataFrame = DataFrame(df_list, columns=["url", "title", "text", "date", "comment num", "comment list"])
        df.to_csv("result.csv")


if __name__ == "__main__":
    load_url = "https://news.yahoo.co.jp/search?p=black+lives+matter&ei=utf-8"
    ws = WebScraper(platform="Yahoo", url=load_url)
    ws.sequence()
    ws.driver.close()