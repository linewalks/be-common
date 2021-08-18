from flask import Blueprint
from flask_apispec import doc, marshal_with
from main import db
from main.models.cdm_data import Visit
from main.models.utils import convert_query_to_response
from main.schema.cdm_schema import (
    VisitCount,
    ResponseConceptVisitCount,
    ResponseSourceVisitCount
)

visit_bp = Blueprint("visit", __name__, url_prefix="/visit")

API_CATEGORY = "Visit"


@visit_bp.route("/index", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="컬럼 설명",
    description="방문 수 조회를 위한 파라미터를 설명합니다."
)
def index():
  return ({
      "all": "모든 방문 수",
      "visit-type": "방문 유형(입원/외래/응급)별 방문 수",
      "gender": "성별 방문 수",
      "race": "인종별 방문 수",
      "ethnicity": "민족별 방문 수",
      "age-group": "방문시 연령대(10세 단위)별 방문 수"
  }, 200)


@visit_bp.route("/all", methods=["GET"])
@marshal_with(
    VisitCount,
    description="""
    <pre>
    visit_count: 전체 방문 수
    </pre>
    """
)
@doc(
    tags=[API_CATEGORY],
    summary="전체 방문 수 조회",
    description="전체 방문 수를 조회합니다."
)
def all_count():
  return {
      "visit_count": db.session.query(Visit).count()
  }


@visit_bp.route("/visit-type", methods=["GET"])
@marshal_with(
    ResponseConceptVisitCount,
    description="""
    <pre>
    visit_list: 방문 수 정보가 들어갈 리스트
      .concept_id: 방문 유형 Concept ID
      .concept_name: 방문 유형 Concept 이름
      .visit_count: 방문 수
    </pre>
    """
)
@doc(
    tags=[API_CATEGORY],
    summary="방문 유형(입원/외래/응급)별 방문 수 조회",
    description="방문 유형(입원/외래/응급)별 방문 수를 조회합니다."
)
def visit_type_count():
  query = Visit.visit_gorup_by_visit_type()
  return {
      "visit_list": convert_query_to_response(
          ("concept_id", "concept_name", "visit_count"),
          query.all()
      )
  }


@visit_bp.route("/gender", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="성별 방문 수 조회",
    description="성별 방문 수를 조회합니다."
)
@marshal_with(
    ResponseConceptVisitCount,
    description="""
    <pre>
    visit_list: 방문 수 정보가 들어갈 리스트
      .concept_id: 성별 Concept ID
      .concept_name: 성별 Concept 이름
      .visit_count: 방문 수
    </pre>
    """
)
def gender_count():
  query = Visit.visit_gorup_by_condtion("gender_concept_id")
  return {
      "visit_list": convert_query_to_response(
          ("concept_id", "concept_name", "visit_count"),
          query.all()
      )
  }


@visit_bp.route("/race", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="인종별 방문 수 조회",
    description="인종별 방문 수를 조회합니다."
)
@marshal_with(
    ResponseConceptVisitCount,
    description="""
    <pre>
    visit_list: 방문 수 정보가 들어갈 리스트
      .concept_id: 인종별 Concept ID
      .concept_name: 인종별 Concept 이름
      .visit_count: 방문 수
    </pre>
    """
)
def race_count():
  query = Visit.visit_gorup_by_condtion("race_concept_id")
  return {
      "visit_list": convert_query_to_response(
          ("concept_id", "concept_name", "visit_count"),
          query.all()
      )
  }


@visit_bp.route("/ethnicity", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="민족별 방문 수 조회",
    description="민족별 방문 수를 조회합니다."
)
@marshal_with(
    ResponseSourceVisitCount,
    description="""
    <pre>
    visit_list: 방문 수 정보가 들어갈 리스트
      .source_value: 민족별 Source Value
      .visit_count: 방문 수
    </pre>
    """
)
def ethnicity_count():
  """
  ethnicitiy_concept_id의 모든 값이 0이다.
  concept 테이블을 조회하니 유효하지 않는 값이라고 나온다.
  부득이하게 대체 값인 ethnicity_source_value를 사용한다.
  """
  query = Visit.visit_group_by_ethnicity()
  return {
      "visit_list": convert_query_to_response(
          ("source_value", "visit_count"),
          query.all()
      )
  }


@visit_bp.route("/age-group", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="방문시 연령대(10세 단위)별 방문 수 조회",
    description="방문시 연령대(10세 단위)별 방문 수를 조회합니다."
)
@marshal_with(
    ResponseSourceVisitCount,
    description="""
    <pre>
    visit_list: 방문 수 정보가 들어갈 리스트
      .source_value: 방문시 연령대(10세 단위)
      .visit_count: 방문 수
    </pre>
    """
)
def age_group_count():
  query = Visit.visit_group_by_age_group()
  return {
      "visit_list": convert_query_to_response(
          ("source_value", "visit_count"),
          query.all()
      )
  }
