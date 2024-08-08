#!/usr/bin/env python3
""" Session Auth Flask View
"""
from typing import Tuple, Dict
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models.user import User
import os


@app_views.route(
        '/auth_session/login', methods=['POST'], strict_slashes=False
)
def login() -> Tuple[Dict, int]:
    """ POST /api/v1/auth_session/login

    Return:
      - User object based on credentials
      - 400 if email or password missing
      - 401 if wrong password submitted
      - 404 if the User doesn't exist
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]
    if not User.is_valid_password(user, password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    resp = make_response(jsonify(user.to_json()))
    resp.set_cookie(os.getenv('SESSION_NAME'), session_id)

    return resp


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False
)
def logout() -> Tuple[str, int]:
    """ DELETE /api/v1/auth_session/logout
    """
    from api.v1.app import auth

    session_destroyed = auth.destroy_session(request)
    if session_destroyed == False:
        abort(404)
    return jsonify({}), 200
