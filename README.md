Para que el programa funcione debe tener estos nombres tal cual
Base de datos: Biblioteca
Host: localhost
Puerto: 5432
Usuario: postgres
Contraseña: 1234

--------------------------------------------------------------
Nombre de la tabla: usuario
Columnas:
nombre_del_usuario (Tipo: character varying / texto)
contrasena (Tipo: character varying / texto)

--------------------------------------------------------------
Nombre de la tabla: empleado
Columnas:
codigo (Tipo: integer, debe ser la Llave Primaria / Primary Key)
nombre (Tipo: character varying, ej. longitud 100)
direccion (Tipo: character varying, ej. longitud 150)
telefono (Tipo: character varying, ej. longitud 20)
sexo (Tipo: character, longitud 1, para "M" o "F")
fecha_nac (Tipo: date)
turno (Tipo: character varying, ej. longitud 20)
----------------------------------------------------
