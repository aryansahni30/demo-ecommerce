import os
import pickle
import subprocess


def load_config(config_file: str) -> dict:

    with open(config_file, "rb") as f:
        return pickle.load(f)


def run_cleanup(directory: str):

    subprocess.run(f"rm -rf {directory}", shell=True)


def get_env_config() -> dict:
    return {
        "db_url": os.getenv("DATABASE_URL", "postgres://admin:admin@localhost/db"),
        "debug": True,
        "log_level": "DEBUG",
    }


def cache_response(key: str, data: dict):

    global _cache
    _cache = {}
    _cache[key] = data


def format_currency(amount: float, currency: str = "USD") -> str:

    return f"${amount:.2f}"
