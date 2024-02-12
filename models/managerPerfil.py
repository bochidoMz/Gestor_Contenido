from flask import Blueprint, render_template, request, redirect, url_for
import Conexion.config as db

manager_perfil = Blueprint('managerPerfil', __name__)

@manager_perfil.route('/insertar_empresa_plan', methods=['POST'])
def insertar_empresa_plan():
    if request.method == 'POST':
        id_empresa = request.form['idEmpresa']
        id_plan_publicacion = request.form['planPublicacion']
        fecha_inicio_contrato = request.form['fechaInicio']
        fecha_fin_contrato = request.form['fechaFin']
        objetivo_principal = request.form['objetivo']

        cursor = db.conection.cursor()

        # Verificar si la empresa existe en la base de datos
        cursor.execute("SELECT id FROM empresaAsociada WHERE id = %s", (id_empresa,))
        empresa_row = cursor.fetchone()
        if empresa_row:
            # Si la empresa existe, continuar con la inserción en la tabla empresaPlan
            # Insertar los datos en la tabla empresaPlan
            sql_insert = "INSERT INTO empresaPlan (idEmpresa, idPlanPublicacion, fechaInicioContrato, fechafinContrato, ObjetivoPrincipal) VALUES (%s, %s, %s, %s, %s)"
            data = (id_empresa, id_plan_publicacion, fecha_inicio_contrato, fecha_fin_contrato, objetivo_principal)

            try:
                cursor.execute(sql_insert, data)
                db.conection.commit()
                # Puedes imprimir un mensaje de éxito si lo deseas
                print("Los datos se han guardado correctamente en la base de datos.")
            except Exception as e:
                print(f"Error al insertar datos en la tabla empresaPlan: {str(e)}")
                db.conection.rollback()
                # Puedes imprimir un mensaje de error si lo deseas
                print("Error al guardar los datos en la base de datos.")
            finally:
                cursor.close()
        else:
            # Si la empresa no existe, imprimir un mensaje de error
            print("No se encontró la empresa en la base de datos.")
            # Puedes imprimir un mensaje de error si lo deseas
            print("No se encontró la empresa en la base de datos.")

        # No devolver ninguna redirección, lo que mantendrá al usuario en la misma página
        return redirect(url_for('manager'))




            
            









