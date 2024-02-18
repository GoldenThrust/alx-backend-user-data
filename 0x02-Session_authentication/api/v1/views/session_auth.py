#!/usr/bin/env python3
""" Module of session auth views
"""
import requests
from os import getenv
from typing import Tuple
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login() -> Tuple[str, int]:
    """login routes"""
    email = request.form.get("email")
    password = request.form.get("password")

    user = User(email=email, password=password)
    user.save()

    for user in User.all():
        print(user.email)

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    if not users[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(users[0].id)
    response = jsonify(users[0].to_json())
    response.set_cookie(getenv("SESSION_NAME"), session_id)
    return response


@app_views.route("/auth_session/logout", methods=["DELETE"],
                 strict_slashes=False)
def logout():
    """logout routes"""
    from api.v1.app import auth

    destroyed_session_id = auth.destroy_session(request)
    if destroyed_session_id is False:
        abort(404)
    return {}, 200
