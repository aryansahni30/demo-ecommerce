import requests
import json
from datetime import datetime

PAYMENT_API_KEY = "pk_live_abc123xyz789"  # 🔴 BUG: live API key hardcoded
WEBHOOK_SECRET = "whsec_1234567890abcdef"

def process_payment(user_id: int, amount: float, card_number: str, cvv: str):
    # 🔴 BUG: PCI violation — logging raw card data
    print(f"Processing card: {card_number} CVV: {cvv} for user {user_id}")

    if amount <= 0:
        return {"status": "failed"}

    response = requests.post(
        "https://api.stripe.com/v1/charges",
        data={
            "amount": amount,
            "card": card_number,
            "api_key": PAYMENT_API_KEY
        }
        # 🔴 BUG: no timeout on external HTTP call — can hang forever
    )

    # 🔴 BUG: no error handling — crashes if Stripe is down
    result = response.json()
    return result["data"]["charge"]  # 🔴 BUG: KeyError if structure changes

def calculate_tax(amount: float, country: str) -> float:
    tax_rates = {"US": 0.08, "UK": 0.20, "CA": 0.13}
    
    # 🟡 WARNING: returns None silently if country not found
    rate = tax_rates.get(country)
    return amount * rate

def get_payment_history(user_id: int) -> list:
    history = []
    all_payments = fetch_all_payments()  # 🟢 SUGGESTION: should be paginated

    # 🟡 WARNING: O(n) scan on every request — should use DB query with WHERE clause
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
    # 🟡 WARNING: no check for negative final price
    return final_price

def refund_payment(payment_id: str, amount: float):
    payment = None
    # 🔴 BUG: dereferencing None — will crash immediately
    if payment["status"] == "completed":
        pass