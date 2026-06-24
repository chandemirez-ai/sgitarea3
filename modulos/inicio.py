import streamlit as st
from config.conexion import ejecutar_consulta


def mostrar_inicio():
    st.title("Panel principal")
    st.write("Información General")

    col1, col2, col3 = st.columns(3)

    total_clientes = ejecutar_consulta("SELECT COUNT(*) AS total FROM clientes").iloc[0]["total"]
    total_productos = ejecutar_consulta("SELECT COUNT(*) AS total FROM productos").iloc[0]["total"]
    total_ventas = ejecutar_consulta("SELECT COUNT(*) AS total FROM ventas").iloc[0]["total"]

    col1.metric("Clientes", total_clientes)
    col2.metric("Productos", total_productos)
    col3.metric("Ventas", total_ventas)

    st.divider()
    st.subheader("Últimas ventas registradas")

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
        LIMIT 10
    """)

    st.dataframe(ventas, use_container_width=True)
