from flask import Flask, render_template, redirect, request, flash, session, abort, url_for
# flask 이용
from sqlalchemy.orm import sessionmaker
# sqlalchemy 이용
from werkzeug import secure_filename
# 파일 업로드에 사용

from image_classification import *
from database import * # 데이터베이스 생성 및 관리
from starbucks import * # starbucks library에서 정의된 함수 가져옴

engine = create_engine('sqlite:///LETSBE.db', echo=True) # 레쓰비 만세
app = Flask(__name__)
setUploadFolder(app)
globaldata = ['', ''] # globaldata = [filename, username]
# 두 가지 전역변수를 한꺼번에 하나의 리스트에 저장
# 전역변수를 더 효율적으로, 가독성 좋게 사용하기 위함임

@app.route('/') # 시작 화면
def home():
    # 로그인 되어 있지 않으면 로그인 페이지로 이동
    if not session.get('logged_in'):
        # flash로 메세지 받은 건 템플릿에서 처리
        return render_template('login.html')
    # 로그인 되었으면 바로 인덱스 페이지로 이동
    else:
        global globaldata
        return render_template('index.html', username = globaldata[1])

@app.route('/login', methods=['POST']) # 로그인
def login(): # login.html에서 받은 데이터 사용
    username_post = str(request.form['username']) # username
    password_post = str(request.form['password']) # password
    global globaldata
    globaldata[1] = username_post
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
    Session = sessionmaker(bind=engine)
    s = Session() # session 생성
    global globaldata
    sql = "DELETE FROM userinfo WHERE username=\'" + globaldata[1] + "\';"
    print(sql)
    result = engine.execute(sql) # sql문 실행
    # 해당 id의 데이터 삭제
    s.commit() # 세션 커밋
    session['logged_in'] = False
    return home()

@app.route('/signup') # 회원가입
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST']) # 회원가입 백엔드 처리
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
        print('[*] hihi')
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            print('[*] nofile?')
            return redirect(request.url)
        file = request.files['file']
        open(app.config['UPLOAD_FOLDER']+'/'+file.filename, 'w').close()
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('[*] no selected')
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(app.config['UPLOAD_FOLDER']+'/'+file.filename)
            return home() # 파일 업로드 성공
    return render_template('upload/upload.html') # 파일 업로드 폼

@app.route('/view')
def view(): # view 템플릿 렌더링
    return render_template('view/view.html')

@app.route('/view-result', methods=['GET'])
def view_back(): # vrview
    try:
        title = request.args.get('filename').replace('.jpg', '')
        print(title)
        filename = 'static/uploads/' + title
        if not (getFileExtension(filename)=='.jpg'):
            filename += '.jpg'
        txtfile = os.path.splitext(filename)[0] # 파일명
        # ex> 'static/uploads/filename.txt' => 'static/uploads/filename'
        global globaldata
        globaldata[0] = txtfile
        txtfile = txtfile + '_tag.txt' # 태그 파일 이름
        # ex> 'static/uploads/filename.txt' => 'static/uploads/filename_tag.txt'
        if os.path.isfile(txtfile) is True: # 태그 파일이 존재
            # 파일이 존재, 열기 성공이면 해당파일의 태그를 읽음
            # read tags in txtfile => tag/tag-result.html에 전달
            result = []
            with open(txtfile, 'r') as fp:
                for tag in fp:
                    result.append(tag)
            filename = filename.replace('static/uploads/', '')
            filename = 'vrview/index.html?image=../uploads/' + filename + '&is_stereo=false'
            print(filename)
            article = getImageData(globaldata[0])
            loglist = return_log(globaldata[0], globaldata[1])
            return render_template('view/view-result.html', title=title, filename=filename, tags=result, article=article, loglist=loglist)
        else:
            # 없으면 classification()을 돌린다
            # 돌린 다음에 tag를 filename_tag.txt로 한 줄에 한 개씩 저장
            result = classification('C:', filename)
            f = open(txtfile, 'w')
            for tag in result:
                f.write(tag + '\n')
            f.close()
            # 파일에 태그 기록
            filename = g_filename.replace('static/uploads/', '')
            filename = 'vrview/index.html?image=../uploads/' + filename + '.jpg' + '&is_stereo=false'
            article = getImageData(globaldata[0])
            loglist = return_log(globaldata[0], globaldata[1])
            return render_template('view/view-result.html', filename=filename, tags=result, article=article, loglist=loglist)
    except:
        return render_template('view/view-error.html')

@app.route('/edit')
def edit(): # write 템플릿 렌더링
    article = getImageData(globaldata[0])
    return render_template('upload/edit.html', basic_text = article) # 기본값은 원래 있던 글

@app.route('/edit', methods=['POST'])
def edit_back():
    text = request.form['text']
    global globaldata
    f = open(globaldata[0] + "_data.txt", 'w')
    f.write(text)
    f.close()
    filename = globaldata[0].replace('static/uploads/', '')
    filename = 'vrview/index.html?image=../uploads/' + filename + '.jpg' + '&is_stereo=false'
    # text를 filename_data.txt로 static/uploads에 저장
    txtfile = globaldata[0] + '_tag.txt' # 태그 파일 이름
    if os.path.isfile(txtfile) is True: # 태그 파일이 존재
        # 파일이 존재, 열기 성공이면 해당파일의 태그를 읽음
        # read tags in txtfile => tag/tag-result.html에 전달
        result = []
        with open(txtfile, 'r') as fp:
            for tag in fp:
                result.append(tag)
    else:
        # 없으면 classification()을 돌린다
        # 돌린 다음에 tag를 filename_tag.txt로 한 줄에 한 개씩 저장
        result = classification('C:', filename)
        f = open(txtfile, 'w')
        for tag in result:
            f.write(tag + '\n')
        f.close()
        # 파일에 태그 기록
    logger()
    loglist=return_log(globaldata[0], globaldata[1])
    return render_template('view/view-result.html', filename=filename, tags=result, article=text, loglist=loglist)

'''
<newsfeed / 뉴스피드>
static/uploads에서 '.jpg'  파일 검색 결과를 리스트에 저장
리스트를 랜덤으로 셔플
img로 이미지와 이미지 이름을 보여주고 클릭시 view page를 보여줌(GET)
'''
@app.route('/newsfeed')
def newsfeed():
    shuffled = getShuffledImageList()
    length = len(shuffled)
    if length < 5:
        length = len(shuffled)
    shuffled = shuffled[:length]
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
    # <= 이거 걍 title이랑 같은 거 같은데 고치면 시간없으니 걍 둘게요~
    # (비슷한 서치리절드에서는 제대로 구현 시도함)
    view = []
    for image in shuffled:
        temp = image.replace('static/uploads\\', '')
        view.append(temp)
    print('[*] title : ' + str(title))
    print('[*] filename : ' + str(filename))
    print('[*] view : ' + str(view))
    return render_template('newsfeed.html', title=title, filename=filename, view=view, length=length)
    # 뉴스피드 템플릿 반환

'''
<image name, tag로 검색>
search result 배열 만듦
static/uploads에서 '.jpg' 파일 검색
    => 있으면 search result에 추가
static/uploads에서 '.txt' 파일 검색
    => 순차적으로 하나씩 열어서 내용에 있으면 해당 태그 파일의 이미지 이름을 search result에 추가
search result에 검색 결과(이미지 파일 이름)이 저장

=>  위 내용을 구현한 것이 바로 본 파일 위에 정의한 searchImage() 함수
여기서는 입력받은 데이터를 인수로 searchImage()에 전달하고 리턴한 검색결과 배열만큼을 피드로 나타내줌
'''
@app.route('/search', methods=['POST'])
def search():
    data = str(request.form['data'])
    print(data)
    result = searchImage(data)
    print(result)
    title = []
    # 경로, 확장자 없이 순수 filename만 있는 배열 title
    for image in result:
        temp = image.replace('static/uploads\\', '')
        temp = os.path.splitext(temp)[0]
        title.append(temp)
    filename = []
    # 'uploads/filename.jpg'와 같은 형태의 배열 filename
    for image in result:
        temp = image.replace('static/', '')
        temp = temp.replace('\\', '/')
        filename.append(temp)
    view = title
    # 경로 없고 그냥 파일네임만(+확장자는 선택 => 즉 title과 같음)
    length=len(title)
    return render_template('view/search-result.html', title=title, filename=filename, view=view, length=length)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    # 404 에러 처리

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug = True, host='0.0.0.0', port=7000)
    # 앱 시작
