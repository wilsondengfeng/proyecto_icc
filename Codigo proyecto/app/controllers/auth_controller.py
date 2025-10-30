from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from functools import wraps

bp = Blueprint("auth", __name__)

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
    # Si el usuario ya tiene sesión activa, redirigir al dashboard (contenido cambia por rol)
    if session.get("user_id"):
        return redirect(url_for("auth.dashboard"))
    return redirect(url_for("auth.login"))

@bp.route("/login", methods=["GET", "POST"])
def login():
    # Si ya hay sesión activa, redirigir al dashboard en vez de mostrar el formulario de login
    if session.get("user_id"):
        return redirect(url_for("auth.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        try:
            current_app.logger.debug(f"auth_controller.login: intento de login para email={email}")
        except Exception:
            pass
        user = current_app.auth_service.validar_login(email, password)
        if user:
            session["user_id"] = user.id
            session["user_name"] = user.nombre
            session["is_admin"] = user.is_admin
            flash(f"Bienvenido {user.nombre}!", "success")
            return redirect(url_for("auth.dashboard"))
        flash("Email o contraseña incorrectos.", "danger")
    return render_template("login.html")

@bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("auth.login"))

@bp.route("/dashboard")
@login_required
def dashboard():
    # Dashboard unificado: muestra distinta información según el rol
    user_id = session.get("user_id")
    if session.get("is_admin"):
        users = current_app.auth_service.listar_usuarios()
        dispositivos = current_app.dispositivo_service.listar_todos()
        return render_template("admin/dashboard.html", users=users, dispositivos=dispositivos)
    else:
        dispositivos = current_app.dispositivo_service.listar_por_usuario(user_id)
        user = current_app.auth_service.repo.obtener_por_id(user_id)
        return render_template("dashboard.html", user=user, dispositivos=dispositivos)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    # Registro de nuevos usuarios (usuarios normales, no admin)
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        password_confirm = request.form.get('password_confirm', '').strip()

        if not nombre or not email or not password:
            flash('Por favor completa todos los campos.', 'warning')
            return render_template('register.html', nombre=nombre, email=email)
        if password != password_confirm:
            flash('Las contraseñas no coinciden.', 'warning')
            return render_template('register.html', nombre=nombre, email=email)

        created = current_app.auth_service.crear_usuario(nombre, email, password, is_admin=False)
        if created:
            flash('Registro exitoso. Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('No se pudo crear el usuario. El correo puede ya estar en uso.', 'danger')
            return render_template('register.html', nombre=nombre, email=email)

    return render_template('register.html')


@bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        if not email:
            flash('Ingresa un correo válido.', 'warning')
            return render_template('forgot_password.html')
        sent = current_app.auth_service.send_reset_email(email)
        if sent:
            flash('Si el correo existe en nuestro sistema, se ha enviado un enlace de recuperación.', 'info')
        else:
            flash('No se pudo enviar el correo de recuperación. Intenta más tarde.', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('forgot_password.html')


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Verificar token en GET para mostrar formulario
    if request.method == 'POST':
        pw = request.form.get('password', '').strip()
        pw2 = request.form.get('password_confirm', '').strip()
        if not pw or pw != pw2:
            flash('Las contraseñas no coinciden o están vacías.', 'warning')
            return render_template('reset_password.html', token=token)
        ok = current_app.auth_service.reset_password_with_token(token, pw)
        if ok:
            flash('Contraseña restablecida correctamente. Puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        flash('El enlace de recuperación no es válido o ha expirado.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    # GET: comprobar token rápido (no estrictamente necesario)
    email = current_app.auth_service.verify_reset_token(token)
    if not email:
        flash('El enlace de recuperación no es válido o ha expirado.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    return render_template('reset_password.html', token=token)
