import pytest
from app import app, db


@pytest.fixture
def client():
    # 配置测试环境使用内存数据库
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_health(client):
    rv = client.get("/")
    assert rv.status_code == 200


def test_create_and_get_user(client):
    # 1. 创建用户
    rv = client.post("/users", json={"username": "testuser", "email": "test@example.com"})
    assert rv.status_code == 201

    # 2. 获取用户列表
    rv = client.get("/users")
    json_data = rv.get_json()
    assert len(json_data) == 1
    assert json_data[0]["username"] == "testuser"
