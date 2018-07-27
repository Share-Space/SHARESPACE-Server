from flask import Flask, render_template, redirect, request, flash, session, abort, url_for
import os
app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else: # if logged in
        return render_template('index.html', username=session.get('username'))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form.get('username')
        session['email'] = request.form.get('email')
        session['logged_in'] = True
        return redirect(url_for('home'))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return home()

@app.errorhandler(404)
def page_not_found(e): # error handler for 404
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.secret_key = os.urandom(12) # generate random key
    app.run(debug = True, host='0.0.0.0', port=5000)
