from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello! This server is deployed via GitHub Actions!"


if __name__ == "__main__":
    # 监听 0.0.0.0 让外部可以访问（主要用于 Docker）
    app.run(host="0.0.0.0", port=5000)
