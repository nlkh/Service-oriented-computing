from flask import Flask, render_template, request, url_for, request, redirect, jsonify
import requests
import json
import facebook

app = Flask(__name__)


fb_access_token = ""
kakao_access_token = ""

@app.route('/')
def index():
    if kakao_access_token == "" :
        return render_template('superindex.html')
    else :
        return render_template('loginindex.html')

@app.route('/about1')
def about1():
    return render_template('about1.html')

@app.route('/about2')
def about2():
    return render_template('about2.html')

@app.route('/about3')
def about3():
    return render_template('about3.html')

@app.route('/oauth')
def oauth():   
    global kakao_access_token
    kakao_access_token = token()
    if kakao_access_token == None :
        return jsonify({
            'status' : 400,
            'message' : 'get access token failed'
        })
    
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
        'Authorization': "Bearer " + kakao_access_token,
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200 :
        return jsonify({
            'status' : 400,
            'message' : 'Authorization Failed'
        })
    
    return redirect("https://serviceoriented.ml:5000/")

@app.route('/friend')
def friend():
    
    result = {
        'status' : 400,
        'message' : "friend list load failed"
    }
    
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': "Bearer " + str(kakao_access_token),
    }

    url = "https://kapi.kakao.com/v1/api/talk/friends"  ##친구 목록 불러오기
    response = requests.get(url, headers=headers)

    if response.status_code != 200 :
        return jsonify({
            'status' : 400,
            'message' : 'get friend list failed'
        })
   
    return response.json()

def token():
    global kakao_access_token
    code = str(request.args.get('code'))
    url = "https://kauth.kakao.com/oauth/token"
    payload = "grant_type=authorization_code&client_id=43e3daf58dd14d049001ebdbd6538f58&redirect_uri=https://serviceoriented.ml:5000/oauth&code=" + str(code)
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    
    if response.status_code != 200 :
        return jsonify({
            'status' : 400,
            'message' : 'get access token failed'
        })
    
    kakao_access_token = str(json.loads(((response.text).encode('utf-8')))['access_token'])

    return kakao_access_token


@app.route('/kakaostory')
def kakaostory():
    global kakao_access_token
    response = requests.get("https://kapi.kakao.com/v1/api/story/mystories", 
                            headers={"Authorization":f"Bearer {kakao_access_token}"})
    return response.text

@app.route('/friend_message', methods=['POST'])
def friend_message():
    global kakao_access_token
    message = request.get_json()['message']
    globaluuids = request.get_json()['friends']
    
    if message is None :
        return jsonify({
            'status' : 400,
            'message' : 'Fill in Message Box'
        })
    
    if globaluuids is None :
        return jsonify({
            'status' : 400,
            'message' : 'Choose friends who get your message'
        })
    
    if None in globaluuids :
        globaluuids.remove(None)
        
    headers = {
        'Authorization': "Bearer " + str(kakao_access_token),
    }
    url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"  ##친구에게 메시지 보내기

    uuidsData = {'receiver_uuids': json.dumps(globaluuids)}
   
    post = {
        "object_type": "text",
        "text": message,
        "link": {
            "web_url": "https://developers.kakao.com",
        },
        "button_title": "바로 확인",
    }

    data = {'template_object': json.dumps(post)}
    uuidsData.update(data)

    response = requests.post(url, headers=headers, data=uuidsData)
   
    if response.status_code != 200 :
        return jsonify({
            'status' : 400,
            'message' : 'send failed'
        })
    
    return jsonify(response.text)

@app.route('/logout')
def logout():
    global kakao_access_token
    url = "https://kapi.kakao.com/v1/user/logout"
    headers = {
        "Authorization" : "Bearer " + kakao_access_token
    }
    response = requests.request("POST", url, headers=headers)
    kakao_access_token=""
    return redirect("https://serviceoriented.ml:5000/")

    
@app.route('/fb-login/oauth')
def fb_oauth():
    global fb_access_token
    code = str(request.args.get('code'))
    url = 'https://graph.facebook.com/v9.0/oauth/access_token?client_id=822581321822671&redirect_uri=https://serviceoriented.ml:5000/fb-login/oauth&client_secret=2b2581f4b49f0bc6b7051ea5de33051c&code=' + str(code)

    response = requests.request("GET", url)
    if response.status_code != 200 :
        return jsonify({
            'status' : 400,
            'message' : 'get access token failed'
        })
    fb_access_token = str(json.loads(response.text)['access_token'])
    return redirect("https://serviceoriented.ml:5000/")

@app.route('/fb-posts')
def load_posts() :
    try :
        graph = facebook.GraphAPI(access_token=fb_access_token, version="3.1")
        post = graph.get_object(id='me', fields='posts')
        post = post['posts']['data']
        postList = []
        
    except :
        return jsonify({
            'status' : 400,
            'message' : 'load post failed'
        })
    
    for i in post :
        if 'message' in i :
            postList.append(i['message'])

    return jsonify(postList)


host_addr = "0.0.0.0"
port_num = "5000"

if __name__ == '__main__':
    app.run(host=host_addr, port=port_num, ssl_context=('./cert/server.crt', './cert/server.key'))