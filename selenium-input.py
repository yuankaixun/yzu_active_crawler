import os
import time
import bs4
import requests
import urllib3
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 關閉 requests/urllib3 的 SSL 警告訊息
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 設定 .env
load_dotenv()    

# 設定 driver
driver = webdriver.Chrome()
driver.get("https://portalx.yzu.edu.tw/PortalSocialVB/Login.aspx")
wait = WebDriverWait(driver, 10)

# --- 階段一：Selenium 自動化登入 ---
userIDInput = driver.find_element(By.ID, "Txt_UserID")
userPasswordInput = driver.find_element(By.ID, "Txt_Password")
singInButtom = driver.find_element(By.ID, "ibnSubmit")

user_ID = os.getenv("YZU_ID")
user_pw = os.getenv("YZU_Password")

userIDInput.send_keys(user_ID)
userPasswordInput.send_keys(user_pw)
time.sleep(0.5)
singInButtom.click()
time.sleep(1)

# --- 階段二：建立 requests Session、繞過 SSL 並轉移 Cookie ---
session = requests.Session()

# 💡 關鍵設定：全域關閉 SSL 憑證驗證
session.verify = False

session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

for cookie in driver.get_cookies():
    session.cookies.set(cookie['name'], cookie['value'])

# 關閉瀏覽器釋放記憶體
driver.quit()


# --- 階段三：定義改用 requests 的 dig_in 函式 ---
def dig_in(url, session):
    try:
        resp = session.get(url)
        resp.encoding = 'utf-8' # 避免中文亂碼
        root = bs4.BeautifulSoup(resp.text, "html.parser")
        
        qualification_data = root.find("td", string="報名資格")
        if qualification_data:
            qualification_text = qualification_data.parent.text
            if "大學部學生" not in qualification_text:
                return False

        body = root.find("td", class_="TDBody")
        if body:
            body_text = body.get_text()
            target_keywords = ["供餐", "餐盒", "便當", "餐卷", "午餐"]
            if any(keyword in body_text for keyword in target_keywords):
                return True

        page_title = root.find("a", string="線上報名")
        if page_title and "href" in page_title.attrs:
            raw_page_url = page_title["href"]
            page_url = raw_page_url.replace("..", "https://portalx.yzu.edu.tw/PortalSocialVB")
            
            final_resp = session.get(page_url)
            final_resp.encoding = 'utf-8'
            final_root = bs4.BeautifulSoup(final_resp.text, "html.parser")

            meal_option = final_root.find("input", id="rdoMeatYes")
            if meal_option:
                return True

        return False
    except Exception as e:
        print(f"抓取失敗 ({url}): {e}")
        return False


# --- 階段四：抓取活動列表 ---
actURL = "https://portalx.yzu.edu.tw/PortalSocialVB/FMain/PageActivityAll.aspx"
data = session.get(actURL)
data.encoding = 'utf-8'

root = bs4.BeautifulSoup(data.text, "html.parser")

raw_titles_body = root.find("tr", class_="hi_line")
if raw_titles_body and raw_titles_body.parent:
    new_titles = raw_titles_body.parent
    print("目前有供餐的活動為：")

    for title in new_titles:
        if hasattr(title, 'a') and title.a and "href" in title.a.attrs:
            raw_href = title.a["href"]
            full_url = raw_href.replace("..", "https://portalx.yzu.edu.tw/PortalSocialVB")
            
            if dig_in(full_url, session):
                print(f"- {title.a.text.strip()}")