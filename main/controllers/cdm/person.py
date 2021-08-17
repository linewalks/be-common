from flask import Blueprint
from flask_apispec import doc, marshal_with
from main import db
from main.schema.cdm_schema import (
    PersonCount,
    ResponseConceptPersonCount,
    ResponseSourcePersonCount
)
from main.models.cdm_data import Death, Person
from main.models.utils import convert_query_to_response

person_bp = Blueprint("person", __name__, url_prefix="/person")

API_CATEGORY = "Person"


@person_bp.route("/index", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="컬럼 설명",
    description="환자 수 조회를 위한 파라미터를 설명합니다."
)
def index():
  return ({
      "all": "모든 환자 수",
      "gender": "성별 환자 수",
      "race": "인종별 환자 수",
      "ethnicity": "민족별 환자 수",
      "death": "사망 환자 수"
  }, 200)


@person_bp.route("/all", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="전체 환자 수 조회",
    description="전체 환자 수를 조회합니다."
)
@marshal_with(
    PersonCount,
    description="""
    <pre>
    person_count: 전체 환자 수
    </pre>
    """
)
def all_count():
  return {
      "person_count": db.session.query(Person).count()
  }


@person_bp.route("/gender", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="성별 환자 수 조회",
    description="성별 환자 수를 조회합니다."
)
@marshal_with(
    ResponseConceptPersonCount("person_list"),
    description="""
    <pre>
    person_list: 환자 수 정보가 들어갈 리스트
      .concept_id: 성별 Concept ID
      .concept_name: 성별 Concept 이름
      .person_count: 환자 수
    </pre>
    """
)
def gender_count():
  query = Person.person_gorup_by_condtion("gender_concept_id")
  return {
      "person_list": convert_query_to_response(
          ("concept_id", "concept_name", "person_count"),
          query.all()
      )
  }


@person_bp.route("/race", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="인종별 환자 수 조회",
    description="인종별 환자 수를 조회합니다."
)
@marshal_with(
    ResponseConceptPersonCount("person_list"),
    description="""
    <pre>
    person_list: 환자 수 정보가 들어갈 리스트
      .concept_id: 인종별 Concept ID
      .concept_name: 인종별 Concept 이름
      .person_count: 환자 수
    </pre>
    """
)
def race_count():
  query = Person.person_gorup_by_condtion("race_concept_id")
  return {
      "person_list": convert_query_to_response(
          ("concept_id", "concept_name", "person_count"),
          query.all()
      )
  }


@person_bp.route("/ethnicity", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="민족별 환자 수 조회",
    description="민족별 환자 수를 조회합니다."
)
@marshal_with(
    ResponseSourcePersonCount("person_list"),
    description="""
    <pre>
    person_list: 환자 수 정보가 들어갈 리스트
      .source_value: 민족별 Source Value
      .person_count: 환자 수
    </pre>
    """
)
def ethnicity_count():
  """
  ethnicitiy_concept_id의 모든 값이 0이다.
  concept 테이블을 조회하니 유효하지 않는 값이라고 나온다.
  부득이하게 대체 값인 ethnicity_source_value를 사용한다.
  """
  query = Person.person_group_by_ethnicity()
  return {
      "person_list": convert_query_to_response(
          ("source_value", "person_count"),
          query.all()
      )
  }


@person_bp.route("/death", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="사망 환자 수 조회",
    description="사망 환자 수를 조회합니다."
)
@marshal_with(
    PersonCount,
    description="""
    <pre>
    person_count: 사망 환자 수
    </pre>
    """
)
def death_count():
  return {
      "person_count": db.session.query(Death).count()
  }
