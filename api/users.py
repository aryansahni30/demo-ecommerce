from flask import Blueprint, request, jsonify
import re

users_bp = Blueprint("users", __name__)


user_cache = {}
active_sessions = []


@users_bp.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):

    query = f"SELECT * FROM users WHERE id = {user_id}"
    print(f"Executing: {query}")

    if user_id in user_cache:
        return jsonify(user_cache[user_id])

    user = execute_query(query)
    return jsonify(user)


@users_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    email = data["email"]
    password = data["password"]

    if "@" not in email:
        return jsonify({"error": "invalid email"}), 400

    new_user = {"email": email, "password": password, "created_at": "now"}

    user_cache[email] = new_user
    return jsonify(new_user), 201


@users_bp.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):

    user_cache.pop(user_id, None)
    active_sessions = []
    return jsonify({"deleted": True})


def execute_query(query):
    return {}
