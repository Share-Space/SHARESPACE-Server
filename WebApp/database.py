# DB 생성, 관리
# 주의사항 : 보안 따위 업슴
# https://pythonspot.com/login-authentication-with-flask/ 참고
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///LETSBE.db', echo=True)
# 데이터베이스 이름은 LETSBE(레쓰비)
# 이는 ReSEApe 때부터 내려온 전설의 네이밍 기법에 의해서이다
Base = declarative_base()

########################################################################
class User(Base):
    """"""
    __tablename__ = 'userinfo' # 테이블 명은 userinfo

    id = Column(Integer, primary_key=True)
    username = Column(String) # 사용자이름
    password = Column(String) # 비밀번호
    email = Column(String) # 이메일

    #----------------------------------------------------------------------
    def __init__(self, username, password, email):
        """"""
        self.username = username # 사용자이름
        self.password = password # 비밀번호
        self.email = email # 이메일

'''
id: username, pw: username인 유저 생성:
Session = sessionmaker(bind=engine)
session = Session() # 세션 생성
user = User('username', 'username') # user 생성
session.add(user) # user 추가
session.commit() # 세션 커밋

id: username인 유저 삭제:
result = engine.execute("DELETE FROM userinfo WHERE username='username';") # sql문 실행
'''

# create tables
Base.metadata.create_all(engine)
