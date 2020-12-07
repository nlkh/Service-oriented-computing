from flask import Flask, render_template, request
import requests
import fbposts
import json
import facebook

app = Flask(__name__)


fb_access_token = ""

@app.route('/fb-login')
def fb_login():
    return render_template('fbtest.html')

    
@app.route('/fb-login/oauth')
def oauth():
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
