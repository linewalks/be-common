import pytest
from tests.helpers import (
    to_json,
    _test_get_status_code
)
from main.schema.cdm_schema import (
    PersonCount,
    ResponseConceptPersonCount,
    ResponseSourcePersonCount,
    VisitCount,
    ResponseConceptVisitCount,
    ResponseSourceVisitCount,
    RequestSearch,
    ResponseConceptSearchCount
)


def test_client(client):
  assert client is not None


# person
def test_person_all(client):
  url = '/person/all'
  _test_get_status_code(
      client=client,
      status_code=200,
      url=url,
      schema=PersonCount()
  )


def test_person_gender(client):
  url = '/person/gender'
  _test_get_status_code(
      client=client,
      status_code=200,
      url=url,
      schema=ResponseConceptPersonCount()
  )


def test_person_race(client):
  url = '/person/race'
  _test_get_status_code(
      client=client,
      status_code=200,
      url=url,
      schema=ResponseConceptPersonCount()
  )


def test_person_ethnicity(client):
  url = '/person/ethnicity'
  _test_get_status_code(
      client=client,
      status_code=200,
      url=url,
      schema=ResponseSourcePersonCount()
  )


def test_person_death(client):
  url = '/person/death'
  _test_get_status_code(
      client=client,
      status_code=200,
      url=url,
      schema=PersonCount()
  )


# visit
def test_visit_all(client):
  url = '/visit/all'
  _test_get_status_code(
      client=client,
      status_code=200,
      url=url,
      schema=VisitCount()
  )


def test_visit_visit_type(client):
  url = '/visit/visit-type'
  _test_get_status_code(
      client=client,
      status_code=200,
      url=url,
      schema=ResponseConceptVisitCount()
  )


def test_visit_gender(client):
  url = '/visit/gender'
  _test_get_status_code(
      client=client,
      status_code=200,
      url=url,
      schema=ResponseConceptVisitCount()
  )


def test_visit_race(client):
  url = '/visit/race'
  _test_get_status_code(
      client=client,
      status_code=200,
      url=url,
      schema=ResponseConceptVisitCount()
  )


def test_visit_ethnicity(client):
  url = '/visit/ethnicity'
  _test_get_status_code(
      client=client,
      status_code=200,
      url=url,
      schema=ResponseSourceVisitCount()
  )


def test_visit_age_group(client):
  url = '/visit/age-group'
  _test_get_status_code(
      client=client,
      status_code=200,
      url=url,
      schema=ResponseSourceVisitCount()
  )


def test_concept_search(client):
  url = '/concept/search'
  query = {
      "page": "1",
      "length": "10",
      "keyword": "aspirin",
      "order_key": "concept_id",
      "desc": "0"
  }
  _test_get_status_code(
      client=client,
      status_code=200,
      url=url,
      query_string=query,
      schema=ResponseConceptSearchCount()
  )
