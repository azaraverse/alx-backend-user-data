#!/usr/bin/env python3
""" Basic Flask App
"""

from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """ Index route
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """ Users /POST route
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        new_user = AUTH.register_user(email=email, password=password)
        return jsonify(
            {"email": f"{new_user.email}", "message": "user created"}
        )
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"))
