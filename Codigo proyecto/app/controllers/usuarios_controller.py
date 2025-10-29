from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.repositories.usuario_repository import UsuarioRepository
from app.models.usuario import Usuario
from app.controllers.auth_controller import admin_required

bp = Blueprint("usuarios", __name__)
repo = UsuarioRepository()

@bp.route("/", methods=["GET"])
@admin_required
def index():
    usuarios = repo.obtener_todos()
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
        usuario = Usuario(nombre=nombre, email=email)
        repo.crear(usuario)
        flash("Usuario creado correctamente.", "success")
        return redirect(url_for("usuarios.index"))
    return render_template("usuarios/form.html", usuario=None)

@bp.route("/<int:usuario_id>/editar", methods=["GET", "POST"])
@admin_required
def editar(usuario_id):
    usuario = repo.obtener_por_id(usuario_id)
    if not usuario:
        flash("Usuario no encontrado.", "danger")
        return redirect(url_for("usuarios.index"))
    
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip()
        if not nombre or not email:
            flash("Todos los campos son obligatorios.", "warning")
            return render_template("usuarios/form.html", usuario=usuario)
        
        usuario.nombre = nombre
        usuario.email = email
        repo.actualizar(usuario)
        flash("Usuario actualizado correctamente.", "success")
        return redirect(url_for("usuarios.index"))
    
    return render_template("usuarios/form.html", usuario=usuario)

@bp.route("/<int:usuario_id>/eliminar", methods=["POST"])
@admin_required
def eliminar(usuario_id):
    usuario = repo.obtener_por_id(usuario_id)
    if usuario:
        repo.eliminar(usuario_id)
        flash("Usuario eliminado correctamente.", "success")
    else:
        flash("Usuario no encontrado.", "danger")
    return redirect(url_for("usuarios.index"))
