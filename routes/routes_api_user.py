from flask import Blueprint, jsonify
from utils.decorators import login_required
from services.graph_service import get_user_photo

api_user = Blueprint("api_user", __name__)

@api_user.route("/api/user_photo")
@login_required
def user_photo():
    try:
        photo_base64 = get_user_photo()
        return jsonify({"photo": photo_base64})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
