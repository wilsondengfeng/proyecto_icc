-- ==========================================
-- BASE DE DATOS: smarthome_webcontrol
-- Versión con admin y usuarios separados
-- ==========================================

CREATE DATABASE IF NOT EXISTS smarthome_webcontrol
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

USE smarthome_webcontrol;

-- ==========================================
-- TABLA: admin
-- ==========================================
CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
) ENGINE=InnoDB;

-- ==========================================
-- TABLA: usuarios
-- ==========================================
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
) ENGINE=InnoDB;

-- ==========================================
-- TABLA: dispositivos
-- ==========================================
CREATE TABLE dispositivos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    tipo ENUM('luz', 'sensor') NOT NULL,
    estado BOOLEAN DEFAULT FALSE,
    usuario_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ==========================================
-- DATOS INICIALES
-- ==========================================

-- Administrador de prueba
INSERT INTO admin (nombre, email, password)
VALUES ('Admin', 'admin@smarthome.com', 'scrypt:32768:8:1$oLhYOqbRr8rOX5SA$061be90174ffebba753cb5f09bf946ab03d40fd386f4e907f04141f1f1dab01391d764cbd47d96112f882815238759579ba8c0569b2668efa2bea9d62138cd6c');

-- Usuarios de prueba
INSERT INTO usuarios (nombre, email, password)
VALUES
('Wilson Deng', 'wilson@smarthome.com', 'scrypt:32768:8:1$z39BviKJHDhiw5ex$b0d3045351dfd3e3bf2962206aac42ffb8d0fdd72d2ecdc0426892d08b23c2e5fc5d02a638a16ce2601b6366ae79bc4b93a6408836a5ded0d4c611f73dc9bfca'), ('Carlo Torres', 'carlo@smarthome.com', 'scrypt:32768:8:1$v4YCylnMJzku8SYA$4c118b5df27feeb5f66ba4841744dd45fe4a1e1aa737db18904643bf7146757fc2e9712d255e161fa94fe23046756c6bc221c3cd31a66b6a3e10b84b4a5391a3');

-- Dispositivos asociados a usuarios
INSERT INTO dispositivos (nombre, tipo, estado, usuario_id) VALUES
('Luz Sala', 'luz', FALSE, 1),
('Sensor Movimiento', 'sensor', TRUE, 1),
('Luz Cocina', 'luz', TRUE, 2); 
