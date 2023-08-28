from flask import Flask, jsonify, request
import mysql.connector
from datetime import date

app = Flask(__name__)


config = {
    'user': 'root',
    'password': 'linux123',
    'host': 'localhost',
    'database': 'R12'
}

@app.route('/users', methods=['GET'])
def get_usuarios():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    query = "SELECT * FROM login"
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()
    cnx.close()
    return jsonify(users)

@app.route('/add-user', methods=['POST'])
def add_user():
    # Obteniendo datos del cuerpo de la petición
    nombre_usuario = request.json['nombre_usuario']
    Email = request.json['Email']
    Contraseña = request.json['Contraseña']
    fecha_vencimiento = request.json['fecha_vencimiento']

    # Asegurarnos que la fecha de vencimiento sea válida
    if fecha_vencimiento < str(date.today()):
        return jsonify({"error": "La fecha de vencimiento debe ser hoy o una fecha futura"}), 400

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = """INSERT INTO login (nombre_usuario, Email, Contraseña, fecha_vencimiento)
                   VALUES (%s, %s, %s, %s)"""
        cursor.execute(query, (nombre_usuario, Email, Contraseña, fecha_vencimiento))
        cnx.commit()
        cursor.close()
        cnx.close()
        return jsonify({"message": "Usuario registrado con éxito"}), 201

    except mysql.connector.Error as err:
        return jsonify({"error": "Error en la base de datos: {}".format(err)}), 500

@app.route('/login', methods=['POST'])
def login():
    Email = request.json['Email']
    Contraseña = request.json['Contraseña']

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    query = "SELECT * FROM login WHERE Email = %s AND Contraseña = %s"
    cursor.execute(query, (Email, Contraseña))
    user = cursor.fetchone()
    cursor.close()
    cnx.close()

    if user:
        return jsonify({"message": "Login successful", "email": user['Email']}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401

@app.route('/update-user', methods=['PUT'])
def update_user():
    Email = request.json['Email']
    nombre_usuario = request.json.get('nombre_usuario', None)
    Contraseña = request.json.get('Contraseña', None)
    fecha_vencimiento = request.json.get('fecha_vencimiento', None)

    updates = []
    params = []

    if nombre_usuario:
        updates.append("nombre_usuario = %s")
        params.append(nombre_usuario)
    if Contraseña:
        updates.append("Contraseña = %s")
        params.append(Contraseña)
    if fecha_vencimiento:
        updates.append("fecha_vencimiento = %s")
        params.append(fecha_vencimiento)
    
    params.append(Email)
    query = f"UPDATE login SET {', '.join(updates)} WHERE Email = %s"

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    cursor.execute(query, tuple(params))
    cnx.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    cnx.close()

    if affected_rows:
        return jsonify({"message": "User updated successfully"}), 200
    else:
        return jsonify({"message": "User not found or no changes were made"}), 404

@app.route('/delete-user', methods=['DELETE'])
def delete_user():
    Email = request.json['Email']

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = "DELETE FROM login WHERE Email = %s"
    cursor.execute(query, (Email,))
    cnx.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    cnx.close()

    if affected_rows:
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404

@app.route('/sucursales', methods=['GET'])
def get_sucursales():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    query = "SELECT * FROM Sucursal"
    cursor.execute(query)
    sucursales = cursor.fetchall()
    cursor.close()
    cnx.close()
    return jsonify(sucursales)

@app.route('/add-sucursal', methods=['POST'])
def add_sucursal():
    nombre = request.json['nombre']
    ciudad = request.json.get('ciudad', None)
    municipio = request.json.get('municipio', None)
    gmail = request.json.get('gmail', None)
    encargado = request.json.get('encargado', None)
    telefono = request.json.get('telefono', None)
    descripcion = request.json.get('descripcion', None)
    Id_vendedor = request.json.get('Id_vendedor', None)
    
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = """INSERT INTO Sucursal(nombre, ciudad, municipio, gmail, encargado, telefono, descripcion, Id_vendedor) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, (nombre, ciudad, municipio, gmail, encargado, telefono, descripcion, Id_vendedor))
    cnx.commit()
    cursor.close()
    cnx.close()
    return jsonify({"message": "Sucursal added successfully"}), 201

@app.route('/productos', methods=['GET'])
def get_productos():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(dictionary=True)
    query = "SELECT * FROM producto"
    cursor.execute(query)
    productos = cursor.fetchall()
    cursor.close()
    cnx.close()
    return jsonify(productos)

@app.route('/add-producto', methods=['POST'])
def add_producto():
    nombre = request.json['nombre']
    precio_compra = request.json['precio_compra']
    precio_venta = request.json['precio_venta']
    descripcion = request.json.get('descripcion', None)
    stock = request.json['stock']
    valoracion = request.json.get('valoracion', None)
    id_sucursal = request.json.get('id_sucursal', None)
    
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = """INSERT INTO producto(nombre, precio_compra, precio_venta, descripcion, stock, valoracion, id_sucursal) 
               VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, (nombre, precio_compra, precio_venta, descripcion, stock, valoracion, id_sucursal))
    cnx.commit()
    cursor.close()
    cnx.close()
    return jsonify({"message": "Producto added successfully"}), 201


if __name__ == "__main__":
    app.run(debug=True)