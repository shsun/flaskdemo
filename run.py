import os

from flask import Flask
from flask import render_template, redirect, url_for
from flask import request

from app import create_app

app = Flask(__name__)

'''
@app.route('/', methods=['GET'])
def init():
    error = None
    return render_template('login.html', error=error)


@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] == 'admin':
        target_url = redirect(url_for('home', username=request.form['username']))
    else:
        error = 'invalid username/password'
        target_url = render_template('login.html', error=error)
    return target_url


@app.route('/home', methods=['POST', 'GET'])
def home():
    return render_template('home.html', username=request.args.get('username'))
'''

config_name = os.getenv('FLASK_CONFIG')
config_name = 'testing'
app = create_app(config_name)


if __name__ == '__main__':
    app.debug = True
    app.run('127.0.0.1', 5000, True)
