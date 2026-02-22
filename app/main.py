import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from flask import Flask
from app.config import Config
from app.routes.auth import auth_bp
from app.routes.admin import admin_bp
from app.utils.errors import register_error_handlers
from app.utils.logger import audit_logger


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    register_error_handlers(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    audit_logger.info("Application started | pid=%d", os.getpid())
    return app


if __name__ == "__main__":
    app = create_app()
    host = os.getenv("FLASK_HOST", "127.0.0.1")
    app.run(host=host, port=5000, debug=False)
