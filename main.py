from flask import Blueprint, session, request, render_template, redirect
import os, base64
from werkzeug import secure_filename
from flask import current_app as app
import os, random, image_classification

main = Blueprint('main', __name__, template_folder='templates/main')
ALLOWED_EXTENSIONS = set(['.jpg', '.jpeg'])

def get_img_url(filename):
    return request.url_root + 'static/uploads/' + os.path.basename(filename)

def get_img_id(filename):
    return base64.b64encode(bytes(get_img_url(filename), 'UTF-8')).decode()

def get_url(filename):
    return [get_img_url(filename), '/view/' + get_img_id(filename)]
 
def allowed_file(filename):
    return os.path.splitext(filename)[1] in ALLOWED_EXTENSIONS

def random_images(number):
    return [get_url(name) for name in random.sample(os.listdir('./static/uploads/'), number)]

@main.route('/view/<image_id>') # 현재는 그냥 파일명만 받게 됨
def view(image_id):
    if not session.get('logged_in'):
        return render_template('login.html')
    image_path = base64.b64decode(image_id).decode()
    image_name = os.path.basename(image_path)
    # for testing
    title = 'Petra'
    article = 'Petra, originally known to its inhabitants as Raqmu, is a historical and archaeological city in southern Jordan.'
    # 요청받은 id의 파일에 대한 정보(제목, 본문, 태그)를 가져와 템플릿으로 전달해야 함
    # 태그 정보가 없을 경우, image_classification으로 태그를 생성해 저장함.
    # print(image_path)
    return render_template(
        'vrview/view.html', 
        image_url=image_path, # 이미지가 있는 정적 URL 주소
        current_url=request.base_url, # 렌더링된 게시물의 URL (클립보드로 복사해 공유 기능을 제공)
        title=title, article=article, # 게시물 제목 및 본문
        tags=image_classification.classification(os.path.join(app.config['UPLOAD_FOLDER'], image_name))
        # 이미지 인식 후 반환된 추론 결과(태그)를 템플릿에 전달
    )

@main.route('/upload', methods=['GET', 'POST'])
def upload():
    if not session.get('logged_in'):
        return render_template('login.html')
    if request.method == 'POST':
        if 'file' not in request.files: # no file part in POST request
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '': # no file selected
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect('/view/' + get_img_id(filename))
    return render_template('vrview/upload.html')

@main.route('/search')
def search():
    if not session.get('logged_in'):
        return render_template('login.html')
    return 'unavailable at the moment'
