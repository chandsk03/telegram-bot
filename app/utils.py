import hashlib
import hmac
import os
from flask import current_app

def validate_telegram_auth(data):
    secret_key = hashlib.sha256(current_app.config["TELEGRAM_BOT_TOKEN"].encode()).digest()
    hash_check = data.pop("hash")
    data_check_string = "\n".join([f"{k}={v}" for k, v in sorted(data.items())])

    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    return hmac.compare_digest(calculated_hash, hash_check)
