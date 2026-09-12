"""
Authentication Routes — /api/auth
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt

from services.db_service import db, User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    required = ["username", "email", "password"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 409

    hashed = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode()
    user = User(
        username=data["username"],
        email=data["email"],
        password=hashed,
        role=data.get("role", "user"),
    )
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id))
    return jsonify({
        "message": "Registered successfully",
        "token": token,
        "user": {"id": user.id, "username": user.username,
                 "email": user.email, "role": user.role},
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get("email", "")).first()

    if not user or not bcrypt.checkpw(
        data.get("password", "").encode(), user.password.encode()
    ):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({
        "token": token,
        "user": {"id": user.id, "username": user.username,
                 "email": user.email, "role": user.role},
    })


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())


@auth_bp.route("/users", methods=["GET"])
@jwt_required()
def list_users():
    """Admin — list all users."""
    users = User.query.all()
    return jsonify({"users": [u.to_dict() for u in users]})
