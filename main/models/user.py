from datetime import datetime
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token
)
from werkzeug.security import check_password_hash, generate_password_hash
from main import app, db


class User(db.Model):
  __tablename__ = "users"
  __table_args__ = {"schema": app.config["SCHEMA_TEST"]}
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(64), unique=True, index=True)
  password_hash = db.Column(db.String(128))
  token = db.Column(db.String(64))
  token_created_time = db.Column(db.DateTime, default=datetime.utcnow)

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.password = kwargs["password"]

  def __repr__(self):
    return "<User %r>" % self.email

  @property
  def password(self):
    raise AttributeError("password is not a readable attribute")

  @password.setter
  def password(self, password):
    self.password_hash = generate_password_hash(password)

  def verify_password(self, password):
    return check_password_hash(self.password_hash, password)

  def generate_access_token(self):
    return create_access_token(identity=dict(email=self.email))

  def generate_refresh_token(self):
    return create_refresh_token(identity=dict(email=self.email))

  def to_dict(self):
    access_token = self.generate_access_token()
    refresh_token = self.generate_refresh_token()
    TokenBlacklist.add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    TokenBlacklist.add_token_to_database(refresh_token, app.config["JWT_IDENTITY_CLAIM"])
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "email": self.email
    }

  @staticmethod
  def exists(email):
    return User.query.filter(User.email == email).scalar()

  @staticmethod
  def get_info(email):
    return User.query.filter(User.email == email).first()

  @staticmethod
  def delete(email):
    User.query.filter(User.email == email).delete()


class TokenBlacklist(db.Model):
  __tablename__ = "tokenblacklist"
  __table_args__ = {"schema": app.config["SCHEMA_TEST"]}
  id = db.Column(db.Integer, primary_key=True)
  jti = db.Column(db.String(36), nullable=False)
  token_type = db.Column(db.String(10), nullable=False)
  user_id = db.Column(
      db.Integer,
      db.ForeignKey(f"{app.config['SCHEMA_TEST']}.users.id", ondelete="SET NULL"),  # f-string 내부에서 dict key 사용을 위해 ' 사용
      nullable=True
  )
  revoked = db.Column(db.Boolean, nullable=False)
  expires = db.Column(db.DateTime, nullable=False)

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def to_dict(self):
    return {
        "token_id": self.id,
        "jti": self.jti,
        "token_type": self.token_type,
        "user_id": self.user_id,
        "revoked": self.revoked,
        "expires": self.expires,
    }

  @staticmethod
  def _epoch_utc_to_datetime(epoch_utc):
    """
    JWT의 저장 시각은 UTC로 계산한다.
    """
    return datetime.fromtimestamp(epoch_utc)

  @staticmethod
  def add_token_to_database(encoded_token, identity_claim):
    """
    새로운 토큰이 revoked 되지 않았을 때 그 토큰을 db에 추가한다.
    """
    decoded_token = decode_token(encoded_token)
    jti = decoded_token["jti"]
    token_type = decoded_token["type"]
    user_id = User.get_info(decoded_token[identity_claim]["email"]).id
    expires = TokenBlacklist._epoch_utc_to_datetime(decoded_token["exp"])
    revoked = False
    db_token = TokenBlacklist(
        jti=jti,
        token_type=token_type,
        user_id=user_id,
        expires=expires,
        revoked=revoked,
    )
    db.session.add(db_token)
    db.session.commit()

  @staticmethod
  def is_token_revoked(decoded_token):
    """
    토큰의 revoked 여부를 검증한다. 모든 토큰은 생성과 동시에 DB에 추가되므로
    DB에 토큰이 없다면 생성자를 모르니 취소된 것으로 처리한다.
    """
    jti = decoded_token["jti"]
    try:
      token = TokenBlacklist.query.filter_by(jti=jti).one()
      return token.revoked
    except NoResultFound:
      return True

  @staticmethod
  def revoke_token(decoded_token, identity_claim):
    """
    토큰을 revoke시킨다. 만약 DB에 토큰이 존재하지 않는다면 ERROR를 발생시킨다.
    """
    try:
      jti = decoded_token["jti"]
      email = decoded_token[identity_claim]["email"]
      token = TokenBlacklist.query.filter(TokenBlacklist.jti == jti).one()
      token.revoked = True
      db.session.commit()
    except NoResultFound():
      raise TokenNotFound(f"Could not find the token for user.email{email}")