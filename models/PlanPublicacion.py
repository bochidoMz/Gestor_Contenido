from flask import Blueprint, render_template, request, redirect, url_for
import Conexion.config as db

registro_plan = Blueprint('registro_plan', __name__)


@registro_plan.route('/agregar_plan', methods=['POST'])
def agregar_plan():
        # Obtener datos del formulario
        nPlan = request.form['nPlan']
        descripcion = request.form['descripcion']
        costo = request.form['costo']
        

        # Insertar plan en la tabla 'planPublicacion'
        cursor = db.conection.cursor()
        sql_plan = "INSERT INTO planPublicacion (nPlan, descripcion, costo) VALUES (%s, %s, %s);"
        data_plan = (nPlan, descripcion, costo)
        try:
            cursor.execute(sql_plan, data_plan)
            db.conection.commit()
        except Exception as e:
            print(f"Error al insertar en la base de datos: {str(e)}")
            db.conection.rollback()
        finally:
            cursor.close

        return  redirect (url_for('planes'))


@registro_plan.route('/edit_plan/<int:id>', methods=['POST','GET'])
def edit_plan(id):
    if request.method == 'POST':
        # Obtener datos del formulario
        nPlan = request.form['nPlan']
        descripcion = request.form['descripcion']
        costo = request.form['costo']

        cursor = db.conection.cursor()
        # Actualizar los datos del plan en la base de datos
        sql_update = "UPDATE planPublicacion SET nPlan = %s, descripcion = %s, costo = %s WHERE id = %s"
        data_update = (nPlan, descripcion, costo, id)
        try:
            cursor.execute(sql_update, data_update)
            db.conection.commit()
            message = 'Plan actualizado correctamente'
            message_type = 'success'
        except Exception as e:
            print(f"Error al actualizar plan: {str(e)}")
            db.conection.rollback()
            message = 'Error al actualizar plan'
            message_type = 'danger'
        finally:
            cursor.close()

        return redirect(url_for('planes'))


@registro_plan.route('/delete_plan/<int:id>', methods=['POST'])
def delete_plan(id):
    cursor = db.conection.cursor()

    try:
        # Eliminar el plan
        sql_plan = "DELETE FROM planPublicacion WHERE id = %s"
        cursor.execute(sql_plan, (id,))
        db.conection.commit()

        message = 'Plan eliminado exitosamente'
        message_type = 'success'
    except Exception as e:
        print(f"Error al eliminar plan: {str(e)}")
        db.conection.rollback()
        message = 'Error al eliminar el plan'
        message_type = 'danger'
    finally:
        cursor.close()

    return redirect(url_for('planes'))
