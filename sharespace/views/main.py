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
from werkzeug import secure_filename
import os, base64, random
import image_classification
from server import app
from server.database import *

ALLOWED_EXTENSIONS = set(['.jpg', '.jpeg'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files: # no file part in POST request
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '': # no file selected
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect('/view/' + get_img_id(filename))
            newpost = Post(
                title = 'test',
                author = current_user.username,
                article = 'test',
                image_url = url_for('static', filename='uploads/' + filename),
                tags = ['a', 'b', 'c']
            )
            
            return redirect(url_for('backdoor'))
    return render_template('vrview/upload.html')
