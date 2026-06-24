import streamlit as st
from config.conexion import ejecutar_consulta, ejecutar_comando


def mostrar_clientes():
    st.title("Gestión de clientes")

    st.subheader("Registros existentes")
    clientes = ejecutar_consulta("SELECT * FROM clientes ORDER BY id_cliente DESC")
    st.dataframe(clientes, use_container_width=True)

    st.divider()
    st.subheader("Insertar nuevo cliente")

    with st.form("form_cliente"):
        nombre = st.text_input("Nombre del cliente")
        correo = st.text_input("Correo")
        telefono = st.text_input("Teléfono")
        direccion = st.text_input("Dirección")
        guardar = st.form_submit_button("Guardar cliente")

    if guardar:
        if not nombre:
            st.warning("El nombre del cliente es obligatorio.")
        else:
            ejecutar_comando(
                """
                INSERT INTO clientes (nombre, correo, telefono, direccion)
                VALUES (%s, %s, %s, %s)
                """,
                (nombre, correo, telefono, direccion),
            )
            st.success("Cliente guardado correctamente.")
            st.rerun()

    st.divider()
    st.subheader("Eliminar cliente")

    if not clientes.empty:
        id_cliente = st.selectbox(
            "Seleccione el cliente a eliminar",
            clientes["id_cliente"].tolist(),
            format_func=lambda x: f"{x} - {clientes.loc[clientes['id_cliente'] == x, 'nombre'].iloc[0]}",
        )

        if st.button("Eliminar cliente"):
            try:
                ejecutar_comando("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
                st.success("Cliente eliminado correctamente.")
                st.rerun()
            except Exception:
                st.error("No se puede eliminar el cliente porque tiene ventas asociadas.")
