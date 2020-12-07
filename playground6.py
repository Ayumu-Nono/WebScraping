from typing import List, Optional
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


driver = webdriver.Chrome("chromedriver")
url = "https://qiita.com/Scstechr/items/5583acdbf258616ea941"
driver.get(url)
html = driver.page_source.encode('utf-8')
soup = BeautifulSoup(html, "lxml")
items = soup.find_all("h1")
print(items)