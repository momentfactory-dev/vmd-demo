# file name : __init__.py
# pwd : /project_name/app/__init__.py

from flask import Flask
from webapp.core.controller.LoginController import path as path_login

app = Flask(__name__)

# 위에서 추가한 파일을 연동해주는 역할
app.register_blueprint(path_login)

