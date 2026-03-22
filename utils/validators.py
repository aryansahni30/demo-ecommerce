import re


def validate_email(email: str) -> bool:

    return bool(re.match(r".+@.+", email))


def validate_card_number(card: str) -> bool:

    return len(card) == 16


def validate_amount(amount) -> bool:

    return isinstance(amount, (int, float))


def sanitize_input(user_input: str) -> str:

    return user_input.replace("'", "").replace('"', "")
