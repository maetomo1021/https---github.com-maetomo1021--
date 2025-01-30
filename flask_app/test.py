from PIL import Image
import pytesseract
import cv2
import os

# Tesseractの実行可能ファイルのパスを指定
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# ファイルパス
file_path = r'C:\syuuzyokuprezentation\flask_app\example_image.png'

# ファイル存在確認
if not os.path.exists(file_path):
    raise FileNotFoundError(f"指定されたファイルが見つかりません: {file_path}")

# 画像の読み込み
img = cv2.imread(file_path)

# 読み込み失敗時のエラー処理
if img is None:
    raise ValueError(f"画像の読み込みに失敗しました: {file_path}")

# グレースケール化
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# OCRの実行
extracted_text = pytesseract.image_to_string(gray, lang='jpn')

# 結果表示
print("抽出されたテキスト:")
print(extracted_text)
