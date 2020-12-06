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
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }

    url = "https://kapi.kakao.com/v1/user/signup"
    headers.update({'Authorization': "Bearer " + str(access_token)})
    response = requests.request("POST", url, headers=headers)

    url = "https://kapi.kakao.com/v1/user/me"
    profile_request = requests.get(url, headers={'Authorization': f"Bearer {access_token}"},
                                   )

    url = "https://kauth.kakao.com/oauth/authorize?client_id=43e3daf58dd14d049001ebdbd6538f58&redirect_uri=http://127.0.0.1:5000/oauth&response_type=code&scope=talk_message"

    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': "Bearer " + str(access_token),
    }

    response = requests.get(url, headers=headers)

    url = "https://kapi.kakao.com/v1/api/talk/friends"  ##친구 목록 불러오기
    response = requests.get(url, headers=headers)

    return response.json()


def token():
    code = str(request.args.get('code'))
    url = "https://kauth.kakao.com/oauth/token"
    payload = "grant_type=authorization_code&client_id=43e3daf58dd14d049001ebdbd6538f58&redirect_uri=http://127.0.0.1:5000/oauth&code=" + str(
        code)
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    access_token = json.loads(((response.text).encode('utf-8')))['access_token']

    return access_token


@app.route('/kakaostory')
def kakaostory():
    access_token = token()
    print(access_token)

    # 게시물 쓰기
    url = "https://kapi.kakao.com/v1/api/story/post/note"
    payload = 'content=POSTING_TEST'  # <-내용
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        "Authorization": f"Bearer {access_token}"
    }
    requests.request("POST", url, data=payload, headers=headers)

    requests.get("https://kapi.kakao.com/v1/api/story/profile",
                 headers={"Authorization": f"Bearer {access_token}"}, )
    # id값 스토리 받기
    response = requests.get("https://kapi.kakao.com/v1/api/story/mystory?id=_CCc7Q8.hCxTbltQ9uA",
                            headers={"Authorization": f"Bearer {access_token}"}, )
    return (response.text)
@app.route('/friend_message')
def friend_message():
    access_token = token()
    print(access_token)
    headers = {
        'Authorization': "Bearer " + str(access_token),
    }
    url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"  ##친구에게 메시지 보내기

    uuidsData = {'receiver_uuids': '["iLmOvIi7jbiNoZivn6uarJigjLmJuYy4geA"]'}

    post = {
        "object_type": "text",
        "text": "hello",
        "link": {
            "web_url": "https://developers.kakao.com",
        },
        "button_title": "바로 확인",
    }

    data = {'template_object': json.dumps(post)}
    uuidsData.update(data)

    response = requests.post(url, headers=headers, data=uuidsData)

    if response.status_code == 200:
        return "sucess"
    else:
        print(response.status_code)
        return response.text


@app.route('/logout')
def logout():
    url = "https://kapi.kakao.com/v1/user/logout"
    headers = {
        "Authorization": "Bearer " + str(token())
    }
    response = requests.post(url, headers=headers)
    return response.json()


host_addr = "0.0.0.0"
port_num = "5000"

if __name__ == '__main__':
    app.run(debug=True, host=host_addr, port=port_num)