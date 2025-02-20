from bs4 import BeautifulSoup
import requests

url = "https://www.jcb.co.jp/voucher/gift-card/merchant.html"
response = requests.get(url)

# 文字化けを防ぐためにエンコーディングを明示的に指定
response.encoding = response.apparent_encoding  # 自動検出されたエンコーディングを適用

# BeautifulSoupで解析
print("全部のDOM取得")
soup = BeautifulSoup(response.text,"html.parser")
# print(response.text)

print("飲食店のチェーン店名を取得")
# 全ての <td> 要素を取得
td_elements = soup.find_all("td")
print("確認用")
print(td_elements)

# テキストだけを取得して表示
for i, td in enumerate(td_elements, 1):
    if (148 <=i and i<= 172):
        print(f"{i}: {td.text.strip()}")
    
