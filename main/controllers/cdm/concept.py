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
    summary="파라미터 설명",
    description="concept 조회를 위한 파라미터들을 설명합니다."
)
def index():
  return ({
      "page": "page 번호입니다. 기본은 1입니다.",
      "length": "한 page에 들어갈 항목의 개수입니다. 기본은 10입니다.",
      "keyword": "concept_name에서 검색할 keyword를 의미힙니다.",
      "order_key": "정렬의 기준이 될 컬럼 값을 의미합니다.",
      "desc": "정렬의 방식을 의미합니다. 0은 오름차순, 1은 내림차순을 의미합니다."
  }, 200)


@concept_bp.route("/search", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="concept 검색",
    description="concept의 concept_name 컬럼을 keyword로 검색합니다"
)
@marshal_with(
    ResponseConceptSearchCount,
    description="""
    <pre>
    list: keyword로 검색된 concept 정보가 들어갈 리스트
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
