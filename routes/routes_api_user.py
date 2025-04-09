from flask import Blueprint, jsonify
from services.auth_manager import get_user_photo

api_user = Blueprint("api_user", __name__)

@api_user.route("/api/user_photo")
def api_user_photo():
    photo = get_user_photo()
    return jsonify({"photo": photo})