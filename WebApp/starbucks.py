import os
import random

# used for upload features
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpg'])

def setUploadFolder(app): # set upload folder
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
        if ext == '.jpg': # 확장자가 jpg 파일이면
            result.append(full_filename) # 리스트에 추가
    return result # 리스트 반환

def getTagList(): # static/uploads에 있는 태그 파일이름 리스트를 가져옴
    filenames = os.listdir(UPLOAD_FOLDER) # 업로드 폴더 디렉토리 리스팅
    result=[] # 리스트 생성
    for filename in filenames:
        full_filename = os.path.join(UPLOAD_FOLDER, filename)
        if ('_tag.txt' not in full_filename)==False: # 태그 파일이면
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

def getFileExtension(filename): # 파일의 확장자를 구함
    result = os.path.splitext(filename)[1] # 파일의 확장자를 구함
    return result # 구한 확장자를 반환

def getImageData(filename): # filename이 가리키는 이미지에 해당되는 본문 데이터를 반환함
    article = ''
    # 데이터 파일이 있는지 확인
    if os.path.isfile(filename + '_data.txt') is True: # 파일 있음
        # 파일에서 내용 읽고 전달
        with open(filename + '_data.txt', 'r') as f:
            article = f.read()
    else:
        # "글이 없습니다" 전달
        article = "글이 없습니다."
    return article

def logger(filename, username): # 로그 기록
    # 현재 접속한 사용자명이 수정한 파일 정보를 filename_log.txt 기록
    logfile = filename + '_log.txt'
    # 로그 파일이 없으면  w로 열어서 생성, 바로 닫기
    if os.path.isfile(logfile) is False:
        f = open(logfile, 'w')
        f.close()
    # a로 열고 정보 추가, 닫기
    f = open(logfile, 'a')
    f.write(username + '\n')
    f.close()

def return_log(filename, username):
    # 해당 파일 이름(filename), 현재 유저 이름(username) 인수로 받고 로그 파일 리스트를 반환
    logfile = filename + '_log.txt'
    # 로그 파일이 없으면 걍 패스
    if os.path.isfile(logfile) is False:
        return "none"
    f = open(logfile, 'r')
    loglist = []
    for i in f.readlines():
        loglist.append(i.strip('\n'))
    for i in range(0, len(loglist)):
        if i < len(loglist)-1:
            loglist[i]+=', '
    f.close()
    return loglist

def searchImage(searchName): # 태그나 파일명에 searchName이 포함되어 있는 파일 리스트를 검색하는 함수
    taglist = getTagList(); # 태그 먼저 검색
    result = [] # 검색결과를 저장할 배열
    for item in taglist:
        f = open(item, 'r')
        data = f.read()
        f.close()
        if (searchName not in data)==False: # 검색대상이 발견된 항목
            result.append(item)
    for i in range(0, len(result)):
        result[i] = result[i].replace('_tag.txt', '.jpg')
        print(result[i])
    imagelist = getImageList() # 이제 이미지 차례
    for item in imagelist:
        if (searchName not in item)==False: # 검색대상이 발견된 항목
            if item not in result:
                result.append(item)
    return result
