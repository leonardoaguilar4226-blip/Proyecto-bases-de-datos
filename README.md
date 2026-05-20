# Configuración de Base de Datos - Biblioteca

Para que el sistema **LibraryControl** (`7.py`) pueda conectarse y funcionar correctamente, debes crear una base de datos en PostgreSQL con los siguientes parámetros y estructura.

## ⚙️ Conexión Básica
*   **Base de datos:** `Biblioteca`
*   **Host:** `localhost`
*   **Puerto:** `5432`
*   **Usuario:** `postgres`
*   **Contraseña:** `1234`

---

## 📋 Estructura de Tablas y Columnas (Tuplas)

### 1. Tabla: `usuario`
*   `nombre_del_usuario` (character varying / texto) - *Usuario administrador (ej. 'admin')*
*   `contrasena` (character varying / texto) - *Contraseña para ingresar*

### 2. Tabla: `empleado`
*   `codigo` (integer) — **Llave Primaria**
*   `nombre` (character varying(100))
*   `direccion` (character varying(150))
*   `telefono` (character varying(20))
*   `sexo` (character(1)) — *'M' o 'F'*
*   `fecha_nac` (date)
*   `turno` (character varying(20)) — *'Matutino' o 'Vespertino'*

### 3. Tabla: `alumnos`
*   `codigo` (integer) — **Llave Primaria**
*   `nombre` (character varying(100))
*   `carrera` (character varying(100))
*   `correo` (character varying(100))
*   `direccion` (character varying(150))
*   `telefono` (character varying(20))
*   `sexo` (character(1)) — *'M' o 'F'*
*   `fecha_nac` (date)

### 4. Tabla: `maestros`
*   `codigo` (integer) — **Llave Primaria**
*   `nombre` (character varying(100))
*   `departamento` (character varying(100))
*   `correo` (character varying(100))
*   `direccion` (character varying(150))
*   `telefono` (character varying(20))
*   `sexo` (character(1)) — *'M' o 'F'*
*   `fecha_nac` (date)

### 5. Tabla: `libros`
*   `isbn` (character varying(20)) — **Llave Primaria**
*   `titulo` (character varying(150))
*   `autores` (character varying(150))
*   `editorial` (character varying(100))
*   `año_publicacion` (integer)
*   `num_ejemplar` (integer)

### 6. Tabla: `prestamo`
*   `id_prestamo` (serial) — **Llave Primaria**
*   `tipo_solicitante` (character(1)) — *'A' (Alumno) o 'P' (Profesor)*
*   `codigo_alumno` (integer) — *Llave Foránea (opcional) a alumnos(codigo)*
*   `codigo_profesor` (integer) — *Llave Foránea (opcional) a maestros(codigo)*
*   `isbn` (character varying(20)) — *Llave Foránea (opcional) a libros(isbn)*
*   `num_ejemplar` (integer)
*   `fecha_prestamo` (date)
*   `fecha_limite` (date)
*   `fecha_devolucion` (date) — *Puede ser NULL hasta que se devuelva*
*   `estatus` (character varying(20)) — *Por defecto 'prestado'*
*   `multa` (numeric(10,2)) — *Por defecto 0.00*

---

## 🛠️ Script SQL de Inicialización (DDL)

Puedes copiar y pegar el siguiente script en tu consola de PostgreSQL (o en la Query Tool de pgAdmin) para crear las tablas automáticamente con la configuración requerida:

```sql
-- Crear base de datos (Ejecutar por separado si es necesario)
-- CREATE DATABASE "Biblioteca";

CREATE TABLE IF NOT EXISTS usuario (
    nombre_del_usuario VARCHAR(50) PRIMARY KEY,
    contrasena VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS empleado (
    codigo INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(150),
    telefono VARCHAR(20),
    sexo CHAR(1) CHECK (sexo IN ('F', 'M')),
    fecha_nac DATE,
    turno VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS alumnos (
    codigo INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    carrera VARCHAR(100),
    correo VARCHAR(100),
    direccion VARCHAR(150),
    telefono VARCHAR(20),
    sexo CHAR(1) CHECK (sexo IN ('F', 'M')),
    fecha_nac DATE
);

CREATE TABLE IF NOT EXISTS maestros (
    codigo INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    departamento VARCHAR(100),
    correo VARCHAR(100),
    direccion VARCHAR(150),
    telefono VARCHAR(20),
    sexo CHAR(1) CHECK (sexo IN ('F', 'M')),
    fecha_nac DATE
);

CREATE TABLE IF NOT EXISTS libros (
    isbn VARCHAR(20) PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    autores VARCHAR(150),
    editorial VARCHAR(100),
    año_publicacion INT,
    num_ejemplar INT
);

CREATE TABLE IF NOT EXISTS prestamo (
    id_prestamo SERIAL PRIMARY KEY,
    tipo_solicitante CHAR(1) CHECK (tipo_solicitante IN ('A', 'P')),
    codigo_alumno INT REFERENCES alumnos(codigo) ON DELETE SET NULL,
    codigo_profesor INT REFERENCES maestros(codigo) ON DELETE SET NULL,
    isbn VARCHAR(20) REFERENCES libros(isbn) ON DELETE SET NULL,
    num_ejemplar INT,
    fecha_prestamo DATE NOT NULL,
    fecha_limite DATE NOT NULL,
    fecha_devolucion DATE DEFAULT NULL,
    estatus VARCHAR(20) DEFAULT 'prestado',
    multa NUMERIC(10, 2) DEFAULT 0.00
);

-- Insertar usuario administrador por defecto
INSERT INTO usuario (nombre_del_usuario, contrasena) 
VALUES ('admin', 'admin')
ON CONFLICT (nombre_del_usuario) DO NOTHING;
```
