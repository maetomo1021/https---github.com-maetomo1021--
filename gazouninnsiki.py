import os
import cv2
import datetime
import pytesseract
from pdf2image import convert_from_path
import re
# Haar Cascadeの顔検出用XMLファイルのパス
haarcascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'

# Haar Cascadeの顔検出モデルを読み込む
face_cascade = cv2.CascadeClassifier(haarcascade_path)

# カメラを起動
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    # フレームをキャプチャ
    ret, frame = cap.read()
    
    if not ret:
        print("Error: Could not read frame.")
        break

    # グレースケールに変換
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 顔を検出
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # 検出された顔に矩形を描画
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # フレームを表示
    cv2.imshow('Face Detection', frame)

    # 'q'キーを押すとループを終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# カメラとウィンドウをリリース
cap.release()
cv2.destroyAllWindows()
