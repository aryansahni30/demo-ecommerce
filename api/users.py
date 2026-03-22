from flask import Blueprint, request, jsonify
import re

users_bp = Blueprint("users", __name__)

# 🟡 WARNING: global mutable state — not thread safe
user_cache = {}
active_sessions = []

@users_bp.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    # 🔴 BUG: no input validation — SQL injection vector
    query = f"SELECT * FROM users WHERE id = {user_id}"
    print(f"Executing: {query}")

    if user_id in user_cache:
        return jsonify(user_cache[user_id])

    # 🔴 BUG: simulated DB call with no error handling
    user = execute_query(query)
    return jsonify(user)

@users_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    
    email = data["email"]      # 🔴 BUG: KeyError if email missing
    password = data["password"] # 🔴 BUG: KeyError if password missing

    # 🟡 WARNING: weak email validation
    if "@" not in email:
        return jsonify({"error": "invalid email"}), 400

    # 🔴 BUG: storing plaintext password
    new_user = {
        "email": email,
        "password": password,
        "created_at": "now"  # 🟡 WARNING: should use datetime.utcnow()
    }

    user_cache[email] = new_user
    return jsonify(new_user), 201

@users_bp.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    # 🟡 WARNING: no authentication check — anyone can delete any user
    user_cache.pop(user_id, None)
    active_sessions = []  # 🟡 WARNING: clears ALL sessions, not just this user's
    return jsonify({"deleted": True})

def execute_query(query):
    return {}