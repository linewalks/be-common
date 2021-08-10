from flask_apispec import use_kwargs, marshal_with, doc
from flask_jwt_extended import (
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    create_access_token,
    get_raw_jwt
)
# main에서 auth 호출 후 auth에서 user 호출
from main.controllers.auth import auth_bp, API_CATEGORY, authroization_header
from main import app, db, jwt
from main.schema import (
    ResponseLoginSchema,
    RequestLoginSchema,
    ResponseBodySchema,
    ResponseAccessTokenSchema,
    RequestEmailVerification
)
from main.models.user import User
from main.models.common.error import (
    ResponseError,
    ERROR_NULL_EMAIL,
    ERROR_NULL_PASSWORD,
    ERROR_USER_EMAIL_EXISTS,
    ERROR_USER_EMAIL_NOT_EXISTS,
    ERROR_VERIFY_EMAIL_PASSWORD,
    ERROR_NOT_VALIDATED_ACCOUNT
)


@auth_bp.route('/signin', methods=["POST"])
@use_kwargs(RequestLoginSchema)
@marshal_with(ResponseLoginSchema, code=200)
@marshal_with(ResponseError)
@doc(tags=[API_CATEGORY],
     summary="로그인",
     description="사용자 로그인을 합니다")
def siginin(**kwargs):
  email = kwargs.get("email", None)
  password = kwargs.get("password", None)
  if not email:
    return ERROR_NULL_EMAIL.get_response()
  if not password:
    return ERROR_NULL_PASSWORD.get_response()
  if not User.exists(email):
    return ERROR_USER_EMAIL_NOT_EXISTS.get_response()
  u = User.get_inf0(email)
  if not u.verify_password(password):
    return ERROR_VERIFY_EMAIL_PASSWORD.get_response()
  if not u.confirmed:
    return ERROR_NOT_VALIDATED_ACCOUNT.get_response()
  return u.to_dict()
