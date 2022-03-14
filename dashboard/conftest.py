import pytest
from settings import app as create_app

@pytest.fixture
def app():
    yield_app = create_app()
    yield yield_app

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
