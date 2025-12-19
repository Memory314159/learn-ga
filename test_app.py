import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    """测试首页能否正常访问"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello" in response.data
