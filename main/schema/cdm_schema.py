from marshmallow import fields, Schema


# Request
class RequestSearch(Schema):
  keyword = fields.Str(description="검색할 키워드입니다.")
  page = fields.Int(description="page index 입니다.")
  page_cnt = fields.Int(description="한 page 당 item의 개수입니다.")


# Response
class PersonCount(Schema):
  person_count = fields.Int(description="환자 수")


class VisitCount(Schema):
  visit_count = fields.Int(description="방문 수")


class Concept(Schema):
  concept_id = fields.Int(description="Concept ID")
  concept_name = fields.Str(description="Concept 이름")


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


class ConceptSearchCount(Concept, Search):
  pass


def create_nested_list_schema(root_name, schema, name):
  return Schema.from_dict({
      root_name: fields.List(fields.Nested(schema))
  }, name=name)


def create_concept_person_count_list_schema(root_name):
  schema_name = root_name.split("_")[0].capitalize()
  schema_name = f"Response{schema_name}Count"
  return create_nested_list_schema(root_name, ConceptPersonCount, schema_name)


def create_source_person_count_list_schema(root_name):
  schema_name = root_name.split("_")[0].capitalize()
  schema_name = f"Response{schema_name}Count"
  return create_nested_list_schema(root_name, SourcePersonCount, schema_name)


def create_concept_visit_count_list_schema(root_name):
  schema_name = root_name.split("_")[0].capitalize()
  schema_name = f"Response{schema_name}Count"
  return create_nested_list_schema(root_name, ConceptVisitCount, schema_name)


def create_source_visit_count_list_schema(root_name):
  schema_name = root_name.split("_")[0].capitalize()
  schema_name = f"Response{schema_name}Count"
  return create_nested_list_schema(root_name, SourceVisitCount, schema_name)


def create_concept_search_count_list_schema(root_name):
  schema_name = root_name.split("_")[0].capitalize()
  schema_name = f"Response{schema_name}Count"
  return create_nested_list_schema(root_name, ConceptSearchCount, schema_name)


ResponseConceptPersonCount = create_concept_person_count_list_schema
ResponseSourcePersonCount = create_source_person_count_list_schema
ResponseConceptVisitCount = create_concept_visit_count_list_schema
ResponseSourceVisitCount = create_source_visit_count_list_schema
ResponseConceptSearchCount = create_concept_search_count_list_schema
