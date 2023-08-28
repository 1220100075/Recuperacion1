Drop database R12;
create database R12;
use R12;

CREATE TABLE login (
	Id INT auto_increment PRIMARY KEY,
    nombre_usuario VARCHAR(255) NOT NULL,
    Email VARCHAR(100),
    Contraseña varchar(20),
    fecha_registro timestamp default current_timestamp,
    fecha_vencimiento date
);

    CREATE TABLE Sucursal (
    Id INT auto_increment PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    ciudad VARCHAR(100),
    municipio VARCHAR(100),
    gmail VARCHAR(255),
    encargado VARCHAR(255),
    telefono VARCHAR(20),
    descripcion TEXT,
    Id_vendedor int,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (Id_vendedor) REFERENCES login(Id)
);

    CREATE TABLE producto (
    id INT auto_increment PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    precio_compra DECIMAL(10, 2) NOT NULL,
    precio_venta DECIMAL(10, 2) NOT NULL,
    descripcion TEXT,
    stock INT NOT NULL,
    valoracion FLOAT,
    id_sucursal INT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_sucursal) REFERENCES Sucursal(Id)
);

select * from login;

INSERT INTO login2 (Id, nombre, Email, Contraseña, fecha_registro, fecha_vencimiento)
VALUES (1, 'prueba1', 'prueba1.com', 'password123', CURRENT_TIMESTAMP, '2023-12-31');
