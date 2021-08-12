from main import app, db


class Person(db.Model):
  """
  환자 수를 조회하기 위한 class

  GET 전체 환자 수
  GET 성별 환자 수
  GET 인종별 환자 수
  GET 민족별 환자 수
  GET 사망 환자 수
  """
  __tablename__ = "person"
  __table_args__ = {"schema": app.config["SCHEMA_SYNTHEA"]}
  __bind_key__ = "synthea"
  person_id = db.Column(db.Integer, primary_key=True)
  gender_concept_id = db.Column(db.Integer)
  year_of_birth = db.Column(db.Integer)
  month_of_birth = db.Column(db.Integer)
  day_of_birth = db.Column(db.Integer)
  birth_datetime = db.Column(db.DateTime)
  race_concept_id = db.Column(db.Integer)
  ethnicity_concept_id = db.Column(db.Integer)
  location_id = db.Column(db.Integer)
  provider_id = db.Column(db.Integer)
  care_site_id = db.Column(db.Integer)
  person_source_value = db.Column(db.String(50))
  gender_source_value = db.Column(db.String(50))
  gender_source_concept_id = db.Column(db.Integer)
  race_source_value = db.Column(db.String(50))
  race_source_concept_id = db.Column(db.Integer)
  ethnicity_source_value = db.Column(db.String(50))
  ethnicity_source_concept_id = db.Column(db.Integer)

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def __repr__(self):
    return f"<Person {self.person_id}>"


class Visit(db.Model):
  """
  방문 수를 확인하기 위한 class

  GET 방문 유형(입원/외래/응급)별 환자 수
  GET 성별 방문 수
  GET 인종별 방문 수
  GET 민족별 방문 수
  GET 방문시 연령대(10세 단위)별 방문 수
  """
  __tablename__ = "visit_occcurence"
  __table_args__ = {"schema": app.config["SCHEMA_SYNTHEA"]}
  __bind_key__ = "synthea"
  visit_occurrence_id = db.Column(db.Integer, primary_key=True)
  person_id = db.Column(db.Integer)
  visit_start_date = db.Column(db.Date)
  visit_start_datetime = db.Column(db.DateTime)
  visit_end_date = db.Column(db.Date)
  visit_end_datetime = db.Column(db.DateTime)
  visit_type_concept_id = db.Column(db.Integer)
  provider_id = db.Column(db.Integer)
  care_site_id = db.Column(db.Integer)
  visit_source_value = db.Column(db.String(50))
  visit_source_concept_id = db.Column(db.Integer)
  admitted_from_concept_id = db.Column(db.Integer)
  admitted_from_source_value = db.Column(db.String(50))
  discharge_to_source_value = db.Column(db.String(50))
  discharge_to_concept_id = db.Column(db.Integer)
  preceding_visit_occurence_id = db.Column(db.Integer)

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def __repr__(self):
    return f"<Visit {self.visit_occurrence_id}>"


class Concept(db.Model):
  """
  각 테이블에 사용된 concept_id를 조회하기 위한 class

  with Pagination
  GET 검색 기능 - 키워드 검색
  Search class의 메소드 사용
  """
  __tablename__ = "concept"
  __table_args__ = {"schema": app.config["SCHEMA_SYNTHEA"]}
  __bind_key__ = "synthea"
  concept_id = db.Column(db.Integer, primary_key=True)
  concept_name = db.Column(db.String(255))
  domain_id = db.Column(db.String(20))
  vocabulary_id = db.Column(db.String(20))
  concept_class_id = db.Column(db.String(20))
  standard_concept = db.Column(db.String(1))
  concept_code = db.Column(db.String(50))
  valid_start_date = db.Column(db.Date)
  valid_end_date = db.Column(db.Date)
  invalid_reason = db.Column(db.String(1))

  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def __repr__(self):
    return f"<Concept {self.concept_id}>"


class Search():
  """
  각 테이블의 값 조회 class

  with concept_id와 concept_name 매칭
    - concept의 의미를 알 수 있게 이름을 함께 return
  with pagination
  GET 특정 컬럼 검색 기능 - 키워드 검색
  """
  pass
