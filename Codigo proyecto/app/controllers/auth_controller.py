from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.auth_service import AuthService
from functools import wraps

bp = Blueprint("auth", __name__)
auth_service = AuthService()

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if "user_id" not in session:
            flash("Por favor inicie sesión para acceder.", "warning")
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view

def admin_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if "user_id" not in session or not session.get("is_admin", False):
            flash("Acceso no autorizado. Se requieren permisos de administrador.", "danger")
            return redirect(url_for("auth.login"))
        return view(**kwargs)
    return wrapped_view

@bp.route("/", methods=["GET"])
def root():
    return redirect(url_for("auth.login"))

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        user = auth_service.validar_login(email, password)
        if user:
            session["user_id"] = user.id
            session["user_name"] = user.nombre
            session["is_admin"] = user.is_admin
            if user.is_admin:
                flash(f"Bienvenido administrador {user.nombre}!", "success")
                return redirect(url_for("auth.admin_dashboard"))
            else:
                flash(f"Bienvenido {user.nombre}!", "success")
                return redirect(url_for("auth.user_dashboard"))
        flash("Email o contraseña incorrectos.", "danger")
    return render_template("login.html")

@bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("auth.login"))

@bp.route("/admin")
@admin_required
def admin_dashboard():
    users = auth_service.listar_usuarios()
    return render_template("admin/dashboard.html", users=users)

@bp.route("/dashboard")
@login_required
def user_dashboard():
    user_id = session.get("user_id")
    user = auth_service.repo.obtener_por_id(user_id)
    return render_template("dashboard.html", user=user)
