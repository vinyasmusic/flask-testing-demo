from flask import Blueprint, jsonify, request
from app.models.user import User
from app import db
from app.schemas import UserSchema, UserResponseSchema, UserCreateSchema

users_routes = Blueprint("users_routes", __name__, url_prefix="/users")


@users_routes.route("/user", methods=["POST"])
def create_user():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    user_schema = UserCreateSchema(**data)
    user = User(**user_schema.dict())
    db.session.add(user)
    db.session.commit()
    return jsonify(UserResponseSchema.from_orm(user).dict()), 201


@users_routes.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(UserResponseSchema.from_orm(user).dict())


@users_routes.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    name = data.get("name")
    email = data.get("email")
    user = User.query.get_or_404(user_id)
    user.name = name or user.name
    user.email = email or user.email
    db.session.commit()
    return jsonify(user.to_dict())


@users_routes.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 204
