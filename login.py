import hashlib
import streamlit as st
from config.conexion import conectar


def generar_hash(password: str) -> str:
    """Convierte una contraseña en hash SHA-256."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def validar_usuario(usuario: str, password: str):
    """Valida usuario y contraseña contra la tabla USUARIO."""

    usuario = usuario.strip()
    password = password.strip()
    password_hash = generar_hash(password)

    query = """
        SELECT id_usuario, usuario, password_hash, nombre, rol, activo
        FROM USUARIO
        WHERE usuario = %s
        LIMIT 1
    """

    try:
        with conectar() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (usuario,))
                datos = cursor.fetchone()

        if not datos:
            st.error("El usuario no existe en la base de datos.")
            return None

        if int(datos["activo"]) != 1:
            st.error("El usuario existe, pero está inactivo.")
            return None

        hash_bd = str(datos["password_hash"]).strip()

        if password_hash != hash_bd:
            st.error("La contraseña no coincide.")
            st.write("Hash generado por la app:")
            st.code(password_hash)
            st.write("Hash guardado en la base:")
            st.code(hash_bd)
            return None

        return {
            "id_usuario": datos["id_usuario"],
            "usuario": datos["usuario"],
            "nombre": datos["nombre"],
            "rol": datos["rol"],
        }

    except Exception as error:
        st.error("Error al validar el usuario.")
        st.exception(error)
        return None


def mostrar_login():
    """Pantalla de inicio de sesión."""
    st.title("Sistema de Gestión")
    st.subheader("Inicio de sesión")

    with st.form("form_login"):
        usuario = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        ingresar = st.form_submit_button("Ingresar")

    if ingresar:
        if not usuario or not password:
            st.warning("Debe ingresar usuario y contraseña.")
            return

        datos_usuario = validar_usuario(usuario, password)

        if datos_usuario:
            st.session_state["autenticado"] = True
            st.session_state["usuario"] = datos_usuario
            st.success("Inicio de sesión correcto.")
            st.rerun()