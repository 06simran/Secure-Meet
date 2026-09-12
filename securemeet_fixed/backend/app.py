"""
SecureMeet — Flask Application Factory
"""

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

from services.db_service import init_db
from routes.auth_routes import auth_bp
from routes.meeting_routes import meeting_bp
from routes.moderation_routes import moderation_bp


def create_app():
    app = Flask(__name__)

    MYSQL_HOST = os.environ.get("MYSQL_HOST", "mysql")
    MYSQL_PORT = os.environ.get("MYSQL_PORT", "3306")
    MYSQL_USER = os.environ.get("MYSQL_USER", "securemeet_user")
    MYSQL_PASS = os.environ.get("MYSQL_PASSWORD", "securemeet2025")
    MYSQL_DB   = os.environ.get("MYSQL_DATABASE", "securemeet")

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    app.config["JWT_SECRET_KEY"] = os.environ.get(
        "JWT_SECRET_KEY", "securemeet-dev-secret"
    )
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    JWTManager(app)
    init_db(app)

    app.register_blueprint(auth_bp,       url_prefix="/api/auth")
    app.register_blueprint(meeting_bp,    url_prefix="/api/meetings")
    app.register_blueprint(moderation_bp, url_prefix="/api/moderation")

    @app.route("/api/health")
    def health():
        return jsonify({"status": "ok", "service": "SecureMeet API"})

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
