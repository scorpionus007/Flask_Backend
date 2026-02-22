import time
from functools import wraps
from flask import request, jsonify
from app.config import Config
from app.extensions import rate_limit_store
from app.utils.logger import audit_logger


def rate_limit(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        client_ip = request.remote_addr
        now = time.time()
        window = Config.RATE_LIMIT_WINDOW_SECONDS

        if client_ip not in rate_limit_store:
            rate_limit_store[client_ip] = []

        rate_limit_store[client_ip] = [
            ts for ts in rate_limit_store[client_ip] if now - ts < window
        ]

        if len(rate_limit_store[client_ip]) >= Config.RATE_LIMIT_MAX_REQUESTS:
            audit_logger.warning(
                "Rate limit exceeded | ip=%s | path=%s",
                client_ip,
                request.path,
            )
            return jsonify({"error": "Too many requests, try again later"}), 429

        rate_limit_store[client_ip].append(now)
        return f(*args, **kwargs)

    return decorated
