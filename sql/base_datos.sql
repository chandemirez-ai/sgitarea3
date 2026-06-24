-- Base de datos para aplicación Streamlit + MySQL en Clever Cloud
-- Ejecutar en phpMyAdmin, dentro de la base de datos creada en Clever Cloud.

CREATE TABLE IF NOT EXISTS USUARIO (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(64) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    rol VARCHAR(30) DEFAULT 'usuario',
    activo TINYINT(1) DEFAULT 1,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    correo VARCHAR(120),
    telefono VARCHAR(30),
    direccion VARCHAR(200),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    categoria VARCHAR(80),
    precio DECIMAL(10,2) NOT NULL,
    stock INT NOT NULL DEFAULT 0,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ventas (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) GENERATED ALWAYS AS (cantidad * precio_unitario) STORED,
    fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_ventas_clientes FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    CONSTRAINT fk_ventas_productos FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- Usuario de prueba:
-- Usuario: admin
-- Contraseña: admin123
-- Hash SHA-256 de admin123
INSERT INTO USUARIO (usuario, password_hash, nombre, rol, activo)
VALUES ('admin', '240be518fabd2724d70f5f00eb8d9f8a7ca7ac9a9f4b657f8ef9b3ffce1e27b9', 'Administrador del sistema', 'admin', 1)
ON DUPLICATE KEY UPDATE usuario = usuario;

INSERT INTO clientes (nombre, correo, telefono, direccion) VALUES
('Ana Martínez', 'ana.martinez@email.com', '7000-1111', 'San Salvador'),
('Carlos López', 'carlos.lopez@email.com', '7000-2222', 'Santa Tecla'),
('María Gómez', 'maria.gomez@email.com', '7000-3333', 'Soyapango');

INSERT INTO productos (nombre, categoria, precio, stock) VALUES
('Laptop Lenovo ThinkPad', 'Tecnología', 850.00, 10),
('Mouse inalámbrico', 'Accesorios', 18.50, 50),
('Teclado mecánico', 'Accesorios', 65.00, 25);

INSERT INTO ventas (id_cliente, id_producto, cantidad, precio_unitario) VALUES
(1, 1, 1, 850.00),
(2, 2, 3, 18.50),
(3, 3, 2, 65.00);
