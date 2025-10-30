from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.controllers.auth_controller import admin_required

bp = Blueprint("usuarios", __name__)

@bp.route("/", methods=["GET"])
@admin_required
def index():
    usuarios = current_app.usuario_service.listar()
    return render_template("usuarios/index.html", usuarios=usuarios)

@bp.route("/nuevo", methods=["GET", "POST"])
@admin_required
def crear():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        if not nombre or not email:
            flash("Todos los campos son obligatorios.", "warning")
            return render_template("usuarios/form.html", usuario=None)
        current_app.usuario_service.crear(nombre, email)
        flash("Usuario creado correctamente.", "success")
        return redirect(url_for("usuarios.index"))
    return render_template("usuarios/form.html", usuario=None)

@bp.route("/<int:usuario_id>/editar", methods=["GET", "POST"])
@admin_required
def editar(usuario_id):
    usuario = current_app.usuario_service.obtener(usuario_id)
    if not usuario:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for("usuarios.index"))
    
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        if not nombre or not email:
            flash("Todos los campos son obligatorios.", "warning")
            return render_template("usuarios/form.html", usuario=usuario)
        
        current_app.usuario_service.actualizar(usuario_id, nombre, email)
        flash("Usuario actualizado correctamente.", "success")
        return redirect(url_for("usuarios.index"))
    
    return render_template("usuarios/form.html", usuario=usuario)

@bp.route("/<int:usuario_id>/eliminar", methods=["POST"])
@admin_required
def eliminar(usuario_id):
    usuario = current_app.usuario_service.obtener(usuario_id)
    if usuario:
        current_app.usuario_service.eliminar(usuario_id)
        flash("Usuario eliminado correctamente.", "success")
    else:
        flash("Usuario no encontrado.", "danger")
    return redirect(url_for("usuarios.index"))
