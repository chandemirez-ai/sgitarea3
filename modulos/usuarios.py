import hashlib
import streamlit as st
from config.conexion import ejecutar_consulta, ejecutar_comando


def generar_hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def mostrar_usuarios():
    st.title("Gestión de usuarios")

    usuario_actual = st.session_state.get("usuario", {})
    if usuario_actual.get("rol") != "admin":
        st.warning("Solo los usuarios con rol admin pueden administrar usuarios.")
        return

    st.subheader("Usuarios registrados")
    usuarios = ejecutar_consulta("""
        SELECT id_usuario, usuario, nombre, rol, activo, fecha_creacion
        FROM USUARIO
        ORDER BY id_usuario DESC
    """)
    st.dataframe(usuarios, use_container_width=True)

    st.divider()
    st.subheader("Crear nuevo usuario")

    with st.form("form_usuario"):
        usuario = st.text_input("Usuario")
        nombre = st.text_input("Nombre")
        password = st.text_input("Contraseña", type="password")
        rol = st.selectbox("Rol", ["admin", "usuario"])
        guardar = st.form_submit_button("Guardar usuario")

    if guardar:
        if not usuario or not nombre or not password:
            st.warning("Usuario, nombre y contraseña son obligatorios.")
        else:
            try:
                ejecutar_comando(
                    """
                    INSERT INTO USUARIO (usuario, password_hash, nombre, rol, activo)
                    VALUES (%s, %s, %s, %s, 1)
                    """,
                    (usuario, generar_hash(password), nombre, rol),
                )
                st.success("Usuario creado correctamente.")
                st.rerun()
            except Exception:
                st.error("No se pudo crear el usuario. Verifica si ya existe.")
