from selenium import webdriver

# バージョン: 87.0.4280.88（Official Build） （64 ビット）
#　ChromeDriverのパスを引数に指定しChromeを起動
driver = webdriver.Chrome("chromedriver")
driver.get("https://news.yahoo.co.jp/search?p=black+lives+matter&ei=utf-8")

element = driver.find_element_by_link_text("もっと見る")

element.click()