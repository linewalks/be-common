from sqlalchemy import cast, func, extract, Integer
from main import app, db


# 생각해보니 굳이 Class가 아니어도 될 거 같긴 하다.
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

  @classmethod
  def person_gorup_by_condtion(cls, target_col):
    """
    getattr(cls, target_col) => Person.gender_concept_id
      Person class에서 정의된 컬럼를 사용한다.

    cls.__table__.c[target_col] => person.gender_concept_id
      person.gender_concept_id라는 sql context가 된다.

    Person class 내부에서 컬럼을 사용할 때 여러 조건들을 추가할 수 있으므로
    getattr를 사용하는게 나을 것 같다.
    """
    target_col = getattr(cls, target_col)
    query = db.session.query(
        target_col,
        Concept.concept_name,
        func.count(cls.person_id)
    ).join(
        Concept,
        Concept.concept_id == target_col
    ).group_by(
        target_col,
        Concept.concept_name
    )
    return query

  @classmethod
  def person_group_by_ethnicity(cls):
    query = db.session.query(
        cls.ethnicity_source_value,
        func.count(cls.ethnicity_source_value)
    ).group_by(
        cls.ethnicity_source_value
    )
    return query


class Visit(db.Model):
  """
  방문 수를 확인하기 위한 class

  GET 방문 유형(입원/외래/응급)별 환자 수
  GET 성별 방문 수
  GET 인종별 방문 수
  GET 민족별 방문 수
  GET 방문시 연령대(10세 단위)별 방문 수
  """
  __tablename__ = "visit_occurrence"
  __table_args__ = {"schema": app.config["SCHEMA_SYNTHEA"]}
  __bind_key__ = "synthea"
  visit_occurrence_id = db.Column(db.Integer, primary_key=True)
  person_id = db.Column(db.Integer)
  visit_concept_id = db.Column(db.Integer)
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
  preceding_visit_occurrence_id = db.Column(db.Integer)

  @classmethod
  def visit_gorup_by_visit_type(cls):
    query = db.session.query(
        cls.visit_concept_id,
        Concept.concept_name,
        func.count(cls.visit_occurrence_id)
    ).join(
        Concept,
        Concept.concept_id == cls.visit_concept_id
    ).group_by(
        cls.visit_concept_id,
        Concept.concept_name
    )
    return query

  @classmethod
  def visit_gorup_by_condtion(cls, target_col):
    target_col = getattr(Person, target_col)
    query = db.session.query(
        target_col,
        Concept.concept_name,
        func.count(cls.visit_occurrence_id)
    ).join(
        Person,
        Person.person_id == cls.person_id
    ).join(
        Concept,
        Concept.concept_id == target_col
    ).group_by(
        target_col,
        Concept.concept_name
    )
    return query

  @classmethod
  def visit_group_by_ethnicity(cls):
    query = db.session.query(
        Person.ethnicity_source_value,
        func.count(cls.visit_occurrence_id)
    ).join(
        Person,
        Person.person_id == cls.person_id
    ).group_by(
        Person.ethnicity_source_value
    )
    return query

  @classmethod
  def visit_group_by_age_group(cls):
    age = cast(extract("year", cls.visit_start_date) - extract("year", Person.birth_datetime), Integer)
    age_group = age / 10 * 10
    query = db.session.query(
        age_group,
        func.count(cls.visit_occurrence_id)
    ).join(
        Person,
        Person.person_id == cls.person_id
    ).group_by(
        age_group
    )
    return query


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


class Death(db.Model):
  """
  사망자에 대한 정보를 모아둔 death 테이블과 연결된 class
  """
  __tablename__ = "death"
  __table_args__ = {"schema": app.config["SCHEMA_SYNTHEA"]}
  __bind_key__ = "synthea"
  person_id = db.Column(db.Integer, primary_key=True)
  death_date = db.Column(db.Date)
  death_datetime = db.Column(db.DateTime)
  death_type_concept_id = db.Column(db.Integer)
  cause_concept_id = db.Column(db.Integer)
  cause_source_value = db.Column(db.Integer)
  cause_source_concept_id = db.Column(db.Integer)


class Search():
  """
  각 테이블의 값 조회 class

  with concept_id와 concept_name 매칭
    - concept의 의미를 알 수 있게 이름을 함께 return
  with pagination
  GET 특정 컬럼 검색 기능 - 키워드 검색
  """
  pass
