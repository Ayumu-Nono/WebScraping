import urllib.request
from bs4 import BeautifulSoup

def get_yahoo_news():
    # ヘッドラインニュースのタイトル格納用リスト
    news_data = []

    # urlの指定
    url = 'http://www.yahoo.co.jp/'

    # ユーザーエージェントを指定
    ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) '\
     'AppleWebKit/537.36 (KHTML, like Gecko) '\
     'Gecko/20100101 Firefox/60.0 '

    req = urllib.request.Request(url, headers={'User-Agent': ua})

    #htmlの取得
    html = urllib.request.urlopen(req)

    # htmlパース
    soup = BeautifulSoup(html, "html.parser")
    topicsindex = soup.find('div', attrs={'class': 'topicsindex'})

    # class「topicsindex」内から記事タイトルを抽出
    for li in topicsindex.find_all('li'):
        a = li.find('a')
        # 記事タイトルとURLを保存
        news_data.append([a.contents[0], a.get('href')])
        
    return news_data

def main():
    # Yahooトップのトピック記事タイトルを取得
    news_data = get_yahoo_news()

    # 取得データの表示
    print(news_data)

if __name__ == '__main__':
    main()