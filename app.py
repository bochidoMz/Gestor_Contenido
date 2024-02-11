from flask import Flask, render_template, request, redirect,url_for, session
import Conexion.config as db
import secrets
from models.registro import registro_usu
from models.PlanPublicacion import registro_plan
from models.registroEmpresa import registro_empresa
from models.empresaplan import empresa_plan

app = Flask(__name__)
app.secret_key = secrets.token_bytes(16)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    cur = db.conection.cursor(dictionary=True)
    query = "SELECT u.id, u.nombreU, u.apellidoU, u.idRol, l.contraseña FROM usuario u JOIN login l ON u.id = l.idUsuario WHERE l.correoElectronico = %s"
    cur.execute(query, (email,))

    user = cur.fetchone()
    cur.close()

    if user and user['contraseña'] == password:
        session['email'] = email
        session['name'] = user['nombreU']
        session['surnames'] = user['apellidoU']

        if user['idRol'] == 1:
            return redirect(url_for('task'))
        elif user['idRol'] == 2:
            return redirect(url_for('admin'))
        elif user['idRol'] == 3:
            return redirect(url_for('manager'))
        else:
            return render_template('index.html', message=" Rol no reconocido")

    else:
        return render_template('index.html', message="    Las credenciales no son correctas")
    
#esto es para dirigirnos a la tarea de usuario  

@app.route('/tasks', methods = ['GET'])
def task():
    
        # Verificar si el usuario está autenticado
    if 'email' not in session:
        return redirect(url_for('home'))  # Redirigir al inicio de sesión si el usuario no está autenticado

    # Obtener el ID del usuario actualmente autenticado
    email = session['email']
    cur = db.conection.cursor(dictionary=True)
    query = "SELECT id FROM login WHERE correoElectronico = %s"
    cur.execute(query, (email,))
    user_id = cur.fetchone()['id']
    cur.close()

    # Consulta para obtener las tareas asignadas al usuario con detalles de empresa asociada y plan de publicación
    cur = db.conection.cursor(dictionary=True)
    query = query = """
    SELECT 
        t.id, 
        t.fechaInicio, 
        t.fechaFin, 
        t.contenido, 
        ep.descripcion AS descripcionEstadoPublicacion, 
        ea.nombreEmp AS empresaAsociada, 
        pp.descripcion AS planPublicacion 
    FROM tarea t
    LEFT JOIN empresaAsociada ea ON t.idEmpresaAsociada = ea.id
    LEFT JOIN planPublicacion pp ON t.idPlanPublicacion = pp.id
    LEFT JOIN estadoPublicacion ep ON t.idEstadoPublicacion = ep.id
    WHERE t.idUsuario = %s
"""
    cur.execute(query, (user_id,))
    tareas = cur.fetchall()
    cur.close()

    
    return render_template('tasks.html', tareas=tareas)

#esto es para dirigirnos al perfil del Administrador

@app.route('/admin', methods=['GET'])
def admin():
    cursor = db.conection.cursor()

    # Consulta para obtener la lista de empresas
    cursor.execute("SELECT nombreEmp, infoContacto, Email, Telefono, Direccion, modeloNegocio, DireccionRedesSociales, DireccionPáginaWeb FROM empresaAsociada;")
    companies_result = cursor.fetchall()

    # Formatear los resultados de las empresas
    companies = []
    column_names = [column[0] for column in cursor.description]
    for record in companies_result:
        companies.append(dict(zip(column_names, record)))

    cursor.close()

    return render_template('admin.html', companies=companies)

#esto es para dirigirnos al perfil del Manager

@app.route('/manager', methods = ['GET'])
def manager():
    return render_template('manager.html')

#esto es para dirigirnos a los usuarios del admin

@app.route('/admin/usuarios', methods=['GET'])
def usuarios():
    cursor = db.conection.cursor()

    # Consulta para obtener la lista de usuarios
    cursor.execute("SELECT u.id, u.nombreU, u.apellidoU, l.correoElectronico, r.descripcion AS rol \
                    FROM usuario u \
                    INNER JOIN login l ON u.id = l.idUsuario \
                    INNER JOIN rol r ON u.idRol = r.id \
                    WHERE u.idRol != 2;")
    users_result = cursor.fetchall()

    # Formatear los resultados de los usuarios
    users = []
    column_names = [column[0] for column in cursor.description]
    for record in users_result:
        users.append(dict(zip(column_names, record)))

    cursor.close()
    return render_template('usuarios.html', users=users)

@app.route('/admin/planes', methods=['GET'])
def planes():
     return render_template('planes.html')
    
@app.route('/logout') #esto es para el cierre de cesion
def logout():
    session.clear()
    return redirect(url_for('home')) 


@app.route('/registro', methods = ['GET'])
def registro():
    return render_template('Registrarse.html')

app.register_blueprint(registro_usu)
app.register_blueprint(registro_plan, url_prefix='/registro_plan')
app.register_blueprint(registro_empresa)
app.register_blueprint(empresa_plan)





if __name__ == ('__main__'):
        app.run(debug=True)

