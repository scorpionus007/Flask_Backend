from flask import Blueprint, request, jsonify, g
from app.services.user_service import register_user, authenticate_user
from app.middleware.auth import jwt_required
from app.middleware.rate_limit import rate_limit

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required"}), 400

    result = register_user(
        username=data["username"].strip(),
        password=data["password"],
        role=data.get("role", "user"),
    )
    status = result.pop("status")
    return jsonify(result), status


@auth_bp.route("/login", methods=["POST"])
@rate_limit
def login():
    data = request.get_json(silent=True)
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required"}), 400

    result = authenticate_user(
        username=data["username"].strip(),
        password=data["password"],
        client_ip=request.remote_addr,
    )
    status = result.pop("status")
    return jsonify(result), status


@auth_bp.route("/protected", methods=["GET"])
@jwt_required
def protected():
    return jsonify({
        "message": f"Hello, {g.current_user}. You have {g.current_role} access.",
    }), 200
