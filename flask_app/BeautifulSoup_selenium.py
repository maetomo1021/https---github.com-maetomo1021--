from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Chromeのオプション設定
options = Options()
options.add_argument("--headless")  # ヘッドレスモード（画面なし）
options.add_argument("--disable-gpu")  # GPU無効化（安定性向上）
options.add_argument("--no-sandbox")  # サンドボックス無効化（Linux向け）
options.add_argument("--disable-dev-shm-usage")  # メモリ使用最適化

url = "https://www.jcb.co.jp/voucher/gift-card/merchant.html"

# Chrome WebDriver のパス
driver = webdriver.Chrome(options=options)

# JCBのページを開く
driver.get(url)
# time.sleep(5)
soup  = BeautifulSoup(driver.page_source,"html.parser")

td_data = soup.find_all("td")
with open ("restaurant.text", "w",encoding="utf-8")as file:
    for i ,td in enumerate(td_data,1):
        shop_name = td.text.strip()
        file.write(f"{i}:{shop_name}\n")
        print(f"{i}:{shop_name}\n")
print("データを保存しました！")

driver.quit()