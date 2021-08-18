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
    ResponseConceptSearchCount,
    description="""
    <pre>
    concept_list: concept 정보가 들어갈 리스트
    </pre>
    """
)
@use_kwargs(
    RequestSearch,
    location="query"
)
def concept_keyword_search(page, length, keyword, order_key, desc):
  query = Concept.get_top_concept_by_keyword(
      keyword=keyword, 
      order_key=order_key,
      desc=desc,
      page=page,
      length=length
  )
  return {
      "list": convert_query_to_response(
          (
              "concept_id",
              "concept_name",
              "domain_id",
              "vocabulary_id",
              "concept_class_id",
              "standard_concept"
          ),
          query.all(),
          Concept
      ),
      "keyword": keyword,
      "page": page,
      "order_key": order_key,
      "desc": desc
  }
