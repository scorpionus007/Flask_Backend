from flask import Blueprint, jsonify, g
from app.middleware.auth import jwt_required, role_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/dashboard", methods=["GET"])
@jwt_required
@role_required("admin")
def dashboard():
    return jsonify({
        "message": f"Welcome to the admin dashboard, {g.current_user}.",
    }), 200
