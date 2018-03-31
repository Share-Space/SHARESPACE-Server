import os
import random
from flask import Flask, render_template, redirect, request, flash, session, abort, url_for
# flask 이용
from sqlalchemy.orm import sessionmaker
# sqlalchemy 이용
from werkzeug import secure_filename
# 파일 업로드에 사용

from database import * # 데이터베이스 생성 및 관리

engine = create_engine('sqlite:///LETSBE.db', echo=True) # 레쓰비 만세
username = '' # username 전역변수
app = Flask(__name__)

# used for upload features
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getImageList(): # static/uploads에 있는 이미지 파일이름 리스트를 가져옴
    filenames = os.listdir(UPLOAD_FOLDER) # 업로드 폴더 디렉토리 리스팅
    result=[] # 리스트 생성
    for filename in filenames:
        full_filename = os.path.join(UPLOAD_FOLDER, filename)
        ext = os.path.splitext(full_filename)[-1] # 확장자를 구함
        if ext == '.jpg' or ext == '.jpeg': # 확장자가 jpg, jpeg 파일이면
            result.append(full_filename) # 리스트에 추가
    return result # 리스트 반환

def getRandomImage(): # getImageList에서 무작위로 하나 꺼내서 vrview 링크를 반환
    result = getImageList() # 업로드 폴더의 이미지 리스트를 가져옴
    filename = random.choice(result) # 그 중 하나를 무작위로 구함
    filename = filename.replace('static/uploads\\', '')
    filename = 'vrview/index.html?image=../uploads/' + filename + '&is_stereo=false'
    return filename # 무작위로 고른 이미지의 vrview 링크를 구한 뒤 반환

def getShuffledImageList(): # getImageList를 무작위로 셔플한 값을 반환
    shuffled = getImageList() # 업로드 폴더의 이미지 리스트를 가져옴
    random.shuffle(shuffled) # 가져온 이미지 리스트를 무작위로 셔플
    return shuffled # 셔플한 이미지 리스트를 반환

def getFileExtension(file_name): # 파일의 확장자를 구함
    result = os.path.splitext(file_name)[1] # 파일의 확장자를 구함
    return result # 구한 확장자를 반환

@app.route('/') # 시작 화면
def home():
    # 로그인 되어 있지 않으면 로그인 페이지로 이동
    if not session.get('logged_in'):
        # flash로 메세지 받은 건 템플릿에서 처리
        return render_template('login.html')
    # 로그인 되었으면 바로 인덱스 페이지로 이동
    else:
        global username
        return render_template('index.html', username = username)

@app.route('/login', methods=['POST']) # 로그인
def login(): # login.html에서 받은 데이터 사용
    username_post = str(request.form['username']) # username
    password_post = str(request.form['password']) # password
    global username
    username = username_post
    Session = sessionmaker(bind=engine)
    s = Session() # session 생성
    query = s.query(User).filter(User.username.in_([username_post]), User.password.in_([password_post]))
    result = query.first()
    if result: # result = True
        session['logged_in'] = True # 로그인 성공
    else:
        flash('wrongData') # 잘못된 데이터
    return home() # 시작 화면으로 가서 처리

@app.route('/logout') # 로그아웃
def logout():
    session['logged_in'] = False # 세션 로그아웃
    return home() # 시작 화면으로 돌아가기

@app.route('/signout') # 탈퇴
def signout():
    global username
    Session = sessionmaker(bind=engine)
    s = Session() # session 생성
    sql = "DELETE FROM userinfo WHERE username=\'" + username + "\';"
    print(sql)
    result = engine.execute(sql) # sql문 실행
    # 해당 id의 데이터 삭제
    s.commit() # 세션 커밋
    session['logged_in'] = False
    return home()

@app.route('/signup') # 회원가입
def signup():
    return render_template('signup.html')

@app.route('/signup-back', methods=['POST']) # 회원가입 백엔드 처리
def signup_back():
    username_post = str(request.form['username']) # username
    password_post = str(request.form['password']) # password
    email_post = str(request.form['email']) # email
    Session = sessionmaker(bind=engine)
    session = Session()
    user = User(username_post, password_post, email_post)
    session.add(user) # 입력한 정보의 유저 추가
    session.commit()
    flash('signUp') # 가입완료 메세지 플래싱
    return home()

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # https://www.tutorialspoint.com/flask/flask_file_uploading.htm 참고
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        open(app.config['UPLOAD_FOLDER']+'/'+file.filename, 'w').close()
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(app.config['UPLOAD_FOLDER']+'/'+file.filename)
            return '<h1>success</h1>' # 파일 업로드 성공
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    ''' # 파일 업로드 폼

@app.route('/view')
def view(): # view 템플릿 렌더링
    return render_template('view/view.html')

@app.route('/view-result', methods=['GET'])
def view_back(): # vrview
    filename = ''
    try:
        filename = 'static/uploads/' + request.args.get('filename')
        if not (getFileExtension(filename)=='.jpg' or getFileExtension(filename)=='.jpeg'):
            filename += '.jpg' # 확장자 체크, 따로 확장자를 주지 않았다면 자동으로 .jpg를 붙임
        filename = filename.replace('static/uploads/', '')
        filename = 'vrview/index.html?image=../uploads/' + filename + '&is_stereo=false'
        return render_template('view/view-result.html', filename=filename)
    except:
         return render_template('view/view-error.html')

'''
<newsfeed / 뉴스피드>
static/uploads에서 '.jpg' / '.jpeg' 파일 검색 결과를 리스트에 저장
리스트를 랜덤으로 셔플
img로 이미지와 이미지 이름을 보여주고 클릭시 view page를 보여줌(GET)
'''
@app.route('/newsfeed')
def newsfeed():
    shuffled = getShuffledImageList()
    shuffled = shuffled[:5]
    # 경로, 확장자 없이 순수 filename만 있는 배열 title
    title = []
    for image in shuffled:
        temp = image.replace('static/uploads\\', '')
        temp = os.path.splitext(temp)[0]
        title.append(temp)
    # 'uploads/filename.jpg'와 같은 형태의 배열 filename
    filename = []
    for image in shuffled:
        temp = image.replace('static/', '')
        temp = temp.replace('\\', '/')
        filename.append(temp)
    # 해당 이미지의 vrview 링크인 view
    view = []
    for image in shuffled:
        temp = image.replace('static/uploads\\', '')
        view.append(temp)
    return render_template('newsfeed.html', title=title, filename=filename, view=view)
    # 뉴스피드 템플릿 반환

'''
<image name, tag로 검색>
search result 배열 만듦
static/uploads에서 '.jpg' / '.jpeg' 파일 검색
    => 있으면 search result에 추가
static/uploads에서 '.txt' 파일 검색
    => 순차적으로 하나씩 열어서 내용에 있으면 해당 태그 파일의 이미지 이름을 search result에 추가
search result에 검색 결과(이미지 파일 이름)이 저장
'''

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    # 404 에러 처리

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug = True, host='0.0.0.0', port=5000)
    # 앱 시작
