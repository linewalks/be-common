from flask import Blueprint
from flask_apispec import doc, marshal_with, use_kwargs
from main.models.cdm_data import (
    Search,
    Person,
    Visit,
    Drug,
    Condition,
    Death
)
from main.models.utils import convert_query_to_response
from main.schema.cdm_schema import (
    RequestTableSearch,
    ResponseConceptSearchCount
)

search_bp = Blueprint("search", __name__, url_prefix="/search")

API_CATEGORY = "Search"


@search_bp.route("/index", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="테이블 설명",
    description="조회가 가능한 테이블들을 설명합니다."
)
def index():
  return ({
      "person": {
          "description": "person 테이블을 검색합니다.",
          "target_column": ["gender", "race"]
      },
      "visit": {
          "description": "visit_occurrence 테이블을 검색합니다.",
          "target_column": ["visit", "visit-type"]
      },
      "condition": {
          "description": "condition_occurrence 테이블을 검색합니다.",
          "target_column": ["condition", "condition-type"]
      },
      "drug": {
          "description": "drug_exposure 테이블을 검색합니다.",
          "target_column": ["drug", "drug-type"]
      },
      "death": {
          "description": "death 테이블을 검색합니다.",
          "target_column": ["death-type"]
      }
  }, 200)


@search_bp.route("/person", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="person 테이블 검색",
    description="person 테이블의 target_column을 keyword로 검색합니다"
)
@marshal_with(
    ResponseConceptSearchCount,
    description="""
    <pre>
    list: keyword로 검색된 테이블 정보가 들어갈 리스트
    </pre>
    """
)
@use_kwargs(
    RequestTableSearch,
    location="query"
)
def person_keyword_search(page, length, target_column, keyword, order_key, desc):
  query = Search.target_column_search(
      table=Person,
      target_col=f"{target_column}_concept_id",
      keyword=keyword,
      order_key=order_key,
      desc=desc
  ).slice((page - 1) * length, page * length)
  return {
      "list": convert_query_to_response(
          (
              "concept_id",
              "concept_name",
              "row_count"
          ),
          query.all(),
          Person
      ),
      "target_column": target_column,
      "keyword": keyword,
      "page": page,
      "order_key": order_key,
      "desc": desc
  }


@search_bp.route("/visit", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="visit 테이블 검색",
    description="visit 테이블의 target_column을 keyword로 검색합니다"
)
@marshal_with(
    ResponseConceptSearchCount,
    description="""
    <pre>
    list: keyword로 검색된 테이블 정보가 들어갈 리스트
    </pre>
    """
)
@use_kwargs(
    RequestTableSearch,
    location="query"
)
def visit_keyword_search(page, length, target_column, keyword, order_key, desc):
  query = Search.target_column_search(
      table=Visit,
      target_col=f"{target_column}_concept_id",
      keyword=keyword,
      order_key=order_key,
      desc=desc
  ).slice((page - 1) * length, page * length)
  return {
      "list": convert_query_to_response(
          (
              "concept_id",
              "concept_name",
              "row_count"
          ),
          query.all(),
          Visit
      ),
      "target_column": target_column,
      "keyword": keyword,
      "page": page,
      "order_key": order_key,
      "desc": desc
  }


@search_bp.route("/condition", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="condition 테이블 검색",
    description="condition 테이블의 target_column을 keyword로 검색합니다"
)
@marshal_with(
    ResponseConceptSearchCount,
    description="""
    <pre>
    list: keyword로 검색된 테이블 정보가 들어갈 리스트
    </pre>
    """
)
@use_kwargs(
    RequestTableSearch,
    location="query"
)
def condition_keyword_search(page, length, target_column, keyword, order_key, desc):
  query = Search.target_column_search(
      table=Condition,
      target_col=f"{target_column}_concept_id",
      keyword=keyword,
      order_key=order_key,
      desc=desc
  ).slice((page - 1) * length, page * length)
  return {
      "list": convert_query_to_response(
          (
              "concept_id",
              "concept_name",
              "row_count"
          ),
          query.all(),
          Condition
      ),
      "target_column": target_column,
      "keyword": keyword,
      "page": page,
      "order_key": order_key,
      "desc": desc
  }


@search_bp.route("/drug", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="drug 테이블 검색",
    description="drug 테이블의 target_column을 keyword로 검색합니다"
)
@marshal_with(
    ResponseConceptSearchCount,
    description="""
    <pre>
    list: keyword로 검색된 테이블 정보가 들어갈 리스트
    </pre>
    """
)
@use_kwargs(
    RequestTableSearch,
    location="query"
)
def drug_keyword_search(page, length, target_column, keyword, order_key, desc):
  query = Search.target_column_search(
      table=Drug,
      target_col=f"{target_column}_concept_id",
      keyword=keyword,
      order_key=order_key,
      desc=desc
  ).slice((page - 1) * length, page * length)
  return {
      "list": convert_query_to_response(
          (
              "concept_id",
              "concept_name",
              "row_count"
          ),
          query.all(),
          Drug
      ),
      "target_column": target_column,
      "keyword": keyword,
      "page": page,
      "order_key": order_key,
      "desc": desc
  }


@search_bp.route("/death", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="death 테이블 검색",
    description="death 테이블의 target_column을 keyword로 검색합니다"
)
@marshal_with(
    ResponseConceptSearchCount,
    description="""
    <pre>
    list: keyword로 검색된 테이블 정보가 들어갈 리스트
    </pre>
    """
)
@use_kwargs(
    RequestTableSearch,
    location="query"
)
def death_keyword_search(page, length, target_column, keyword, order_key, desc):
  query = Search.target_column_search(
      table=Death,
      target_col=f"{target_column}_concept_id",
      keyword=keyword,
      order_key=order_key,
      desc=desc
  ).slice((page - 1) * length, page * length)
  return {
      "list": convert_query_to_response(
          (
              "concept_id",
              "concept_name",
              "row_count"
          ),
          query.all(),
          Death
      ),
      "target_column": target_column,
      "keyword": keyword,
      "page": page,
      "order_key": order_key,
      "desc": desc
  }
