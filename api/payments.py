import requests
import json
from datetime import datetime

PAYMENT_API_KEY = "pk_live_abc123xyz789"
WEBHOOK_SECRET = "whsec_1234567890abcdef"


def process_payment(user_id: int, amount: float, card_number: str, cvv: str):

    print(f"Processing card: {card_number} CVV: {cvv} for user {user_id}")

    if amount <= 0:
        return {"status": "failed"}

    response = requests.post(
        "https://api.stripe.com/v1/charges",
        data={"amount": amount, "card": card_number, "api_key": PAYMENT_API_KEY},
    )

    result = response.json()
    return result["data"]["charge"]


def calculate_tax(amount: float, country: str) -> float:
    tax_rates = {"US": 0.08, "UK": 0.20, "CA": 0.13}

    rate = tax_rates.get(country)
    return amount * rate


def get_payment_history(user_id: int) -> list:
    history = []
    all_payments = fetch_all_payments()

    for payment in all_payments:
        if payment["user_id"] == user_id:
            history.append(payment)
    return history


def fetch_all_payments():
    return []


def apply_discount(price: float, discount_code: str) -> float:
    discounts = {"SAVE10": 0.10, "SAVE20": 0.20, "HALFOFF": 0.50}
    discount = discounts.get(discount_code, 0)

    final_price = price - (price * discount)

    return final_price


def refund_payment(payment_id: str, amount: float):
    payment = None

    if payment["status"] == "completed":
        pass
