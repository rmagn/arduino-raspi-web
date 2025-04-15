# /routes/routes_admin.py

from flask import Blueprint, render_template, request, jsonify
from utils.decorators import login_required, role_required
import services.users_service as users_service

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/dashboard")
@login_required
@role_required("administrateur")
def dashboard_Admin():
    """
    Renders the admin dashboard management page.
    """
    cards = [
    {"url": "/admin/users", "icon": "bi-people", "title": "Utilisateurs"},
    {"url": "/HardwareManagement", "icon": "bi-house-gear", "title": "Alias Arduino/Sonde"},
    {"url": "/admin/notifications", "icon": "bi-bell", "title": "Notifications"},
    {"url": "/admin/templates", "icon": "bi-envelope-at", "title": "Templates"},
    ]
    return render_template("admin/dashboard.html", cards=cards)

@admin_bp.route("/admin/users")
@login_required
@role_required("administrateur")
def admin_users():
    """
    Renders the admin users management page.

    This route is accessible only to logged-in users with the "administrateur" role.
    It retrieves all users from the database and displays them on the admin users
    management page.

    Returns:
        A rendered HTML page displaying the list of users.
    """
    users = users_service.get_all_users()
    return render_template("admin/users.html", users=users)


@admin_bp.route("/admin/users/edit", methods=["POST"])
@login_required
@role_required("administrateur")
def edit_user():
    data = request.form.to_dict()
    email = data.get("email")  # on utilise directement le champ email comme identifiant

    if not email:
        return jsonify({"success": False, "message": "Email requis"}), 400

    success = users_service.update_user(email, data)

    if success:
        user = users_service.get_user_by_email(email)
        return jsonify({
            "success": True,
            "message": "Utilisateur modifié avec succès",
            "user": {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "birthdate": user.birthdate,
                "role": user.role
            }
        })
    else:
        return jsonify({"success": False, "message": "Utilisateur non trouvé"}), 404

    
@admin_bp.route("/admin/users/delete", methods=["POST"])
@login_required
@role_required("administrateur")
def delete_user():
    email = request.form.get("email")

    if not email:
        return jsonify({"success": False, "message": "Email manquant"}), 400

    success = users_service.delete_user(email)
    if success:
        return jsonify({"success": True, "message": "Utilisateur supprimé avec succès"})
    else:
        return jsonify({"success": False, "message": "Utilisateur non trouvé"}), 404


@admin_bp.route("/admin/users/create", methods=["POST"])
@login_required
@role_required("administrateur")
def create_user():
    data = request.form.to_dict()
    email = data.get("email")

    if not email:
        return jsonify({"success": False, "message": "Email requis"}), 400

    user_exists = users_service.get_user_by_email(email)
    if user_exists:
        return jsonify({"success": False, "message": "Utilisateur déjà existant"}), 409

    sucess = users_service.create_user(data)    

    if sucess:
        new_user = users_service.get_user_by_email(email)
        return jsonify({
            "success": True,
            "message": "Nouvel utilisateur crée avec succès !",
            "user": {
                "email": new_user.email,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "birthdate": new_user.birthdate,
                "role": new_user.role
                }})
    else:
        return jsonify({"success": False, "message": "Erreur lors de la création"}), 500
