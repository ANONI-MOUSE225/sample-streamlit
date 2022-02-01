import streamlit as st
import io

import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

st.title('顔認識アプリ')

subscription_key ='SUBSCRIPTION_KEY'
assert subscription_key
face_api_url = 'ENDPOINT/face/v1.0/detect'

uploaded_file = st.file_uploader("choose an image...", type='jpeg')

if uploaded_file is not None:
  img = Image.open(uploaded_file)

  with io.BytesIO() as output:
    img.save(output, format="JPEG")
    binary_img = output.getvalue()#バイナリ取得
  # ヘッダ設定
  headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key}
  # パラメーターの設定
  params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
  }

  # POSTリクエスト
  res = requests.post(face_api_url, params=params,headers=headers, data=binary_img)
  results = res.json()

  for result in results:
    def get_text_rectangle():
      left = (rect['left'] + (rect['left'] + rect['width'])) / 2
      top = rect['top'] -20
      return (left, top)
      
    rect =result['faceRectangle']
    txpos = get_text_rectangle()
    age = str(result['faceAttributes']['age'])
    textsize = 14
    font = ImageFont.truetype("/Library/Fonts/Arial Bold.ttf", size=textsize)
    textcolor = (255, 255, 255)

    draw = ImageDraw.Draw(img)
    draw.rectangle([(rect['left'],rect['top']),(rect['left']+rect['width'], rect['top']+rect['height'])], fill=None, outline='green', width=3)
    draw.text(txpos, age, font=font, fill=textcolor)
  st.image(img, caption='Uploaded Image.', use_column_width=True)
