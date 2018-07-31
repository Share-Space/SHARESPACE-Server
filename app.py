from flask import (
    Flask, 
    render_template, 
    redirect, 
    request, 
    session, 
    url_for, 
    send_from_directory
)
from main import main as main_blueprint
from main import random_images
import os
app = Flask(__name__)
UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.register_blueprint(main_blueprint) # main_blueprint in main.py

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else: # if logged in
        return render_template('index.html', 
            username=session.get('username'),
            newsfeed=random_images(4)
        )

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        if (not username) or (not email):
            return render_template('login.html')
        session['username'] = username
        session['email'] = email
        session['logged_in'] = True
        return redirect(url_for('home'))
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.errorhandler(404)
def page_not_found(e): # error handler for 404
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.secret_key = os.urandom(12) # generate random key
    app.run(debug = True, host='0.0.0.0', port=5000) # run server
