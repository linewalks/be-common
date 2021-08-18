from marshmallow import fields, Schema, validate


def create_pagination_list_schema(nested_cls):
  class PaginationList(Schema):
    list = fields.List(fields.Nested(nested_cls), requried=True)
    page = fields.Int(required=True, validate=validate.Range(min=1))
    keyword = fields.Str(required=True)
    order_key = fields.Str(required=True)
    desc = fields.Str(required=True)

  return PaginationList


class RequestPagination(Schema):
  page = fields.Int(
      missing=1,
      validate=validate.Range(min=1),
      description="페이지 번호 (1부터 시작)"
  )
  length = fields.Int(missing=10, description="페이지당 길이")
