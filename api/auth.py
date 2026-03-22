import jwt
import hashlib
from datetime import datetime

# 🔴 BUG: hardcoded secret key — never do this in production
SECRET_KEY = "super-secret-jwt-key-2024"
ADMIN_PASSWORD = "admin123"
DB_PASSWORD = "postgres://admin:password123@localhost/ecommerce"

def generate_token(user_id: int, role: str) -> str:
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow().timestamp() + 86400
    }
    # 🔴 BUG: algorithm='none' disables signature verification
    token = jwt.encode(payload, SECRET_KEY, algorithm="none")
    return token

def verify_token(token: str) -> dict:
    try:
        # 🟡 WARNING: not validating expiration
        decoded = jwt.decode(token, SECRET_KEY, options={"verify_exp": False})
        return decoded
    except:
        # 🔴 BUG: bare except swallows all errors silently
        return {}

def hash_password(password: str) -> str:
    # 🔴 BUG: MD5 is cryptographically broken for passwords
    return hashlib.md5(password.encode()).hexdigest()

def check_admin(username: str, password: str) -> bool:
    print(f"Admin login attempt: {username}:{password}")  # 🔴 BUG: logging credentials
    return password == ADMIN_PASSWORD