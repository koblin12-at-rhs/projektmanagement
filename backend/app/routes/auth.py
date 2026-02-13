from flask import Blueprint, jsonify, request
from flask_login import current_user, login_user, logout_user

from app import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/local/login")
def local_login():
    data = request.get_json() or {}
    user = User.query.filter_by(username=data.get("username")).first()
    if not user or not user.check_password(data.get("password", "")):
        return jsonify({"message": "Invalid credentials"}), 401
    login_user(user)
    return jsonify({"id": user.id, "username": user.username, "role": user.role})


@auth_bp.post("/local/register")
def local_register():
    data = request.get_json() or {}
    user = User(username=data["username"], email=data["email"], role=data.get("role", "student"))
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id}), 201


@auth_bp.post("/logout")
def logout():
    logout_user()
    return jsonify({"status": "ok"})


@auth_bp.get("/saml/login")
def saml_stub():
    return jsonify({"message": "SAML 2.0 login stub endpoint"})


@auth_bp.get("/me")
def me():
    if not current_user.is_authenticated:
        return jsonify({"authenticated": False})
    return jsonify({"authenticated": True, "username": current_user.username, "role": current_user.role})
