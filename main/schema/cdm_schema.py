from marshmallow import fields, Schema
from main.models.common.common import (
    create_pagination_list_schema,
    RequestPagination
)


# Request
class RequestSearch(RequestPagination):
  keyword = fields.Str(description="검색할 키워드입니다.", missing="")
  order_key = fields.Str(description="정렬의 기준이 될 컬럼입니다.", missing=None)
  desc = fields.Int(description="정렬 방식을 말합니다. (0: 오름차순, 1: 내림차순)", missing=0)


class RequestTableSearch(RequestSearch):
  target_column = fields.Str(description="검색할 컬럼입니다", required=True)


# Response
class PersonCount(Schema):
  person_count = fields.Int(description="환자 수")


class VisitCount(Schema):
  visit_count = fields.Int(description="방문 수")


class Concept(Schema):
  concept_id = fields.Int(description="Concept ID")
  concept_name = fields.Str(description="Concept 이름")


class ConceptInfo(Schema):
  concept_id = fields.Int()
  concept_name = fields.Str()
  domain_id = fields.Str()
  vocabulary_id = fields.Str()
  concept_class_id = fields.Str()
  standard_concept = fields.Str()
  row_count = fields.Str()


class Source(Schema):
  source_value = fields.Str(description="Source Value")


class Search(Schema):
  row_count = fields.Int(description="사용 row 수")


class ConceptPersonCount(Concept, PersonCount):
  pass


class SourcePersonCount(Source, PersonCount):
  pass


class ConceptVisitCount(Concept, VisitCount):
  pass


class SourceVisitCount(Source, VisitCount):
  pass


class ConceptSearchCount(ConceptInfo, Search):
  pass


class ResponseConceptPageSchema(Schema):
  concept_info = fields.List(fields.Nested(ConceptInfo, required=True))


def create_nested_list_schema(root_name, schema):
  schema_name = root_name.split("_")[0].capitalize()
  schema_name = f"Response{schema_name}Count"
  return Schema.from_dict({
      root_name: fields.List(fields.Nested(schema))
  }, name=schema_name)


ResponseConceptPersonCount = create_nested_list_schema("person_list", ConceptPersonCount)
ResponseSourcePersonCount = create_nested_list_schema("person_list", SourcePersonCount)
ResponseConceptVisitCount = create_nested_list_schema("visit_list", ConceptVisitCount)
ResponseSourceVisitCount = create_nested_list_schema("visit_list", SourceVisitCount)
ResponseConceptSearchCount = create_pagination_list_schema(ConceptSearchCount)
