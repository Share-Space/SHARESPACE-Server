<h1 align="center">
  <a href="https://github.com/404-NOTFOUND">
    <img src="./sharespace/static/logo.png" width="150"><br>
  </a>
  SHARESPACE-Server
</h1>
<p align="center">
SHARESPACE Server & Web app with Python Flask, Google VR view
<br><br>
<a href="https://www.python.org/download/releases/3.0/">
  <img alt="forthebadge made-with-python" src="http://ForTheBadge.com/images/badges/made-with-python.svg"/>
</a>
<a href="https://github.com/googlevr/vrview">
  <img alt="ForTheBadge uses-js" src="http://ForTheBadge.com/images/badges/uses-js.svg"/>
</a>
</p>

> 해커톤 당시 만들었던 결과물은 `hackathon` 브랜치에 있습니다 :)

----------

## Server (REST API with Flask-RESTful)

### Newsfeed
서버에 있는 전체 이미지 중에서 무작위로 일정 개수의 이미지를 선택해 각각 제목과 이미지 URL을 제공한다.

### Image infomation
요청받은 이미지에 대한 정보를 제공한다.

- 제목
- 본문
- 태그
- 게시자 이름
- 이미지 URL

## Web app

### Google VR view
Google의 [VR view](https://developers.google.com/vr/develop/web/vrview-web) JavaScript API를 이용해서 360° 포토를 임베딩한다.

```HTML
<script src="https://storage.googleapis.com/vrview/2.0/build/vrview.min.js"></script>
```
