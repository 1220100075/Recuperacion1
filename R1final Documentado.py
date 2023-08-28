from flask import Flask, jsonify, request   #Importa las clases necesarias de Flask para crear una aplicación web, manejar respuestas en formato JSON y manejar solicitudes HTTP.
import mysql.connector  # Importa el módulo necesario para conectarse y realizar consultas a una base de datos MySQL
from datetime import date  # Importa la clase date desde el módulo datetime, que puede ser utilizada para trabajar con fechas

app = Flask(__name__) #Crea una instancia de la aplicación Flask. El parámetro __name__ es una referencia al módulo actual.

#conexion con la base de datos
#contiene la información necesaria para establecer una conexión con la base de datos MySQL. Esto incluye el usuario, contraseña, dirección del host y nombre de la base de datos.
config = {
    'user': 'root', #usuario
    'password': 'linux123', #Contraseña
    'host': 'localhost', # o 127.0.0.1
    'database': 'R12' #nombre de la base de datos.
}

#lista de usuarios

@app.route('/users', methods=['GET'])  #Define una ruta en la aplicación web. Cuando se accede a esta ruta usando el método HTTP GET
def get_usuarios(): #Esta función se ejecutará cuando se realice una solicitud GET a la ruta '/users'
    cnx = mysql.connector.connect(**config) #Se establece una conexión con la base de datos MySQL utilizando la información proporcionada en el diccionario config.
    cursor = cnx.cursor(dictionary=True) #indica que las filas de resultados se devolverán como diccionarios en lugar de tuplas.
    query = "SELECT * FROM login" #Se define una consulta SQL para seleccionar todos los registros de la tabla
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()
    cnx.close()
    return jsonify(users)  #Se devuelve una respuesta JSON que contiene la lista de usuarios obtenidos de la base de datos.

#agregar usuarios

@app.route('/add-user', methods=['POST'])  #Define una nueva ruta en la aplicación web para recibir solicitudes POST que agreguen un nuevo usuario.
def add_user(): #Esta función se ejecutará cuando se realice una solicitud POST a la ruta '/add-user'
    # Obteniendo datos del cuerpo de la petición
    nombre_usuario = request.json['nombre_usuario'] #  Los datos del cuerpo de la solicitud se obtienen utilizando request.json. Los campos incluyen 
    Email = request.json['Email']  #nombre_usuario, Email, Contraseña y fecha_vencimiento
    Contraseña = request.json['Contraseña']
    fecha_vencimiento = request.json['fecha_vencimiento']

    # Asegurarnos que la fecha de vencimiento sea válida
    #Se verifica si la fecha de vencimiento proporcionada es una fecha futura o igual al día actual. 
    #Si no lo es, se devuelve un mensaje de error
    if fecha_vencimiento < str(date.today()):
        return jsonify({"error": "La fecha de vencimiento debe ser hoy o una fecha futura"}), 400
#Se intenta establecer una conexión con la base de datos y se insertan los datos del nuevo usuario en la tabla login
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = """INSERT INTO login (nombre_usuario, Email, Contraseña, fecha_vencimiento)
                   VALUES (%s, %s, %s, %s)"""
        cursor.execute(query, (nombre_usuario, Email, Contraseña, fecha_vencimiento))
        cnx.commit()
        cursor.close()
        cnx.close()
        return jsonify({"message": "Usuario registrado con éxito"}), 201                #Si la operación es exitosa, se confirma la transacción, se cierra el cursor y la conexión, y 
                                                                                         #se devuelve un mensaje de éxito en formato JSON.
    except mysql.connector.Error as err:
        return jsonify({"error": "Error en la base de datos: {}".format(err)}), 500     # Si ocurre un error en la base de datos, se devuelve un mensaje de error con el código de estado 500
    
    
    #inicio de sesion

@app.route('/login', methods=['POST'])   #Define una ruta para recibir solicitudes POST para el inicio de sesión.
def login():   #Se ejecuta cuando se realiza una solicitud POST a la ruta '/login'.
    Email = request.json['Email']
    Contraseña = request.json['Contraseña']  #Los datos del cuerpo de la solicitud (correo electrónico y contraseña) se obtienen de request.json

    cnx = mysql.connector.connect(**config)  #Se establece una conexión con la base de datos y se realiza una consulta para verificar 
    cursor = cnx.cursor(dictionary=True)     #si las credenciales proporcionadas coinciden con un usuario en la base de datos
    query = "SELECT * FROM login WHERE Email = %s AND Contraseña = %s"
    cursor.execute(query, (Email, Contraseña))     
    user = cursor.fetchone()                       
    cursor.close()                                 
    cnx.close()

    if user:
        return jsonify({"message": "Ingreso Correcto", "email": user['Email']}), 200 #Si se encuentra un usuario, se devuelve un mensaje de éxito junto con el correo electrónico del usuario en formato JSON y un código de estado 200.
    else:
        return jsonify({"message": "Usuario o contraseña Incorrecto"}), 401  # Si no se encuentra un usuario, se devuelve un mensaje de error con el código de estado 401.
    
    #actualizar datos de usuarios

@app.route('/update-user', methods=['PUT'])  # Define una nueva ruta en la aplicación web para recibir solicitudes PUT que actualicen la información de un usuario existente.
def update_user():    # Esta función se ejecutará cuando se realice una solicitud PUT a la ruta '/update-user'
    Email = request.json['Email']                              #Los datos del cuerpo de la solicitud se obtienen utilizando request.json. 
    nombre_usuario = request.json.get('nombre_usuario', None)   #El campo obligatorio es Email, y los campos opcionales son nombre_usuario, Contraseña y fecha_vencimiento
    Contraseña = request.json.get('Contraseña', None)
    fecha_vencimiento = request.json.get('fecha_vencimiento', None)
#Se inicializan listas updates y params para almacenar las cláusulas SET de la consulta SQL y sus valores asociados.
    updates = []
    params = []

    if nombre_usuario:                           #Se verifica si los campos opcionales (nombre_usuario, Contraseña 
        updates.append("nombre_usuario = %s")    #y fecha_vencimiento) están presentes en la solicitud. Si lo están, se agregan a las 
        params.append(nombre_usuario)            #listas correspondientes las cláusulas SET con marcadores de posición %s y los valores respectivos.
    if Contraseña:
        updates.append("Contraseña = %s")
        params.append(Contraseña)
    if fecha_vencimiento:
        updates.append("fecha_vencimiento = %s")
        params.append(fecha_vencimiento)
    
    params.append(Email)
    query = f"UPDATE login SET {', '.join(updates)} WHERE Email = %s"  #Se crea una consulta SQL dinámica utilizando las cláusulas SET generadas.
                                                                        # La función join se utiliza para unir las cláusulas con comas y formar una sola cadena.
    cnx = mysql.connector.connect(**config) #Se establece una conexión con la base de datos utilizando la información proporcionada en el diccionario config'
    cursor = cnx.cursor()   #Se crea un cursor para ejecutar consultas en la base de datos
    cursor.execute(query, tuple(params)) #La consulta SQL dinámica se ejecuta utilizando el cursor y los valores de los parámetros se pasan como una tupla.
    cnx.commit()                           #Se confirma la transacción en la base de datos y se obtiene la cantidad de filas afectadas.
    affected_rows = cursor.rowcount
    cursor.close()  #Se cierra el cursor y la conexión a la base de datos
    cnx.close()
#Se verifica si se actualizaron filas en la base de datos (affected_rows). 
    if affected_rows:
        return jsonify({"message": "El usuario se a actualizado correctamente"}), 200  #Si se actualizó al menos una fila, se devuelve un mensaje de éxito con un código de estado 200
    else:
        return jsonify({"message": "Usuario no encontrado o no se realizaron cambios"}), 404 #Si no se encontró un usuario con el correo electrónico proporcionado o no se realizaron 
                                                                                         #cambios en los campos, se devuelve un mensaje de error con un código de estado 404
  #eliminacion de usuario  

@app.route('/delete-user', methods=['DELETE']) #Define una nueva ruta en la aplicación web para recibir solicitudes DELETE que eliminen un usuario existente.
def delete_user():   #Esta función se ejecutará cuando se realice una solicitud DELETE a la ruta '/delete-user'
    Email = request.json['Email'] #El dato necesario para identificar el usuario que se desea eliminar se obtiene del cuerpo de la solicitud mediante request.json. En este caso, se utiliza el campo Email

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()  #Se crea un cursor para ejecutar consultas en la base de datos
    query = "DELETE FROM login WHERE Email = %s"   #Se crea una consulta SQL para eliminar el usuario con el correo electrónico especificado
    cursor.execute(query, (Email,))  #La consulta SQL se ejecuta utilizando el cursor, y se confirma la transacción en la base de datos.
    cnx.commit()  #Se obtiene la cantidad de filas afectadas por la eliminación
    affected_rows = cursor.rowcount
    cursor.close()  #Se cierra el cursor y la conexión a la base de datos.
    cnx.close()

    if affected_rows:
        return jsonify({"message": "El usuario se a eliminado correctamente"}), 200 #Si se eliminó al menos una fila, se devuelve un mensaje de éxito con un código de estado 200.
    else:
        return jsonify({"message": "Usuario no encontrado"}), 404 #Si no se encontró un usuario con el correo electrónico proporcionado para eliminar, se devuelve un mensaje de error con un código de estado 404.
    
 #listado de sucursales   

@app.route('/sucursales', methods=['GET']) #Define una nueva ruta en la aplicación web para recibir solicitudes GET que obtengan la lista de sucursales desde la base de datos.
def get_sucursales():  #Esta función se ejecutará cuando se realice una solicitud GET a la ruta '/sucursales'
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    query = "SELECT * FROM Sucursal" #Se define una consulta SQL para seleccionar todos los registros de la tabla "Sucursal".
    cursor.execute(query) #La consulta SQL se ejecuta utilizando el cursor, y se obtienen todas las sucursales de la base de datos.
    sucursales = cursor.fetchall()
    cursor.close() #Se cierra el cursor y la conexión a la base de datos
    cnx.close()
    return jsonify(sucursales)  #Se devuelve una respuesta JSON que contiene la lista de sucursales obtenidas de la base de datos

#creacion de sucursales

@app.route('/add-sucursal', methods=['POST']) #Define una nueva ruta en la aplicación web para recibir solicitudes POST que creen y agreguen una nueva sucursal en la base de datos.
def add_sucursal():  #Esta función se ejecutará cuando se realice una solicitud POST a la ruta '/add-sucursal'
    nombre = request.json['nombre'] #  Los datos del cuerpo de la solicitud se obtienen utilizando request.json. Los campos obligatorios son nombre,
    ciudad = request.json.get('ciudad', None)  # mientras que los demás campos (ciudad, municipio, gmail, encargado, telefono, descripcion y Id_vendedor) son opcionales.
    municipio = request.json.get('municipio', None)
    gmail = request.json.get('gmail', None)
    encargado = request.json.get('encargado', None)
    telefono = request.json.get('telefono', None)
    descripcion = request.json.get('descripcion', None)
    Id_vendedor = request.json.get('Id_vendedor', None)
    
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()  #La consulta SQL se ejecuta utilizando el cursor, y se confirma la transacción en la base de datos.
    query = """INSERT INTO Sucursal(nombre, ciudad, municipio, gmail, encargado, telefono, descripcion, Id_vendedor) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, (nombre, ciudad, municipio, gmail, encargado, telefono, descripcion, Id_vendedor))
    cnx.commit()
    cursor.close()
    cnx.close()
    return jsonify({"message": "La sucursal se a Creado correctamente"}), 201  #Si la inserción en la base de datos es exitosa, se devuelve un mensaje de éxito con un código de estado 201 en formato JSON

#listado de productos

@app.route('/productos', methods=['GET'])  #Define una nueva ruta en la aplicación web para recibir solicitudes GET que obtengan la lista de productos desde la base de datos.
def get_productos(): #Esta función se ejecutará cuando se realice una solicitud GET a la ruta '/productos'.
    cnx = mysql.connector.connect(**config) #Se establece una conexión con la base de datos MySQL utilizando la información proporcionada en el diccionario config
    cursor = cnx.cursor(dictionary=True)
    query = "SELECT * FROM producto"  #Se define una consulta SQL para seleccionar todos los registros de la tabla "producto"
    cursor.execute(query) #
    productos = cursor.fetchall()
    cursor.close() #Se cierra el cursor y la conexión a la base de datos.
    cnx.close()
    return jsonify(productos) #Se devuelve una respuesta JSON que contiene la lista de productos obtenidos de la base de datos.

#agregar productos

@app.route('/add-producto', methods=['POST'])  #Define una nueva ruta en la aplicación web para recibir solicitudes POST que creen y agreguen un nuevo producto en la base de datos
def add_producto():  #Esta función se ejecutará cuando se realice una solicitud POST a la ruta '/add-producto'
    nombre = request.json['nombre']       #Los datos del cuerpo de la solicitud se obtienen utilizando request.json. Los campos obligatorios son nombre, precio_compra, precio_venta y stock.
    precio_compra = request.json['precio_compra'] # Los campos opcionales son descripcion, valoracion e id_sucursal
    precio_venta = request.json['precio_venta']
    descripcion = request.json.get('descripcion', None)
    stock = request.json['stock']
    valoracion = request.json.get('valoracion', None)
    id_sucursal = request.json.get('id_sucursal', None)
    
    cnx = mysql.connector.connect(**config) #Se establece una conexión con la base de datos utilizando la información proporcionada en el diccionario config
    cursor = cnx.cursor() #Se crea un cursor para ejecutar consultas en la base de datos.
    query = """INSERT INTO producto(nombre, precio_compra, precio_venta, descripcion, stock, valoracion, id_sucursal) 
               VALUES (%s, %s, %s, %s, %s, %s, %s)""" #Se define una consulta SQL para insertar los datos del nuevo producto en la tabla "producto"
    cursor.execute(query, (nombre, precio_compra, precio_venta, descripcion, stock, valoracion, id_sucursal))  #La consulta SQL se ejecuta utilizando el cursor, y se confirma la transacción en la base de datos
    cnx.commit()
    cursor.close()#Se cierra el cursor y la conexión a la base de datos
    cnx.close()
    return jsonify({"message": "PRoducto se a creado correctamente"}), 201  #Si la inserción en la base de datos es exitosa, se devuelve un mensaje de éxito con un código de estado 201 en formato JSON


if __name__ == "__main__":  #Esta línea asegura que la siguiente línea de código solo se ejecute cuando el script se ejecuta directamente (no cuando se importa en otro script)
    app.run(debug=True)   #Inicia la aplicación Flask en modo de depuración (debug=True). Esto permite que la aplicación se recargue automáticamente cuando se realizan cambios en el código.