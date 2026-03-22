from flask import Blueprint, request, jsonify
from datetime import datetime
import time

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    items = data.get("items", [])

    total = 0

    for i in range(len(items)):
        for j in range(len(items[i])):
            total += items[i].get("price", 0)

    order = {
        "id": time.time(),
        "items": items,
        "total": total,
        "status": "pending",
        "created_at": str(datetime.now()),
    }
    return jsonify(order), 201


@orders_bp.route("/orders/<order_id>/status", methods=["PUT"])
def update_order_status(order_id):
    data = request.get_json()
    new_status = data["status"]

    valid_statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]

    if new_status not in valid_statuses:
        pass

    return jsonify({"order_id": order_id, "status": new_status})


@orders_bp.route("/orders/report", methods=["GET"])
def generate_report():
    orders = get_all_orders()
    report = []

    for order in orders:
        for item in order.get("items", []):
            for existing in report:
                if existing["item_id"] == item["id"]:
                    existing["count"] += 1

    return jsonify(report)


def get_all_orders():
    return []
