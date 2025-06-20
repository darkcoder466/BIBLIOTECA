-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS biblioteca;
USE biblioteca;

-- Tabla de administradores
CREATE TABLE administradores (
    id_administrador INT AUTO_INCREMENT PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    telefono VARCHAR(15),
    email VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    fecha_creacion DATE DEFAULT (CURRENT_DATE)
);

-- Tabla de bibliotecarios
CREATE TABLE bibliotecarios (
    id_bibliotecario INT AUTO_INCREMENT PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    telefono VARCHAR(15),
    email VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    fecha_creacion DATE DEFAULT (CURRENT_DATE)
);

-- Tabla de usuarios
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    telefono VARCHAR(15),
    email VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    fecha_registro DATE DEFAULT (CURRENT_DATE)
) ;

-- Tabla de libros
CREATE TABLE libros (
    id_libro INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    autor VARCHAR(100) NOT NULL,
    ano_publicacion INT,
    estado ENUM('disponible', 'prestado') DEFAULT 'disponible',
    fecha_registro DATE DEFAULT (CURRENT_DATE)
);

-- Tabla de préstamos
CREATE TABLE prestamos (
    id_prestamo INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_libro INT NOT NULL,
    fecha_prestamo DATE NOT NULL,
    fecha_devolucion_estimada DATE NOT NULL,
    fecha_devolucion_real DATE,
    estado ENUM('pendiente','aprovado', 'devuelto', 'en mora') DEFAULT 'pendiente',
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_libro) REFERENCES libros(id_libro) 
);

-- Tabla de informes de libros
CREATE TABLE informe_libros (
    id_informe INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    total_libros INT DEFAULT 0,
    libros_disponibles INT DEFAULT 0,
    libros_prestados INT DEFAULT 0,
    libros_mora INT DEFAULT 0
);

