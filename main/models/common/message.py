from marshmallow import fields, Schema


# 기존 Flask-Skeleton에서 Error였지만 Success도 다루므로 Message로 변경
class Message:
  def __init__(self, id, msg, code):
    self.id = id
    self.msg = msg
    self.code = code  # http status code

  def get_response(self, **msg_kwargs):
    msg = self.msg.format(**msg_kwargs)
    return {"msg_id": self.id, "msg": msg}, self.code


# 기존 ResponseError였으나 Success도 다루므로 ResponseMessage로 변경
class ResponseMessage(Schema):
  msg_id = fields.Str(data_key="msgId")
  msg = fields.Str()


# 에러 코드 정의 방법
# 같은 카테고리의 에러는 뒤 숫자만 변경 u001, u002, u003
# 새로운 카테고리의 에러는 앞 숫자 변경 u101, u201
# 같은 에러지만 상태 코드가 다른 경우, 같은 에러 코드를 쓴다
# 성공이지만 메세지가 필요한 경우, 다음과 같이 명명한다. SUCCESS_*
ERROR_VERIFY_EMAIL_PASSWORD = Message("u005", "Email or Password is not verified", 400)
ERROR_NULL_EMAIL = Message("u006", "Email should not be null.", 400)
ERROR_NULL_PASSWORD = Message("u007", "Password should not be null.", 400)
ERROR_USER_EMAIL_EXISTS = Message("u008", "User email already exists.", 409)
ERROR_USER_EMAIL_NOT_EXISTS = Message("u009", "User email not exists.", 400)
ERROR_USER_NOT_EXISTS = Message("u011", "User does not exist.", 401)

ERROR_ID_NOT_EXISTS = Message("u101", "Id not exists.", 400)
ERROR_ID_ALREADY_EXISTS = Message("u102", "Id already exists.", 400)

SUCCESS_ID_INSERT = Message("u202", "id insert success.", 200)
SUCCESS_ID_UPDATE = Message("u203", "id update success.", 200)
SUCCESS_ID_DELETE = Message("u204", "id delete success.", 200)
SUCCESS_SIGNUP = Message("u205", "sign up success.", 200)
SUCCESS_LOGOUT = Message("u206", "sign out success.", 200)

ERROR_PARAMETER_NOT_EXISTS = Message("u301", "parameter not exists.", 404)
ERROR_BODY_NOT_EXISTS = Message("u302", "body not exists.", 400)
