from flask import Blueprint
from flask_apispec import doc, marshal_with, use_kwargs
from main.models.cdm_data import Concept
from main.models.utils import convert_query_to_response
from main.schema.cdm_schema import (
    RequestSearch,
    ResponseConceptSearchCount
)

concept_bp = Blueprint("concept", __name__, url_prefix="/concept")

API_CATEGORY = "Concept"


@concept_bp.route("/index", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="컬럼 설명",
    description="concept 조회를 위한 keyword를 설명합니다."
)
def index():
  return ({
      "gender": "person 테이블의 concept",
      "race": "person 테이블의 concept",
      "visit": "visit_occurrence 테이블의 concept",
      "visit_type": "visit_occurrence 테이블의 concept",
      "condition": "condition_occurrence 테이블의 concept",
      "condition_type": "condition_occurrence 테이블의 concept",
      "drug": "drug_exposure 테이블의 concept",
      "drug_type": "drug_exposure 테이블의 concept",
      "death_type": "death 테이블의 concept",
      "page": "page index, default=1",
      "page_cnt": "한 page에 들어갈 항목의 개수, default=10"
  }, 200)


@concept_bp.route("/search", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="concept 검색",
    description="keyword로 concept를 검색합니다"
)
@marshal_with(
    ResponseConceptSearchCount("concept_list"),
    description="""
    <pre>
    concept_list: concept 정보가 들어갈 리스트
      .concept_id: Concept ID
      .concept_name: Concept 이름
      .row_count: 해당 concept가 사용된 row 수
    </pre>
    """
)
@use_kwargs(
    RequestSearch,
    location="query"
)
def concept_keyword_search(**kwargs):
  page = kwargs.get("page", 1)
  page_cnt = kwargs.get("page_cnt", 10)
  keyword = kwargs.get("keyword", "gender")
  query = Concept.get_top_concept_by_keyword(keyword, page, page_cnt)

  return {
      "concept_list": convert_query_to_response(
          ("concept_id", "concept_name", "row_count"),
          query.all()
      )
  }
