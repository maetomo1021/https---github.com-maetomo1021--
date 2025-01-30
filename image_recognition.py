import os
import cv2
import datetime
import pytesseract
from pdf2image import convert_from_path
import re

# Tesseract OCRの実行ファイルのパスを設定
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windowsの場合

# データを収集するフォルダを指定
input_folder = 'path_to_your_folder'  # 画像ファイルが保存されているフォルダのパスを指定

# データを保存するリスト
data_list = []

# PDFファイルを画像に変換する関数
def pdf_to_images(pdf_path):
    return convert_from_path(pdf_path)

# 画像からテキストを抽出する関数
def extract_text_from_image(image):
    text = pytesseract.image_to_string(image, lang='eng')
    return text

# テキストから数値データを抽出する関数
def extract_data_from_text(text):
    data = {}
    patterns = {
        '筋肉量': r'筋肉量\s*:\s*([\d.]+)',
        '年月日': r'年月日\s*:\s*([\d/]+)',
        '体重': r'体重\s*:\s*([\d.]+)',
        '脂肪量': r'脂肪量\s*:\s*([\d.]+)',
        '水分量%': r'水分量%\s*:\s*([\d.]+)',
        '体脂肪率': r'体脂肪率\s*:\s*([\d.]+)',
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            data[key] = match.group(1)
    return data

# フォルダ内のファイルを処理
for filename in os.listdir(input_folder):
    file_path = os.path.join(input_folder, filename)
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        image = cv2.imread(file_path)
        text = extract_text_from_image(image)
        data = extract_data_from_text(text)
        data_list.append(data)
    elif filename.lower().endswith('.pdf'):
        images = pdf_to_images(file_path)
        for image in images:
            text = extract_text_from_image(image)
            data = extract_data_from_text(text)
            data_list.append(data)

# 収集したデータを表示
for data in data_list:
    print(data)
