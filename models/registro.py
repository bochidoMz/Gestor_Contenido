from flask import Blueprint, render_template, request, redirect, url_for
from flask_bcrypt import Bcrypt
import Conexion.config as db


registro_usu = Blueprint('registro_usu', __name__)

@registro_usu.route('/registro', methods=['GET'])
def mostrarFormularioRegistro():
    return render_template('Registrarse.html')

@registro_usu.route('/user', methods=['POST'])
def addUser():
    nombre = request.form['Nombre']
    apellido = request.form['Apellido']
    email = request.form['Correo']
    contraseña = request.form['Contraseña']
    rol_str = request.form['Rol']  # Ahora obtienes directamente el valor del formulario
    
    rol_mapping = {'usuario': 1, 'admin': 2, 'manager': 3}
    rol = rol_mapping.get(rol_str)

    if rol is None:
        return render_template('Registrarse.html', message="Rol no válido")


    if nombre and apellido and email and contraseña:
        cursor = db.conection.cursor()

        # Insertar usuario en la tabla 'usuario'
        sql_usuario = "INSERT INTO usuario (nombreU, apellidoU, idRol) VALUES (%s, %s, %s);"
        data_usuario = (nombre, apellido, rol)
        cursor.execute(sql_usuario, data_usuario)

        # Obtener el ID del usuario recién insertado
        id_usuario = cursor.lastrowid

        # Insertar datos de login asociados al nuevo usuario en la tabla 'login'
        sql_login = "INSERT INTO login (correoElectronico, contraseña, idUsuario) VALUES (%s, %s, %s);"
        data_login = (email, contraseña, id_usuario)
        cursor.execute(sql_login, data_login)

        db.conection.commit()

        return redirect(url_for('task'))
    else:
        return render_template('Registrarse.html', message="Por favor, completa todos los campos.")

