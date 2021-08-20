import pytest


@pytest.fixture(scope="session")
def app():
  from main import create_app
  return create_app()


@pytest.fixture(scope="module")
def app_context(app):
  with app.app_context():
    app.config["TESTING"] = True
    yield app


@pytest.fixture
def client(app_context):
  return app_context.test_client()
