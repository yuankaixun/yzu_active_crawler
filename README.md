YZU Active Crawler

這是一個用於自動抓取元智大學 Portal 系統活動的 Python 爬蟲工具。它可以幫助你快速篩選出「有提供餐點」並且「大學部學生」符合報名資格的活動。

🚀 主要功能

自動化登入：透過 Selenium 自動填寫帳號密碼，無縫登入元智大學 Portal 系統。

效能優化：登入後將瀏覽器的 Cookie 轉移至 requests Session，並全域關閉 SSL 驗證，大幅加快後續頁面的解析速度，並在登入後關閉瀏覽器以釋放記憶體。

智慧資格檢查：自動進入各活動頁面檢查報名資格，若資格不包含「大學部學生」則會自動略過。

精準供餐辨識：

掃描活動說明內容，尋找「供餐」、「餐盒」、「便當」、「餐卷」、「午餐」等關鍵字。

進一步深入線上報名表單，檢查是否含有實質的餐點選項（例如：葷食選項）。

🛠️ 安裝與環境設定

確保 Python 環境：請確認您的電腦已安裝 Python 3.x。

安裝依賴套件：
請在終端機執行以下指令來安裝所需套件：

pip install selenium beautifulsoup4 requests python-dotenv urllib3


準備瀏覽器驅動：本專案預設使用 Chrome 瀏覽器，請確保已安裝 Google Chrome。Selenium 會嘗試自動處理 ChromeDriver。

設定環境變數：
在專案的根目錄下建立一個名為 .env 的檔案（可以參考專案中的 .env.expale），並填入您的元智大學 Portal 帳號與密碼：

YZU_ID="你的帳號"
YZU_Password="你的密碼"


⚠️ 注意：專案中的 .gitignore 已設定排除 .env，請絕對不要將包含真實密碼的 .env 檔案 push 到公開的 GitHub 儲存庫。

🏃 執行方式

在終端機或命令提示字元中執行主程式：

python selenium-input.py


程式啟動流程：

會短暫自動彈出 Chrome 瀏覽器進行登入操作。

登入完成獲取 Cookie 後，瀏覽器會自動關閉。

程式會在背景快速掃描，最後在終端機印出目前所有符合條件（大學部學生可報名且有供餐）的活動名稱清單。

📂 檔案結構簡介

selenium-input.py: 爬蟲主要執行腳本。

.env.expale: 環境變數範例檔，用於提示設定欄位。

.gitignore: Git 忽略清單，保護本地敏感資訊。
