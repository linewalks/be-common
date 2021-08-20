from sqlalchemy.orm import query
import ujson
from marshmallow import ValidationError


def to_json(data):
  return ujson.loads(data)


def _test_get_status_code(client, status_code, url, query_string=None, schema=None):
  rv = client.get(url, query_string=query_string)
  assert rv.status_code == status_code
  if schema:  # validate schema
    errors = schema.validate(rv.json)
    if errors:
      raise ValidationError(errors)
  return rv
