from marshmallow import fields, Schema


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


class ConceptPersonCount(Concept, PersonCount):
  pass


class SourcePersonCount(Source, PersonCount):
  pass


class ConceptVisitCount(Concept, VisitCount):
  pass


class SourceVisitCount(Source, VisitCount):
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


ResponseConceptPersonCount = create_concept_person_count_list_schema
ResponseSourcePersonCount = create_source_person_count_list_schema
ResponseConceptVisitCount = create_concept_visit_count_list_schema
ResponseSourceVisitCount = create_source_visit_count_list_schema
