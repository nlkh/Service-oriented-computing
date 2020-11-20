from flask import Flask, render_template, redirect, url_for, request
import requests
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')
@app.route('/oauth')
def oauth():
    code = str(request.args.get('code'))
    url = "https://kauth.kakao.com/oauth/token"
    payload = "grant_type=authorization_code&client_id=43e3daf58dd14d049001ebdbd6538f58&redirect_uri=http://13.125.177.64:5000/oauth&code="+str(code)
    headers = {
               'Content-Type': "application/x-www-form-urlencoded",
               'Cache-Control': "no-cache",
               }
    response = requests.request("POST",url,data=payload,headers=headers)
    access_token = json.loads(((response.text).encode('utf-8')))['access_token']

    url = "https://kapi.kakao.com/v1/user/signup"
    headers.update({'Authorization' : "Bearer " + str(access_token)})
    response = requests.request("POST",url,headers=headers)

    url = "https://kapi.kakao.com/v1/user/me"
    profile_request = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization" : f"Bearer {access_token}"},
            )
    profile_json = profile_request.json()
    kakao_account = profile_json.get("kakao_account")
    email = kakao_account.get("email", None)
    kakao_id = profile_json.get("id")

    return (profile_request.text)

host_addr = "0.0.0.0"
port_num = "5000"

if __name__ == '__main__':
    app.run(debug=True, host=host_addr, port=port_num)
