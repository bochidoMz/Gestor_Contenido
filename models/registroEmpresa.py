from flask import Blueprint, flash, render_template, request, redirect, url_for
import Conexion.config as db

registro_empresa = Blueprint('registro_empresa', __name__)

@registro_empresa.route('/agregar_empresa', methods=['POST'])
def agregar_empresa():
    # Obtener datos del formulario
    nombreEmp = request.form['nombreEmp']
    infoContacto = request.form['infoContacto']
    email = request.form['Email']
    telefono = request.form['Telefono']
    direccion = request.form['Direccion']
    modeloNegocio = request.form['modeloNegocio']
    idPlataforma = request.form['idPlataforma']  # Nuevo campo para la plataforma seleccionada

    # Insertar empresa en la tabla 'empresaAsociada'
    cursor = db.conection.cursor()
    sql_empresa = "INSERT INTO empresaAsociada (nombreEmp, infoContacto, Email, Telefono, Direccion, modeloNegocio, idPlataforma) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    data_empresa = (nombreEmp, infoContacto, email, telefono, direccion, modeloNegocio, idPlataforma)
    
    try:
        cursor.execute(sql_empresa, data_empresa)
        db.conection.commit()
        message = 'Empresa agregada con éxito'
        message_type = 'success'  # Mensaje de éxito
    except Exception as e:
        print(f"Error al insertar en la tabla de empresa: {str(e)}")
        db.conection.rollback()  # Corregir el llamado a rollback()
        message = 'Error al agregar la empresa'
        message_type = 'danger'  # Mensaje de error
    finally:
        cursor.close()

    return redirect(url_for('admin'))
       
#Ruta para eliminar 
@registro_empresa.route('/delete/<int:id>')
def delete_empresa(id):
    
    cursor = db.conection.cursor()
    sql_empresa = "DELETE FROM empresaAsociada WHERE id = %s"
    data = (id,)
    cursor.execute(sql_empresa,data)
      
    return redirect(url_for('admin'))

#Editar empresa

@registro_empresa.route('/edit_empresa/<int:id>', methods=['POST'])
def edit_empresa(id):
    if request.method == 'POST':
        # Obtener datos del formulario
        nombreEmp = request.form['nombreEmp']
        infoContacto = request.form['infoContacto']
        email = request.form['email']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        modeloNegocio = request.form['modeloNegocio']

        cursor = db.conection.cursor()
        # Actualizar los datos de la empresa en la base de datos
        sql_update = "UPDATE empresaAsociada SET nombreEmp = %s, infoContacto = %s, Email = %s, Telefono = %s, Direccion = %s, modeloNegocio = %s WHERE id = %s"
        data_update = (nombreEmp, infoContacto, email, telefono, direccion, modeloNegocio, id)
        try:
            cursor.execute(sql_update, data_update)
            db.conection.commit()
            message = 'Empresa actualizada correctamente'
            message_type = 'success'
        except Exception as e:
            print(f"Error al actualizar empresa: {str(e)}")
            db.conection.rollback()
            message = 'Error al actualizar empresa'
            message_type = 'danger'
        finally:
            cursor.close()

        return redirect(url_for('admin'))



     