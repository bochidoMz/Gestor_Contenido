from flask import Blueprint, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import DateField
import Conexion.config as db

registro_empresa = Blueprint('registro_empresa', __name__)

@registro_empresa.route('/agregar_empresa', methods=['POST'])
def agregar_empresa():
   
    # Obtener datos del formulario
    nombreEmp = request.form['nombreEmp']
    infoContacto = request.form['infoContacto']
    idPlanPublicacion = request.form['idPlanPublicacion']
    fechaInicioContrato = request.form['fechaInicioContrato']
    fechaFinContrato = request.form['fechaFinContrato']
    modeloNegocio = request.form['modeloNegocio']
    requerimientoPrincipal = request.form['requerimientoPrincipal']

    # Insertar empresa en la tabla 'empresaAsociada'
    cursor = db.conection.cursor()
    sql_empresa = "INSERT INTO empresaAsociada (nombreEmp, infoContacto, idPlanPublicacion, fechaInicioContrato, fechaFinContrato, modeloNegocio, requerimientoPrincipal) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    data_empresa = (nombreEmp, infoContacto, idPlanPublicacion, fechaInicioContrato, fechaFinContrato, modeloNegocio, requerimientoPrincipal)
    
    cursor.execute(sql_empresa, data_empresa)
    db.conection.commit()
    
    
    
    return redirect(url_for('task'))
       
    
     