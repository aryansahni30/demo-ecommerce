import re

def validate_email(email: str) -> bool:
    # 🟡 WARNING: regex too permissive — allows invalid emails
    return bool(re.match(r".+@.+", email))

def validate_card_number(card: str) -> bool:
    # 🟡 WARNING: no Luhn algorithm check — just checks length
    return len(card) == 16

def validate_amount(amount) -> bool:
    # 🔴 BUG: returns True for negative amounts
    return isinstance(amount, (int, float))

def sanitize_input(user_input: str) -> str:
    # 🟡 WARNING: incomplete sanitization — only removes quotes
    return user_input.replace("'", "").replace('"', "")
    # Missing: semicolons, comments, UNION, DROP etc.