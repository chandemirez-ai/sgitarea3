import streamlit as st


def mostrar_menu():
    """Muestra el menú lateral después del login."""
    usuario = st.session_state.get("usuario", {})

    st.sidebar.title("Menú del sistema")
    st.sidebar.write(f"Usuario: **{usuario.get('nombre', '')}**")
    st.sidebar.caption(f"Rol: {usuario.get('rol', '')}")

    opcion = st.sidebar.radio(
        "Seleccione una sección",
        [
            "Inicio",
            "Clientes",
            "Productos",
            "Ventas",
            "Usuarios",
            "Cerrar sesión",
        ],
    )

    return opcion
