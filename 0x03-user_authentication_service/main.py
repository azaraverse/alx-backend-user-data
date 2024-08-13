#!/usr/bin/env python3
""" Main app module
"""
import requests


def register_user(email: str, password: str) -> None:
    """ Tests the Flask App's register user function and
    /users route to return expected status code and payload
    """
    url = "http://127.0.0.1:5000/users"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url=url, data=data)
    assert response.status_code == 200
    assert response.json() == {
        "email": email, "message": "user created"
    }


def log_in_wrong_password(email: str, password: str) -> None:
    """ Tests the Flask App's login function and
    /sessions route to return expected status code
    """
    url = "http://127.0.0.1:5000/sessions"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url=url, data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> None:
    """ Tests the Flask App's login function and
    /sessions route to return expected status code and payload
    """
    url = "http://127.0.0.1:5000/sessions"
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url=url, data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    assert "session_id" in response.cookies.keys()
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    """ Test an attempt to retrieve a user profile without a login
    Meaning, there's no session_id generated
    """
    url = "http://127.0.0.1:5000/profile"

    response = requests.get(url=url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """ Test an attempt to show a user profile with a particular session
    ID
    """
    url = "http://127.0.0.1:5000/profile"
    cookie = {
        "session_id": session_id
    }
    response = requests.get(url=url, cookies=cookie)
    assert response.status_code == 200
    assert response.json() == {"email": "guillaume@holberton.io"}


def log_out(session_id: str) -> None:
    """ Test a logout attempt and session_id related to logged-out user
    deletion
    """
    url = "http://127.0.0.1:5000/sessions"
    cookie = {
        "session_id": session_id
    }
    response = requests.delete(url=url, cookies=cookie)
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """ Test an attempt to generate a reset password token
    """
    url = "http://127.0.0.1:5000/reset_password"
    data = {
        "email": email
    }
    response = requests.post(url=url, data=data)
    assert response.status_code == 200
    reset_token = response.json().get("reset_token")
    assert response.json() == {"email": email, "reset_token": reset_token}
    return reset_token


def update_password(
        email: str, reset_token: str, new_password: str
) -> None:
    """ Test an attempt to change a user's password using the generated
    reset password token
    """
    url = "http://127.0.0.1:5000/reset_password"
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }

    response = requests.put(url=url, data=data)
    assert response.status_code == 200
    assert response.json() == {
        "email": email, "message": "Password updated"
    }


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
