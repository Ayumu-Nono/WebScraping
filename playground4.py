from typing import List
from urllib.parse import urlunsplit
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
# Webページを取得して解析する

load_url = "https://news.yahoo.co.jp/search?p=black+lives+matter&ei=utf-8"
html = requests.get(load_url)
soup = BeautifulSoup(html.content, "html.parser")

items: List[BeautifulSoup] = soup.find_all("li", class_="newsFeed_item-ranking")
print(type(items[0]))
item = items[0]
tug_a = item.find("a", class_="newsFeed_item_link")
tug_time = item.find("time")
# tug_title = item.find("div", class_="newsFeed_item_title")
url = tug_a.get("href")
date = tug_time.text
# title = tug_time.text
# print("Found {0} items.".format(len(items)))

# 記事詳細に入る
driver = webdriver.Chrome("chromedriver")
driver.get(url)

load_url = url
html = requests.get(load_url)
soup = BeautifulSoup(html.content, "html.parser")

article = soup.find("article")
# print(article)
tug_title = article.find("h1")
text = article.text
comment_info = soup.find_all("li", class_="num")
print(tug_title)
# print(text)
print(comment_info)

# コメント抽出
load_url = url + "/comments"
html = requests.get(load_url)
soup = BeautifulSoup(html.content, "html.parser")
# print(soup.find_all("li"))