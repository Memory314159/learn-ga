import os
from flask import Flask, request, jsonify
from models import db, User

app = Flask(__name__)

# --- 配置部分 ---
# Render 会自动提供 DATABASE_URL 环境变量
database_url = os.environ.get("DATABASE_URL")

if database_url:
    # 修正 Render 提供的 Postgres URL 格式 (postgres:// -> postgresql://)
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    # 本地开发或测试使用 SQLite
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///local.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 初始化数据库
db.init_app(app)

# 每次启动前尝试创建表 (生产环境通常用 Migration 工具，这里为了演示简化)
with app.app_context():
    db.create_all()

# --- API 路由 ---


@app.route("/")
def health_check():
    return jsonify({"status": "healthy", "db": app.config["SQLALCHEMY_DATABASE_URI"].split(":")[0]})


@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    new_user = User(username=data["username"], email=data["email"])
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


if __name__ == "__main__":
    app.run(debug=True)
