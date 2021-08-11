from marshmallow import fields, Schema


# Requests
class RequestBodySchema(Schema):
  id = fields.Int(required=True)
  name = fields.Str(required=True)
  count = fields.Int(required=True)


class RequestParameterSchema(Schema):
  id = fields.Int(requried=True, location="query")


class RequestLoginSchema(Schema):
  email = fields.Str(required=True)
  password = fields.Str(required=True)


# Response
class ResponseBodySchema(Schema):
  skeleton = fields.Nested(RequestBodySchema)


class ResponseLoginSchema(Schema):
  access_token = fields.Str(data_key="accessToken")
  refresh_token = fields.Str(data_key="refreshToken")
  email = fields.Str()


class ResponseAccessTokenSchema(Schema):
  access_token = fields.Str(data_key="accessToken")
