# from selenium import webdriver
# import chromedriver_binary
# driver = webdriver.Chrome()

from selenium import webdriver
import time
from selenium.webdriver.support.select import Select
import pandas as pd
import os
# from bs4 import BeautifulSoup

driver = webdriver.Chrome("chromedriver")
url = "https://utas.adm.u-tokyo.ac.jp/campusweb/campusportal.do"

driver.get(url)

# ログイン
selector = ".ui-corner-all:nth-child(1)"
element = driver.find_element_by_css_selector(selector)
element.click()

# Username
selector = "#userNameInput"
element = driver.find_element_by_css_selector(selector)
username = os.environ["utas_username"]
element.send_keys(username)

# Password
selector = "#passwordInput"
element = driver.find_element_by_css_selector(selector)
password = os.environ["utas_password"]
element.send_keys(password)

# ログイン
selector = "#submitButton"
element = driver.find_element_by_css_selector(selector)
element.click()

# シラバス
selector = "#tab-sy"
element = driver.find_element_by_css_selector(selector)
element.click()

driver.implicitly_wait(10)

# iFrame切り替え
selector = "#main-frame-if"
iframe = driver.find_element_by_css_selector(selector)
driver.switch_to.frame(iframe)

# 学部選択
selector = "#gakubuShozokuCode"
select = Select(driver.find_element_by_css_selector(selector))
select.select_by_index(11) # ここ変える

time.sleep(1)

driver.implicitly_wait(10)

# 検索
selector = ".ui-button.ui-widget.ui-state-default.ui-corner-all:nth-child(1)"
element = driver.find_element_by_css_selector(selector)
element.click()

driver.implicitly_wait(30)

# 画面遷移まで待機
selector = ".ui-button.ui-widget.ui-state-default.ui-corner-all:nth-child(1)"
driver.find_element_by_css_selector(selector)

course_num = 51 # ここも
courses = [{}] * course_num

for i in range(int(course_num / 100 + 1)):
    try:
        # continuous = True
        # tbody = driver.find_element_by_tag_name("tbody")
        # elements = tbody.find_elements_by_tag_name("tr")
        # while continuous:
        tbody = driver.find_element_by_tag_name("tbody")
        elements = tbody.find_elements_by_tag_name("tr")
        # if tds[0].text == str(i*100+1):
        #     continuous = False
        for j in range(0, 100):
            courses[i * 100 + j] = {}
            tds = elements[j].find_elements_by_tag_name("td")
            # 開講区分
            courses[i * 100 + j]["semesterOffered"] = tds[1].text
            # 曜限
            courses[i * 100 + j]["dayPeriod"] = tds[2].text
            # 学部
            courses[i * 100 + j]["graduate"] = tds[3].text
            # 所属
            courses[i * 100 + j]["affiliation"] = tds[4].text
            # 教室
            courses[i * 100 + j]["classroom"] = tds[5].text
            # 持ち出し
            courses[i * 100 + j]["isSpecialized"] = tds[6].text
            # 時間割コード
            courses[i * 100 + j]["code"] = tds[7].text
            # 科目大区分
            courses[i * 100 + j]["bigGroup"] = tds[8].text
            # 科目中区分
            courses[i * 100 + j]["midGroup"] = tds[9].text
            # 授業名
            courses[i * 100 + j]["name"] = tds[10].text
            # 教員
            courses[i * 100 + j]["instructor"] = tds[11].text

            if i == int(course_num / 100) and j == (course_num % 100 - 1):
                break
        if i != int(course_num / 100):
            body = driver.find_element_by_tag_name("body")
            elements = driver.find_elements_by_tag_name("a")
            elements[-1].click()
    except:
        import traceback
        traceback.print_exc()

print("----------------")
print(courses)

df = pd.json_normalize(courses)
df.to_csv("pharmaceuticalSciences.csv") # ここ変える

# driver.execute_script("refer('2020','00','30011','ja_JP');")

# driver.implicitly_wait(10)
#
# driver.switch_to.window(driver.window_handles[1])
# selector = ".syllabus-break-word"
# element = driver.find_element_by_css_selector(selector)
# syllabus_break_word = element.text
# print(syllabus_break_word)

driver.switch_to.window(driver.window_handles[0])

time.sleep(10)

driver.close()

driver.quit()