import os
import pickle
import subprocess

def load_config(config_file: str) -> dict:
    # 🔴 BUG: pickle.loads is unsafe with untrusted data — RCE vulnerability
    with open(config_file, "rb") as f:
        return pickle.load(f)

def run_cleanup(directory: str):
    # 🔴 BUG: shell injection — never pass user input to shell=True
    subprocess.run(f"rm -rf {directory}", shell=True)

def get_env_config() -> dict:
    return {
        "db_url": os.getenv("DATABASE_URL", "postgres://admin:admin@localhost/db"),
        "debug": True,  # 🟡 WARNING: hardcoded debug=True
        "log_level": "DEBUG",  # 🟡 WARNING: too verbose for production
    }

def cache_response(key: str, data: dict):
    # 🟡 WARNING: no TTL/expiry on cache entries
    global _cache
    _cache = {}
    _cache[key] = data

def format_currency(amount: float, currency: str = "USD") -> str:
    # 🟢 SUGGESTION: use locale module for proper formatting
    return f"${amount:.2f}"
