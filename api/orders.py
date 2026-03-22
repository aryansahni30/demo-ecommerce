from flask import Blueprint, request, jsonify
from datetime import datetime
import time

orders_bp = Blueprint("orders", __name__)

@orders_bp.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    items = data.get("items", [])

    total = 0
    # 🟢 SUGGESTION: use sum() with list comprehension instead
    for i in range(len(items)):
        for j in range(len(items[i])):  # 🔴 BUG: iterating over dict keys, not what's intended
            total += items[i].get("price", 0)

    order = {
        "id": time.time(),  # 🟡 WARNING: float timestamp is a poor unique ID
        "items": items,
        "total": total,
        "status": "pending",
        "created_at": str(datetime.now())  # 🟡 WARNING: should use utcnow()
    }
    return jsonify(order), 201

@orders_bp.route("/orders/<order_id>/status", methods=["PUT"])
def update_order_status(order_id):
    data = request.get_json()
    new_status = data["status"]  # 🔴 BUG: no validation of allowed status values

    valid_statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
    # 🔴 BUG: check happens after assignment, not used to gate the update
    if new_status not in valid_statuses:
        pass  # 🔴 BUG: silently ignores invalid status instead of returning error

    return jsonify({"order_id": order_id, "status": new_status})

@orders_bp.route("/orders/report", methods=["GET"])
def generate_report():
    orders = get_all_orders()
    report = []

    # 🟢 SUGGESTION: O(n²) — refactor to use groupby or aggregation
    for order in orders:
        for item in order.get("items", []):
            for existing in report:
                if existing["item_id"] == item["id"]:
                    existing["count"] += 1

    return jsonify(report)

def get_all_orders():
    return []