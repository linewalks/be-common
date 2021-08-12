
import os
from datetime import timedelta  # 산술 연산이 가능한 date 객체
from flask import Flask  # Falsk 2.0.0부터는 FlaskApiSpec이 동작하지 않는다. v1.1.2를 사용했다.
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_compress import Compress
from flask_jwt_extended import JWTManager

# swagger, OpenAPI 명세 작성
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

app = Flask(__name__)
base_dir = os.getcwd()
app.config.from_pyfile(f"{base_dir}/main/default.cfg")
app.config["SQLALCHEMY_BINDS"] = {
    "test": app.config["TEST_DATABASE_URI"],
    "synthea": app.config["SYNTHEA_DATABASE_URI"]
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config.update({
    "APISPEC_SPEC": APISpec(
        title="CRUD api",
        version="v1",
        openapi_version="2.0.0",
        plugins=[MarshmallowPlugin()],
    ),
    "APISPEC_SWAGGER_URL": "/docs.json",
    "APISPEC_SWAGGER_UI_URL": "/docs/"
})
app.config["JWT_IDENTITY_CLAIM"] = "identity"
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=app.config["JWT_ACCESS_TOKEN_EXPIRES_TIME"])
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=app.config["JWT_REFRESH_TOKEN_EXPIRES_TIME"])

docs = FlaskApiSpec(app)
db = SQLAlchemy(app)
compress = Compress(app)
jwt = JWTManager(app)
CORS(app)

# blueprint 추가
from main.controllers.auth import auth_bp
from main.controllers import skeleton_bp

blueprints = [auth_bp, skeleton_bp]

for bp in blueprints:
  app.register_blueprint(bp)

docs.register_existing_resources()

# 스웨거에서 options 제거
for key, value in docs.spec._paths.items():
  docs.spec._paths[key] = {
      inner_key: inner_value for inner_key, inner_value in value.items() if inner_key != "options"
  }

db.create_all()  # DB 없으면 생성
