from flask import Blueprint, render_template, request, redirect, url_for
import Conexion.config as db

empresa_plan = Blueprint('empresa_plan', __name__)

@empresa_plan.route('/plan_empresa', methods= ['POST'])
def plan_empresa():
    id_empresas = request.form.getlist('empresa')
    id_plan_publicacion = request.form.get('plan_publicacion')
    fecha_inicio = request.form.get('fecha_inicio')
    fecha_fin = request.form.get('fecha_fin')
    objetivo = request.form.get('objetivo')
    
    cursor = db.conection.cursor()
    
    try:
        for id_empresa in id_empresas:
            sql_empresa_plan = "INSERT INTO empresaPlan (idEmpresa, idPlanPublicacion, fechaInicioContrato, fechafinContrato, ObjetivoPrincipal) VALUES (%s, %s, %s, %s, %s);"
            data_empresa_plan = (id_empresa, id_plan_publicacion,fecha_inicio,fecha_fin,objetivo)
            cursor.execute(sql_empresa_plan, data_empresa_plan)
        
        db.conection.commit()
        return redirect(url_for('admin'))
    except Exception as e:
        print(f"Error al insertar datos en la tabla empresa plan: {str(e)}")
        db.conection.rollback()
        return "error al agregar empresa plan", 500
    finally:
        cursor.close()
    
    
    
    