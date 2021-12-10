import concurrent
import os
from PIL import Image
import io
from flask import Flask,Blueprint,request,render_template,jsonify,Response,send_file
import jsonpickle
import numpy as np
import json
import base64
import translate
from keras import backend as K

from werkzeug.utils import secure_filename
import generate_caption as gc
import save_mobileNetV2 as classification

import time

app = Flask(__name__)
static_dir='images/'

@app.route('/gallery-caption', methods=['GET','POST'])
def testHome():
    r = request.method
    if(r=="GET"):
        K.clear_session()
        captions=gc.generate_captions('./test2.jpg')
        cap={"captions":captions}
        K.clear_session()
        return cap


    elif(r=='POST'):
        # api 요청 시 받은 파일
        file = request.files['file']
        name = 'test_' + file.filename

        # api 요청 시 받은 파일은 서버에 임시 파일로 저장되기 때문에 다시 한 번 파일로 저장하고 사용을 하는 것이 좋음 -> 서버에 저장하는 코드 (file.save)
        file.save(secure_filename(name))

        # image classification - 이미지 분류 모델을 실행하고 결과를 papago api로 한글로 변환하는 함수
        kind = make_kind(name)

        # image captioning - 이미지 캡셔닝 모델을 실행하고 결과를 papago api로 한글로 변환하는 함수
        translated = make_caption(name)
    
        return {"kind":kind, "message" : translated}
    else:
        return jsonify({"captions":"Refresh again !"})


def make_kind(filename):

    K.clear_session() # 세션 초기화
    kind = classification.image_classification(filename) # 이미지 분류 모델
    kind = translate.translate_en_to_ko(kind) # "dog" -> "개"
    # K.clear_session()
    return kind # "개" 리턴


def make_caption(filename):

    K.clear_session() # 세션 초기화
    captions = gc.generate_captions(filename) # 이미지 캡셔닝 모델
    translated = translate.translate_en_to_ko(captions) # "dogs are running" -> "개들이 뛰고 있다."
    # K.clear_session()
    return translated # "개들이 뛰고 있다." 리턴

if __name__ == '__main__':
    app.run(debug=True,host='localhost',port=5000)
    # print(func('./test2.jpg'))