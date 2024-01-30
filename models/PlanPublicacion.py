from flask import Blueprint, render_template, request, redirect, url_for
import Conexion.config as db

registro_plan = Blueprint('registro_plan', __name__)


@registro_plan.route('/agregar_plan', methods=['POST'])
def agregar_plan():
        # Obtener datos del formulario
        nPlan = request.form['nPlan']
        descripcion = request.form['descripcion']
        costo = request.form['costo']
        observaciones = request.form['observaciones']

        # Insertar plan en la tabla 'planPublicacion'
        cursor = db.conection.cursor()
        sql_plan = "INSERT INTO planPublicacion (nPlan, descripcion, costo, observaciones) VALUES (%s, %s, %s, %s);"
        data_plan = (nPlan, descripcion, costo, observaciones)
        try:
            cursor.execute(sql_plan, data_plan)
            db.conection.commit()
        except Exception as e:
            print(f"Error al insertar en la base de datos: {str(e)}")
            db.conection.rollback()
        finally:
            cursor.close

        return  redirect (url_for('admin'))
