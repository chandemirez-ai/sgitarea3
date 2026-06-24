import streamlit as st
from config.conexion import ejecutar_consulta, ejecutar_comando


def mostrar_productos():
    st.title("Gestión de productos")

    st.subheader("Registros existentes")
    productos = ejecutar_consulta("SELECT * FROM productos ORDER BY id_producto DESC")
    st.dataframe(productos, use_container_width=True)

    st.divider()
    st.subheader("Insertar nuevo producto")

    with st.form("form_producto"):
        nombre = st.text_input("Nombre del producto")
        categoria = st.text_input("Categoría")
        precio = st.number_input("Precio", min_value=0.0, step=0.01)
        stock = st.number_input("Stock", min_value=0, step=1)
        guardar = st.form_submit_button("Guardar producto")

    if guardar:
        if not nombre:
            st.warning("El nombre del producto es obligatorio.")
        else:
            ejecutar_comando(
                """
                INSERT INTO productos (nombre, categoria, precio, stock)
                VALUES (%s, %s, %s, %s)
                """,
                (nombre, categoria, precio, stock),
            )
            st.success("Producto guardado correctamente.")
            st.rerun()

    st.divider()
    st.subheader("Eliminar producto")

    if not productos.empty:
        id_producto = st.selectbox(
            "Seleccione el producto a eliminar",
            productos["id_producto"].tolist(),
            format_func=lambda x: f"{x} - {productos.loc[productos['id_producto'] == x, 'nombre'].iloc[0]}",
        )

        if st.button("Eliminar producto"):
            try:
                ejecutar_comando("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
                st.success("Producto eliminado correctamente.")
                st.rerun()
            except Exception:
                st.error("No se puede eliminar el producto porque tiene ventas asociadas.")
