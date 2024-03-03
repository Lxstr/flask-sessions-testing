import base64
import sys

from app.config import Config
from flask import Blueprint, current_app, jsonify, session

guest = Blueprint("guest", __name__)


@guest.route("/", methods=["GET"])
def index():
    # check if we see secret key
    # print(f"Secret Key: {Config.SECRET_KEY}")
    # print(f"{current_app.secret_key}")

    session["key"] = "some value"
    return jsonify({"session key": "is set"})


@guest.route("/get_session", methods=["GET"])
def get_session():
    if not session:
        return jsonify("No active session to check")

    session_size = sys.getsizeof(str(session))
    session_elements = {}

    for key, value in session.items():
        if isinstance(value, bytes):
            value = base64.b64encode(value).decode()
        session_elements[key] = value

    return jsonify(
        {"session_size in bytes": session_size, "session_elements": session_elements}
    )
