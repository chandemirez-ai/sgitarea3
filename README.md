# Aplicación Streamlit + MySQL en Clever Cloud

## Objetivo

Aplicación funcional desarrollada en Streamlit conectada a una base de datos MySQL alojada en Clever Cloud y administrada desde phpMyAdmin. Incluye login, menú lateral y gestión de múltiples tablas.

## Estructura del proyecto

```text
streamlit_clever_mysql_app/
│
├── app.py
├── login.py
├── menu.py
├── requirements.txt
├── .gitignore
│
├── config/
│   └── conexion.py
│
├── modulos/
│   ├── inicio.py
│   ├── clientes.py
│   ├── productos.py
│   ├── ventas.py
│   └── usuarios.py
│
├── sql/
│   └── base_datos.sql
│
└── .streamlit/
    └── secrets.example.toml
```

## Tablas incluidas

- `USUARIO`: almacena usuarios del sistema.
- `clientes`: registro de clientes.
- `productos`: registro de productos.
- `ventas`: registro de ventas relacionadas con clientes y productos.

## Usuario de prueba

```text
Usuario: admin
Contraseña: admin123
```

## Instalación local

1. Crear entorno virtual:

```bash
python -m venv venv
```

2. Activar entorno virtual:

```bash
venv\Scripts\activate
```

En Mac/Linux:

```bash
source venv/bin/activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Crear archivo local de secretos:

Copiar:

```text
.streamlit/secrets.example.toml
```

como:

```text
.streamlit/secrets.toml
```

Luego completar las credenciales de MySQL de Clever Cloud.

5. Ejecutar:

```bash
streamlit run app.py
```

## Configuración de base de datos en Clever Cloud

1. Crear un add-on MySQL en Clever Cloud.
2. Abrir phpMyAdmin desde el panel de Clever Cloud.
3. Entrar a la base de datos asignada.
4. Ejecutar el script `sql/base_datos.sql`.
5. Copiar host, puerto, usuario, contraseña y nombre de base de datos.
6. Configurar esas credenciales en Streamlit Cloud como Secrets.

## Secrets para Streamlit Cloud

En Streamlit Cloud ir a:

```text
App > Settings > Secrets
```

Pegar:

```toml
[mysql]
host = "tu_host_mysql_clever_cloud"
port = 3306
database = "tu_base_de_datos"
user = "tu_usuario"
password = "tu_password"
```

## Despliegue en Streamlit Cloud

1. Subir el proyecto a GitHub.
2. Crear una nueva app en Streamlit Cloud.
3. Seleccionar el repositorio.
4. Main file path:

```text
app.py
```

5. Agregar los Secrets de conexión.
6. Deploy.

## Entregables sugeridos

1. Enlace público de Streamlit Cloud.
2. Captura o acceso de phpMyAdmin.
3. Repositorio GitHub con estructura completa.
4. Script SQL utilizado.
