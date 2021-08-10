
import configparser  # config 설정
import os
import decimal
import flask.json
from datetime import timedelta  # 산술 연산이 가능한 date 객체
from flask import Flask, blueprints
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# swagger, OpenAPI 명세 작성
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_apispec.extension import FlaskApiSpec

app = Flask(__name__)
base_dir = os.getcwd()
app.config.from_pyfile(f"{base_dir}/main/default.cfg")
app.config["SQLACHEMY_TRACKJMODIFICATIONS"] = False
app.config.update({
    "APISPEC_SPEC": APISpec(
        title="skeleton",
        version="v1",
        openapi_version="2.0.0",
        plugins=[MarshmallowPlugin()],
    )
})
app.config["JWT_IDENTITY_CLAIM"] = "identity"
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=app.config["JWT_ACCESS_TOKEN_EXPIRES_TIME"])
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=app.config["JWT_REFRESH_TOKEN_EXPIRES_TIME"])
docs = FlaskApiSpec(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

from main.controllers.auth import auth_bp
blueprints = [
  auth_bp
]

for bp in blueprints:
  app.register_blueprint(bp)
docs.register_existing_resources()
