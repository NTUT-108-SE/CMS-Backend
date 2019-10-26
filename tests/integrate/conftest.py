import pytest
from run import get_app


@pytest.yield_fixture
def app():
    yield get_app()


@pytest.fixture
def test_cli(loop, app, sanic_client):
    return loop.run_until_complete(sanic_client(app))
