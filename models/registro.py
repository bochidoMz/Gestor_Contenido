from flask import Blueprint, render_template, request, redirect, url_for
from flask import redirect, url_for, session
import Conexion.config as db


registro_usu = Blueprint('registro_usu', __name__)

@registro_usu.route('/registro', methods=['GET'])
def mostrarFormularioRegistro():
    return render_template('usuarios.html')

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
        return render_template('usuarios.html', message="Rol no válido")


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
        cursor.close()  # Cierra el cursor después de ejecutar las consultas

        session['email'] = email
        session['name'] = nombre
        session['surnames'] = apellido

        # Redirigir nuevamente al formulario de registro
        return redirect(url_for('usuarios'))
    else:
        return render_template('usuarios.html', message="Por favor, completa todos los campos.")
    
    #Metodo Borrar
    
@registro_usu.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_user(id):
        
            cursor = db.conection.cursor()

            # Elimina primero los registros relacionados en la tabla login
            sql_login = "DELETE FROM login WHERE idUsuario = %s"
            cursor.execute(sql_login, (id,))
            db.conection.commit()

            # Luego elimina al usuario de la tabla usuario
            sql_usuario = "DELETE FROM usuario WHERE id = %s"
            cursor.execute(sql_usuario, (id,))
            db.conection.commit()

            cursor.close()

            return redirect(url_for('usuarios'))   
  # Redirige a la vista de usuarios después de eliminar

# Agrega el método para editar usuarios
@registro_usu.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    if request.method == 'POST':
        nombre = request.form['Nombre']
        apellido = request.form['Apellido']
        email = request.form['Correo']
        contraseña = request.form['Contraseña']
        rol = request.form['Rol']
        
        cursor = db.conection.cursor()
        # Actualizar tabla 'usuario'
        sql_usuario = "UPDATE usuario SET nombreU = %s, apellidoU = %s WHERE id = %s"
        cursor.execute(sql_usuario, (nombre, apellido, id))

        # Actualizar tabla 'login'
        sql_login = "UPDATE login SET correoElectronico = %s, contraseña = %s WHERE idUsuario = %s"
        cursor.execute(sql_login, (email, contraseña, id))

        db.conection.commit()
        cursor.close()
            
        # Redirigir a la página de usuarios después de la actualización exitosa
        return redirect(url_for('usuarios'))  
       
    else:
        cursor = db.conection.cursor()
        sql = "SELECT u.id, u.nombreU, u.apellidoU, l.correoElectronico, r.descripcion AS rol FROM usuario u \
               INNER JOIN login l ON u.id = l.idUsuario \
               INNER JOIN rol r ON u.idRol = r.id \
               WHERE u.id = %s"
        cursor.execute(sql, (id,))
        user = cursor.fetchone()
        cursor.close()
        return render_template('usuarios.html', user=user)

        
    





    


