from flask import Blueprint, render_template, request, redirect, url_for
from flask_bcrypt import Bcrypt
import Conexion.config as db


registro_usu = Blueprint('registro_usu', __name__)

@registro_usu.route('/registro', methods=['GET'])
def mostrarFormularioRegistro():
    return render_template('Registrarse.html')

#Agregar al Usuario

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
    
#Ruta para Listar

@registro_usu.route('/registro')
def Listar():
    cursor = db.conection.cursor()
    cursor.execute("SELECT * FROM usuario")
    myresult = cursor.fetchall()
    
    insertObject = []
    columNames = [column [0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columNames, record)))
    cursor.close()
    return render_template('Registrarse.html', data=insertObject)

#Ruta para eliminar

@registro_usu.route('/delete/<string:id>')
def delete(id):
    cursor = db.conection.cursor()
    sql = "DELETE FROM usuario WHERE id= %s"
    data = (id,)
    cursor.execute(sql, data)
    db.conection.commit()
    return redirect(url_for("Registrarse.html"))

#Ruta para editar

@registro_usu.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    nombre = request.form['Nombre']
    apellido = request.form['Apellido']
    email = request.form['Correo']
    contraseña = request.form['Contraseña']
    rol_str = request.form['Rol']
    
    if nombre and apellido and email and contraseña and rol_str:
        cursor = db.conection.cursor()
        sql = "UPDATE usuario SET nombreU = %s, apellidoU = %s, correoElectronico = %s, contraseña = %s, idRol = %s WHERE id = %s"
        data = (nombre, apellido, email, contraseña, rol_str, id)
        cursor.execute(sql, data)
        db.conection.commit()
        
        return redirect(url_for('Registro.html'))
    


