from flask import Flask, render_template, request, url_for, request
import requests
import json
import facebook

app = Flask(__name__)


fb_access_token = ""
kakao_access_token = ""

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/oauth')
def oauth():
    global kakao_access_token
    kakao_access_token = token()
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }

    url = "https://kapi.kakao.com/v1/user/signup"
    headers.update({'Authorization': "Bearer " + str(kakao_access_token)})
    response = requests.request("POST", url, headers=headers)

    url = "https://kapi.kakao.com/v1/user/me"
    profile_request = requests.get(url, headers={'Authorization': f"Bearer {kakao_access_token}"},
                                   )

    url = "https://kauth.kakao.com/oauth/authorize?client_id=43e3daf58dd14d049001ebdbd6538f58&redirect_uri=https://serviceoriented.ml:5000/oauth&response_type=code&scope=talk_message"

    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': "Bearer " + str(kakao_access_token),
    }

    response = requests.get(url, headers=headers)

    url = "https://kapi.kakao.com/v1/api/talk/friends"  ##친구 목록 불러오기
    response = requests.get(url, headers=headers)

    return response.json()


def token():
    global kakao_access_token
    code = str(request.args.get('code'))
    url = "https://kauth.kakao.com/oauth/token"
    payload = "grant_type=authorization_code&client_id=43e3daf58dd14d049001ebdbd6538f58&redirect_uri=https://serviceoriented.ml:5000/oauth&code=" + str(
        code)
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    kakao_access_token = json.loads(((response.text).encode('utf-8')))['access_token']

    return kakao_access_token


@app.route('/kakaostory')
def kakaostory():
    global kakao_access_token
    #access_token = token()
    print(kakao_access_token)

    # 게시물 쓰기
    url = "https://kapi.kakao.com/v1/api/story/post/note"
    payload = 'content=POSTING_TEST'  # <-내용
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        "Authorization": f"Bearer {kakao_access_token}"
    }
    requests.request("POST", url, data=payload, headers=headers)

    requests.get("https://kapi.kakao.com/v1/api/story/profile",
                 headers={"Authorization": f"Bearer {kakao_access_token}"}, )
    # id값 스토리 받기
    response = requests.get("https://kapi.kakao.com/v1/api/story/mystory?id=_CCc7Q8.hCxTbltQ9uA",
                            headers={"Authorization": f"Bearer {kakao_access_token}"}, )
    return (response.text)

@app.route('/friend_message')
def friend_message():
    global kakao_access_token
    print(kakao_access_token)
    headers = {
        'Authorization': "Bearer " + str(kakao_access_token),
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

@app.route('/fb-login')
def fb_login():
    return render_template('fbtest.html')

    
@app.route('/fb-login/oauth')
def fb_oauth():
    global fb_access_token
    code = str(request.args.get('code'))
    url = 'https://graph.facebook.com/v9.0/oauth/access_token?client_id=1226404121075869&redirect_uri=https://serviceoriented.ml:5000/fb-login/oauth&client_secret=ae1b40de9370d3ef5290ae4cb9f4191b&code=' + str(code)

    response = requests.request("GET", url)
    fb_access_token = str(json.loads(response.text)['access_token'])
    return response.text

@app.route('/fb-posts')
def load_posts() :
    graph = facebook.GraphAPI(access_token=fb_access_token, version="3.1")
    post = graph.get_object(id='me', fields='posts')
    return str(post['posts']['data'])



host_addr = "0.0.0.0"
port_num = "5000"

if __name__ == '__main__':
    app.run(host=host_addr, port=port_num, ssl_context=('./cert/server.crt', './cert/server.key'))
