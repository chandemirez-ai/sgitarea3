import streamlit as st

from login import mostrar_login
from menu import mostrar_menu
from modulos.inicio import mostrar_inicio
from modulos.clientes import mostrar_clientes
from modulos.productos import mostrar_productos
from modulos.ventas import mostrar_ventas
from modulos.usuarios import mostrar_usuarios


st.set_page_config(
    page_title="APP SISTEMA",
    page_icon="🛒",
    layout="wide",
)


def inicializar_sesion():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False
    if "usuario" not in st.session_state:
        st.session_state["usuario"] = None


def cerrar_sesion():
    st.session_state["autenticado"] = False
    st.session_state["usuario"] = None
    st.rerun()


def main():
    inicializar_sesion()

    if not st.session_state["autenticado"]:
        mostrar_login()
        return

    opcion = mostrar_menu()

    if opcion == "Inicio":
        mostrar_inicio()
    elif opcion == "Clientes":
        mostrar_clientes()
    elif opcion == "Productos":
        mostrar_productos()
    elif opcion == "Ventas":
        mostrar_ventas()
    elif opcion == "Usuarios":
        mostrar_usuarios()
    elif opcion == "Cerrar sesión":
        cerrar_sesion()


if __name__ == "__main__":
    main()
