import urllib.request as req
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv
import time
import bs4

#設定.env
load_dotenv()    

#設定driver
driver = webdriver.Chrome()
driver.get("https://portalx.yzu.edu.tw/PortalSocialVB/Login.aspx")
wait = WebDriverWait(driver, 10)


def dig_in(url):
    driver.get(url)
    page_data = driver.page_source
    root = bs4.BeautifulSoup(page_data, "html.parser")
    qualification_data=root.find("td", string="報名資格")
    if qualification_data:
        
        qualification_text=qualification_data.parent.text
        if "大學部學生" not in qualification_text:
            return False
    body=root.find("td", class_="TDBody")
    
    if body:
        
        body_text=body.get_text()
        target_keywords=["供餐", "餐盒", "便當", "餐卷", "午餐"]

        if any(keyword in body_text for keyword in target_keywords):
            return True
    

    page_title = root.find("a", string="線上報名")
    
    # 💡 加上防呆判斷：確保 page_title 存在，且裡面有 <a> 標籤與 href 屬性
    if page_title and "href" in page_title.attrs:
        raw_page_url = page_title["href"]
        page_url = raw_page_url.replace(
            "..", "https://portalx.yzu.edu.tw/PortalSocialVB"
        )
        
            # 進入報名頁面
        driver.get(page_url)
        final_page_data = driver.page_source
        final_root = bs4.BeautifulSoup(final_page_data, "html.parser")

        
        meal_option = final_root.find("input", id="rdoMeatYes")
        if meal_option:
            return True
            

    # 如果沒有找到 <a> 標籤或沒有連結，直接回傳 False 跳過
    return False
    


driver.refresh() 
time.sleep(1)
#登入操作
userIDInput=driver.find_element(By.ID, "Txt_UserID")
userPasswordInput=driver.find_element(By.ID, "Txt_Password")
singInButtom=driver.find_element(By.ID, "ibnSubmit")
user_ID = os.getenv("YZU_ID")
user_pw = os.getenv("YZU_Password")
userIDInput.send_keys(user_ID)
userPasswordInput.send_keys(user_pw)


time.sleep(0.5)
singInButtom.click()
time.sleep(1)

activeButtom=wait.until(EC.element_to_be_clickable((By.ID, "tdP4")))
time.sleep(0.5)
activeButtom.click()
time.sleep(1)


data=driver.page_source

root=bs4.BeautifulSoup(data, "html.parser")
raw_titles_body=root.find("tr", class_="hi_line")
new_titles=raw_titles_body.parent
print("目前有供餐的活動為")

for title in new_titles:
    if title("a"):
        raw_href = title.a["href"]
        full_url = raw_href.replace("..", "https://portalx.yzu.edu.tw/PortalSocialVB")
        if dig_in(full_url):
            print(title.a.text)

driver.close()
    
    


