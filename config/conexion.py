import streamlit as st
import pymysql
import pandas as pd


def obtener_config_mysql():
    """
    Obtiene credenciales desde Streamlit Secrets.
    """
    mysql_config = st.secrets["mysql"]

    return {
        "host": mysql_config["host"],
        "port": int(mysql_config.get("port", 3306)),
        "user": mysql_config["user"],
        "password": mysql_config["password"],
        "database": mysql_config["database"],
        "cursorclass": pymysql.cursors.DictCursor,
        "autocommit": True,
    }


def conectar():
    """Crea una conexión nueva a MySQL."""
    config = obtener_config_mysql()
    return pymysql.connect(**config)


def ejecutar_consulta(query, params=None):
    """
    Ejecuta consultas SELECT y devuelve un DataFrame.
    Esta versión evita el problema de que pandas lea mal los nombres de columnas.
    """
    with conectar() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            resultado = cursor.fetchall()

    return pd.DataFrame(resultado)


def ejecutar_comando(query, params=None):
    """
    Ejecuta INSERT, UPDATE o DELETE.
    """
    with conectar() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.lastrowid