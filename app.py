from flask import Flask, render_template
app = Flask(__name__)

@app.route('/fb-login')
def hello():
    return 'hello'


@app.route('/fb-login')
def index():
    return render_template('fblogin.html')
'''
@app.route('/facebook-login')
def facebook_login():
    return 


@app.route('/facebook-posts')
def facebook_posts():
    return str(fbposts.load_posts())
'''
host_addr = "0.0.0.0"
port_num = "5000"

if __name__ == '__main__':
    app.run(host=host_addr, port=port_num)
