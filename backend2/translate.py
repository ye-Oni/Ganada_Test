import os
import sys
import urllib.request
import json


def translate_en_to_ko(text) :
    client_id = "S5Y7q0BwlHaNCDRLH49N" 
    client_secret = "ZDpyF3ClLm"

    encText = urllib.parse.quote(text)
    data = "source=en&target=ko&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)

    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        response_body = response_body.decode("utf-8")
        body = json.loads(response_body)
        
        return body['message']['result']['translatedText']
    else:
        print("Error Code:" + rescode)
        return '401'


    #client_id : S5Y7q0BwlHaNCDRLH49N
    #cliend_secret : ZDpyF3ClLm

if __name__=='__main__':
    print(translate_en_to_ko("I am playing the piano."))