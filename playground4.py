import requests
import urllib
from bs4 import BeautifulSoup

keyword = "black lives matter"
url = 'https://news.yahoo.co.jp/search'

params = {'hl':'ja', 'gl':'JP', 'ceid':'JP:ja', 'q':keyword}
article_no = 1

# url、パラメータを設定してリクエストを送る
res = requests.get(url, params=params)
# レスポンスをBeautifulSoupで解析する
soup = BeautifulSoup(res.content, "html.parser")

# レスポンスからh3階層のニュースを抽出する（classにxrnccdを含むタグ）
h3_blocks = soup.select(".newsFeed_list")
print(h3_blocks)
for i, h3_entry in enumerate(h3_blocks):

    # 記事を10件だけ処理する
    if article_no == 11:
        break
    
    with open('playground4.txt', mode='a') as f:
        # ニュースのタイトルを抽出する（h3タグ配下のaタグの内容）
        h3_title = h3_entry.select_one("h3 a").text
        # ニュースのリンクを抽出する（h3タグ配下のaタグのhref属性）
        h3_link = h3_entry.select_one("h3 a")["href"]
        # 抽出したURLを整形して絶対パスを作る
        h3_link = urllib.parse.urljoin(url, h3_link)

        # ニュースのタイトル、リンクをファイルに書き込む
        f.write(h3_title)
        f.write('\r\n')
        f.write(h3_link)
        f.write('\r\n')

        article_no = article_no + 1

        # h3階層のニュースからh4階層のニュースを抽出する
        h4_block = h3_entry.select_one(".SbNwzf")

        if h4_block != None:
            # h4階層が存在するときのみニュースを抽出する
            h4_articles = h4_block.select("article")

            for j, h4_entry in enumerate(h4_articles):
                h4_title = h4_entry.select_one("h4 a").text
                h4_link = h4_entry.select_one("h4 a")["href"]
                h4_link = urllib.parse.urljoin(url, h4_link)

                f.write(h4_title)
                f.write('\r\n')
                f.write(h4_link)
                f.write('\r\n')

                article_no = article_no + 1
