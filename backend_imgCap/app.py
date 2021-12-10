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

app = Flask(__name__)
static_dir='images/'

@app.route('/test-api', methods=['GET','POST'])
def testHome():
    r = request.method
    if(r=="GET"):
        K.clear_session()
        captions=gc.generate_captions('./test.jpg')
        cap={"captions":captions}
        K.clear_session()
        return cap
    elif(r=='POST'):
        K.clear_session()
        file = request.files['file']
        name = 'test_' + file.filename
        file.save(secure_filename(name))
        captions=gc.generate_captions(name)
        translated = translate.translate_en_to_ko(captions)
        
        # return {"captions":captions, "message" : translated}
        return {"message" : translated}
    else:
        return jsonify({
        "captions":"Refresh again !"
        })  


def func(filename):
    captions = gc.generate_captions(filename)        
    translated = translate.translate_en_to_ko(captions)

    return {"captions":captions, "message" : translated}

if __name__ == '__main__':
    app.run(debug=True,host='localhost',port=5000)
    # print(func('./test2.jpg'))