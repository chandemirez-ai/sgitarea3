import streamlit as st
from config.conexion import ejecutar_consulta, ejecutar_comando


def mostrar_ventas():
    st.title("Gestión de ventas")

    st.subheader("Registros existentes")
    ventas = ejecutar_consulta("""
        SELECT 
            v.id_venta,
            c.nombre AS cliente,
            p.nombre AS producto,
            v.cantidad,
            v.precio_unitario,
            v.total,
            v.fecha_venta
        FROM ventas v
        INNER JOIN clientes c ON v.id_cliente = c.id_cliente
        INNER JOIN productos p ON v.id_producto = p.id_producto
        ORDER BY v.id_venta DESC
    """)
    st.dataframe(ventas, use_container_width=True)

    clientes = ejecutar_consulta("SELECT id_cliente, nombre FROM clientes ORDER BY nombre")
    productos = ejecutar_consulta("SELECT id_producto, nombre, precio, stock FROM productos ORDER BY nombre")

    st.divider()
    st.subheader("Insertar nueva venta")

    if clientes.empty or productos.empty:
        st.warning("Debe existir al menos un cliente y un producto para registrar ventas.")
        return

    with st.form("form_venta"):
        id_cliente = st.selectbox(
            "Cliente",
            clientes["id_cliente"].tolist(),
            format_func=lambda x: clientes.loc[clientes["id_cliente"] == x, "nombre"].iloc[0],
        )

        id_producto = st.selectbox(
            "Producto",
            productos["id_producto"].tolist(),
            format_func=lambda x: productos.loc[productos["id_producto"] == x, "nombre"].iloc[0],
        )

        producto_sel = productos[productos["id_producto"] == id_producto].iloc[0]
        precio_unitario = st.number_input(
            "Precio unitario",
            min_value=0.0,
            value=float(producto_sel["precio"]),
            step=0.01,
        )
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        guardar = st.form_submit_button("Guardar venta")

    if guardar:
        stock_actual = int(producto_sel["stock"])

        if cantidad > stock_actual:
            st.error(f"No hay stock suficiente. Stock actual: {stock_actual}")
        else:
            ejecutar_comando(
                """
                INSERT INTO ventas (id_cliente, id_producto, cantidad, precio_unitario)
                VALUES (%s, %s, %s, %s)
                """,
                (id_cliente, id_producto, cantidad, precio_unitario),
            )

            ejecutar_comando(
                "UPDATE productos SET stock = stock - %s WHERE id_producto = %s",
                (cantidad, id_producto),
            )

            st.success("Venta registrada correctamente.")
            st.rerun()

    st.divider()
    st.subheader("Eliminar venta")

    ventas_ids = ejecutar_consulta("SELECT id_venta FROM ventas ORDER BY id_venta DESC")

    if not ventas_ids.empty:
        id_venta = st.selectbox("Seleccione la venta a eliminar", ventas_ids["id_venta"].tolist())

        if st.button("Eliminar venta"):
            ejecutar_comando("DELETE FROM ventas WHERE id_venta = %s", (id_venta,))
            st.success("Venta eliminada correctamente.")
            st.rerun()
