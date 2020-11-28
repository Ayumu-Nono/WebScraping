import newspaper

import pandas as pd

# URL = 'https://news.yahoo.co.jp'
URL = "https://news.yahoo.co.jp/search?p=black+lives+matter&ei=utf-8"
website = newspaper.build(URL, memoize_articles=False, MAX_SUMMARY=300)

df_list: list = []
for article in website.articles:
    temp_list: list = [article.title, article.url]
    print(article.url)
    print(article.title)
    df_list.append(temp_list)

df: pd.DataFrame = pd.DataFrame(df_list, columns=["title", "url"])
print(df)
df.to_csv("playground2.csv")

for item in range(len(website.articles)):
    website_article = website.articles[item]
    website_article_url = website_article.url
    try:
        website_article.download()
        website_article.parse()
        website_article.nlp()
        print("記事[" + str(item) + "]: " + website_article_url + " : " + website_article.summary + "\n")
    except ValueError:
        print("記事[" + str(item) + "]: " + website_article_url + " : " + "取得エラー" + "\n")
    continue
