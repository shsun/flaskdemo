from flask import Flask
from flask import render_template, redirect, url_for
from flask import request

app = Flask(__name__)

@app.route('/', methods=['GET'])
@app.route('/login', methods=['POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin':
            return redirect(url_for('home', username=request.form['username']))
        else:
            error = 'invalid username/password'
    return render_template('login.html', error=error)


@app.route('/home', methods=['POST', 'GET'])
def home():
    return render_template('home.html', username=request.args.get('username'))


if __name__ == '__main__':
    app.debug = True
    app.run()
