
import decimal
import flask.json
import os
import warnings
from datetime import timedelta  # 산술 연산이 가능한 date 객체
# swagger, OpenAPI 명세 작성
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask  # Falsk 2.0.0부터는 FlaskApiSpec이 동작하지 않는다. v1.1.2를 사용했다.
from flask_apispec.extension import FlaskApiSpec
from flask_compress import Compress
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

base_dir = os.getcwd()
config_dir = f"{base_dir}/main/default.cfg"
docs = FlaskApiSpec()
db = SQLAlchemy()
cors = CORS()
compress = Compress()
jwt = JWTManager()


def read_config(config_filename=config_dir):
  app = Flask(__name__)
  app.config.from_pyfile(config_filename)

  return app


class DecimalSerializeEncoder(flask.json.JSONEncoder):
  # jsonify decimal serialize 해결
  def default(self, obj):
    if isinstance(obj, decimal.Decimal):
      return float(obj)
    return super(DecimalSerializeEncoder, self).default(obj)


def create_app(config_filename=config_dir):
  app = Flask(__name__)
  app.json_encoder = DecimalSerializeEncoder

  app.config.from_pyfile(config_filename)
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

  docs.init_app(app)
  db.init_app(app)
  compress.init_app(app)
  jwt.init_app(app)
  cors.init_app(app)

  warnings.filterwarnings(
      "ignore",
      message="Multiple schemas resolved to the name ",
  )

  with app.app_context():
      # blueprint 추가
      from main.controllers import skeleton_bp
      from main.controllers.auth import auth_bp
      from main.controllers.cdm import cdm_bps

      blueprints = [auth_bp, skeleton_bp]
      blueprints.extend(cdm_bps)

      for bp in blueprints:
        app.register_blueprint(bp)

      docs.register_existing_resources()

      # 스웨거에서 options 제거
      for key, value in docs.spec._paths.items():
        docs.spec._paths[key] = {
            inner_key: inner_value for inner_key, inner_value in value.items() if inner_key != "options"
        }

  return app
