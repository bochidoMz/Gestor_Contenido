from flask import Blueprint, flash, render_template, request, redirect, url_for
import Conexion.config as db

registro_empresa = Blueprint('registro_empresa', __name__)

@registro_empresa.route('/agregar_empresa', methods=['POST'])
def agregar_empresa():
   
    # Obtener datos del formulario
    nombreEmp = request.form['nombreEmp']
    infoContacto = request.form['infoContacto']
    email = request.form['email']
    telefono = request.form['telefono']
    direccion = request.form['direccion']
    modeloNegocio = request.form['modeloNegocio']
    direccionRedesSociales = request.form['direccionRedesSociales']
    direccionPaginaWeb = request.form['direccionPáginaWeb']
    
    # Insertar empresa en la tabla 'empresaAsociada'
    cursor = db.conection.cursor()
    sql_empresa = "INSERT INTO empresaAsociada (nombreEmp, infoContacto, Email, Telefono, Direccion, modeloNegocio, DireccionRedesSociales, DireccionPáginaWeb) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
    data_empresa = (nombreEmp, infoContacto, email, telefono, direccion, modeloNegocio, direccionRedesSociales, direccionPaginaWeb)
    
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
       


     