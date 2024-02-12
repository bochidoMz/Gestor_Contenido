from flask import Flask, render_template, request, redirect,url_for, session
import Conexion.config as db
import secrets
from models.registro import registro_usu
from models.PlanPublicacion import registro_plan
from models.registroEmpresa import registro_empresa
from models.empresaplan import empresa_plan
from models.managerPerfil import manager_perfil

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
  return render_template('tasks.html')

#esto es para dirigirnos al perfil del Administrador

@app.route('/admin', methods=['GET'])
def admin():
    cursor = db.conection.cursor()

    # Consulta para obtener la lista de empresas con información de la plataforma asociada
    cursor.execute("SELECT e.*, p.nombrePlataforma FROM empresaAsociada e INNER JOIN plataforma p ON e.idPlataforma = p.id;")
    companies_result = cursor.fetchall()

    # Formatear los resultados de las empresas
    companies = []
    column_names = [column[0] for column in cursor.description]
    for record in companies_result:
        companies.append(dict(zip(column_names, record)))
        
    # Obtener las plataformas disponibles
    cursor.execute("SELECT * FROM plataforma;")
    plataformas_result = cursor.fetchall()
    plataformas = [dict(id=plataforma[0], nombrePlataforma=plataforma[1]) for plataforma in plataformas_result]

    cursor.close()
    
    print(plataformas)

    return render_template('admin.html', companies=companies, plataformas = plataformas)

#esto es para dirigirnos al perfil del Manager

@app.route('/manager', methods=['GET'])
def manager():
    ultima_empresa = None
    ultimo_plan = None
    todas_empresas = []
    todos_planes = []

    cursor = db.conection.cursor()

    # Obtener la última empresa y el último plan por defecto
    cursor.execute("SELECT id, nombreEmp FROM empresaAsociada ORDER BY id DESC LIMIT 1")
    ultima_empresa_row = cursor.fetchone()
    if ultima_empresa_row:
        ultima_empresa = ultima_empresa_row[1]  # Nombre de la última empresa
        id_ultima_empresa = ultima_empresa_row[0]
        todas_empresas.append((id_ultima_empresa, ultima_empresa))

    cursor.execute("SELECT id, descripcion FROM planPublicacion ORDER BY id DESC LIMIT 1")
    ultimo_plan_row = cursor.fetchone()
    if ultimo_plan_row:
        ultimo_plan = ultimo_plan_row[1]  # Descripción del último plan
        id_ultimo_plan = ultimo_plan_row[0]
        todos_planes.append((id_ultimo_plan, ultimo_plan))

    # Obtener todas las empresas y planes
    cursor.execute("SELECT id, nombreEmp FROM empresaAsociada")
    todas_empresas.extend(cursor.fetchall())

    cursor.execute("SELECT id, descripcion FROM planPublicacion")
    todos_planes.extend(cursor.fetchall())
    
    cursor.execute("SELECT e.nombreEmp, p.descripcion, fechaInicioContrato, fechafinContrato, ObjetivoPrincipal FROM empresaPlan ep JOIN empresaAsociada e ON ep.idEmpresa = e.id JOIN planPublicacion p ON ep.idPlanPublicacion = p.id")
    datos_empresa_plan = cursor.fetchall()

    cursor.close()

    return render_template('manager.html', ultima_empresa=ultima_empresa, ultimo_plan=ultimo_plan, todas_empresas=todas_empresas, todos_planes=todos_planes, datos_empresa_plan=datos_empresa_plan)

@app.route('/manager/asignarTareas', methods=['GET'])
def asignar():
    return render_template('asignarTareas.html')

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
    cursor = db.conection.cursor()
    cursor.execute("SELECT * FROM planPublicacion")
    planes_result = cursor.fetchall()
    
    planes = []
    column_names = [column[0] for column in cursor.description]
    for record in planes_result:
        planes.append(dict(zip(column_names, record)))
    
    cursor.close()

    
    return render_template('planes.html', planes=planes)
    
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
app.register_blueprint(manager_perfil)


# Ruta para agregar una nueva tarea
@app.route('/calendar', methods=['GET', 'POST'])
def calendario():
    if request.method == 'POST':
        fecha = request.form['fecha']
        descripcion = request.form['descripcion']
        estado = request.form['estado']
        
        cursor = db.conection.cursor

        # Insertar nueva tarea en la base de datos
        cursor.execute("INSERT INTO tareas (fecha, descripcion, estado) VALUES (%s, %s, %s)", (fecha, descripcion, estado))
        db.commit()

    return  render_template('calendario.html')





if __name__ == ('__main__'):
        app.run(debug=True)

