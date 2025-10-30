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
    password VARCHAR(100) NOT NULL
) ENGINE=InnoDB;

-- ==========================================
-- TABLA: usuarios
-- ==========================================
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
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
VALUES ('Admin', 'admin@smarthome.com', 'admin123');

-- Usuarios de prueba
INSERT INTO usuarios (nombre, email, password)
VALUES
('Wilson Deng', 'wilson@smarthome.com', '123456'),
('Carlo Torres', 'carlo@smarthome.com', '123456');

-- Dispositivos asociados a usuarios
INSERT INTO dispositivos (nombre, tipo, estado, usuario_id) VALUES
('Luz Sala', 'luz', FALSE, 1),
('Sensor Movimiento', 'sensor', TRUE, 1),
('Luz Cocina', 'luz', TRUE, 2); 
