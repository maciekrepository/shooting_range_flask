import pytest

from shooting_range_flask.shooting_range_front.app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({"TESTING": True})

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()