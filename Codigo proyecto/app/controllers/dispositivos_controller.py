from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.services.dispositivo_service import DispositivoService
from app.models.dispositivo import Dispositivo
from app.controllers.auth_controller import login_required, admin_required

bp = Blueprint("dispositivos", __name__)
service = DispositivoService()


@bp.route("/", methods=["GET"])
@login_required
def index():
    # if admin, show all devices; otherwise show only user's devices
    if session.get("is_admin"):
        dispositivos = service.listar_todos()
    else:
        dispositivos = service.listar_por_usuario(session.get("user_id"))
    return render_template("dispositivos/index.html", dispositivos=dispositivos)


@bp.route("/nuevo", methods=["GET", "POST"])
@admin_required
def crear():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        tipo = request.form.get("tipo", "luz").strip()
        usuario_id = request.form.get("usuario_id") or None
        usuario_id = int(usuario_id) if usuario_id else None
        if not nombre:
            flash("El nombre es obligatorio.", "warning")
            return render_template("dispositivos/form.html", dispositivo=None)
        service.crear(nombre, tipo, usuario_id)
        flash("Dispositivo creado.", "success")
        return redirect(url_for("dispositivos.index"))
    return render_template("dispositivos/form.html", dispositivo=None)


@bp.route("/<int:dispositivo_id>/editar", methods=["GET", "POST"])
@admin_required
def editar(dispositivo_id):
    d = service.obtener(dispositivo_id)
    if not d:
        flash("Dispositivo no encontrado.", "danger")
        return redirect(url_for("dispositivos.index"))
    if request.method == "POST":
        d.nombre = request.form.get("nombre", "").strip()
        d.tipo = request.form.get("tipo", "luz").strip()
        usuario_id = request.form.get("usuario_id") or None
        d.usuario_id = int(usuario_id) if usuario_id else None
        service.actualizar(d)
        flash("Dispositivo actualizado.", "success")
        return redirect(url_for("dispositivos.index"))
    return render_template("dispositivos/form.html", dispositivo=d)


@bp.route("/<int:dispositivo_id>/eliminar", methods=["POST"])
@admin_required
def eliminar(dispositivo_id):
    service.eliminar(dispositivo_id)
    flash("Dispositivo eliminado.", "info")
    return redirect(url_for("dispositivos.index"))


@bp.route("/<int:dispositivo_id>/toggle", methods=["POST"])
@login_required
def toggle(dispositivo_id):
    nuevo = service.toggle_estado(dispositivo_id)
    if nuevo is None:
        return jsonify({"error": "no encontrado"}), 404
    return jsonify({"estado": nuevo}), 200
