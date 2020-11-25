from flask import Flask, render_template, redirect, url_for, request
import requests
import json

app = Flask(__name__)

access_token = ""

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/oauth')
def oauth():

    access_token = token()

    url = "https://kapi.kakao.com/v1/user/signup"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        'Authorization': "Bearer " + str(access_token)
    }
    response = requests.request("POST",url,headers=headers)

    url = "https://kapi.kakao.com/v1/user/me"
    profile_request = requests.get(url, headers={'Authorization' : f"Bearer {access_token}"},
            )

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    response = requests.post(url, headers=headers, data=make_message("hello"))

    if response.status_code == 200:
        return ('메시지를 성공적으로 보냈습니다.')
    else:
        return('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()) + str(type(post)))

def token():
    code = str(request.args.get('code'))
    url = "https://kauth.kakao.com/oauth/token"
    payload = "grant_type=authorization_code&client_id=43e3daf58dd14d049001ebdbd6538f58&redirect_uri=http://127.0.0.1:5000/oauth&code=" + str(code)
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    access_token = json.loads(((response.text).encode('utf-8')))['access_token']

    return access_token


def make_message(text):
    temp = {
        "object_type": "text",
        "text": "hello",
        "link": {
            "web_url": "https://developers.kakao.com",
        },
        "button_title": "바로 확인",
    }

    return {"template_object":json.dumps(temp)}

@app.route('/logout')
def logout():
    
    url = "https://kapi.kakao.com/v1/user/logout"
    headers = {
        "Authorization": "Bearer " + access_token
    }
    response = requests.post(url, headers=headers)
    return response.json()

@app.route('/unlink')
def unlink():
    
    url = "https://kapi.kakao.com/v1/user/unlink"
    headers = {
        "Authorization": "Bearer " + access_token
    }
    response = requests.post(url, headers=headers)
    return response.json()

@app.route('/message')
def message():
    
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {
        "Authorization": "Bearer " + access_token
    }
    data = {
        "template_object": json.dumps({"object_type": "text",
                                       "text": "Hello, world!",
                                       "link": {
                                           "web_url": "www.naver.com"
                                       },
                                       "scope" : ["talk_message", "friends"]
                                       })
    }
    response = requests.post(url, headers=headers, data=data)
    response.status_code
    if response.json().get('result_code') == 0:
        return ('메시지를 성공적으로 보냈습니다.')
    else:
        return('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()) + access_token)

@app.route('/plus')
def plus() :
    url = "https://kauth.kakao.com/oauth/authorize?client_id=43e3daf58dd14d049001ebdbd6538f58&redirect_uri=http://13.125.177.64:5000/plus&response_type=code&scope={required_scopes.join('talk_message')}"
    response = requests.get(url)
    return response.text

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    headers = {
        "Authorization": "Bearer " + str(access_token)
    }

    data = {
        "template_object": json.dumps({"object_type": "text",
                                       "text": "Hello, world!",
                                       "link": {
                                           "web_url": "www.naver.com"
                                       }
                                       })
    }

    response = requests.post(url, headers=headers, data=data)
    response.status_code
    if response.json().get('result_code') == 0:
        return ('메시지를 성공적으로 보냈습니다.')
    else:
        return('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))


def make_message(text):
    temp = {
        "object_type": "text",
        "text": "hello",
        "link": {
            "web_url": "https://developers.kakao.com",
            "mobile_web_url": "https://developers.kakao.com"
        },
        "button_title": "바로 확인",
    }

    return {"template_object":json.dumps(temp)}


host_addr = "0.0.0.0"
port_num = "5000"

if __name__ == '__main__':
    app.run(debug=True, host=host_addr, port=port_num)