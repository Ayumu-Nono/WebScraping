import requests
from bs4 import BeautifulSoup
 
r = requests.get("https://news.livedoor.com/")
 
soup = BeautifulSoup(r.content, "html.parser")
 
# ニュース一覧を抽出
print(soup.find("a"))