import os
from datetime import datetime, timedelta, timezone

import jwt
from flask import Flask, request, jsonify

app = Flask(__name__)

secret = os.environ.get("JWT_SECRET")

if not secret:
    raise ValueError("JWT_SECRET puudub!")


users = {
    "student": {"password": "student123", "role": "student"},
    "admin": {"password": "admin123", "role": "admin"}
}


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if username not in users or users[username]["password"] != password:
        return jsonify({"error": "Vale kasutajanimi või parool"}), 401

    token = jwt.encode({
        "sub": username,
        "role": users[username]["role"],
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5)
    }, secret, algorithm="HS256")

    return jsonify({"token": token}), 200


def check_token():
    auth = request.headers.get("Authorization")

    if not auth or not auth.startswith("Bearer "):
        return None

    token = auth.split(" ")[1]

    try:
        data = jwt.decode(token, secret, algorithms=["HS256"])
        return data
    except jwt.InvalidTokenError:
        return None


@app.route("/profiil", methods=["GET"])
def profiil():
    data = check_token()

    if data is None:
        return jsonify({"error": "Kehtetu token"}), 401

    return jsonify(data), 200


@app.route("/admin", methods=["GET"])
def admin():
    data = check_token()

    if data is None:
        return jsonify({"error": "Kehtetu token"}), 401

    if data["role"] != "admin":
        return jsonify({"error": "Ligipääs keelatud"}), 403

    return jsonify({"message": "Admini ligipääs lubatud"}), 200


if __name__ == "__main__":
    app.run(debug=True)