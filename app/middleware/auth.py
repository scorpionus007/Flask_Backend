from functools import wraps
from flask import request, jsonify, g
import jwt as pyjwt
from app.utils.security import verify_jwt
from app.utils.logger import audit_logger


def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            audit_logger.warning(
                "Unauthorized access attempt | ip=%s | path=%s",
                request.remote_addr,
                request.path,
            )
            return jsonify({"error": "Missing or invalid token"}), 401

        token = auth_header.split(" ", 1)[1]
        try:
            payload = verify_jwt(token)
        except pyjwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except pyjwt.InvalidTokenError:
            audit_logger.warning(
                "Invalid token presented | ip=%s | path=%s",
                request.remote_addr,
                request.path,
            )
            return jsonify({"error": "Invalid token"}), 401

        g.current_user = payload["sub"]
        g.current_role = payload["role"]
        return f(*args, **kwargs)

    return decorated


def role_required(role: str):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if g.get("current_role") != role:
                audit_logger.warning(
                    "Forbidden access attempt | ip=%s | user=%s | required_role=%s",
                    request.remote_addr,
                    g.get("current_user", "unknown"),
                    role,
                )
                return jsonify({"error": "Insufficient permissions"}), 403
            return f(*args, **kwargs)

        return decorated

    return decorator
