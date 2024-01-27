from flask import Flask, render_template, request, redirect,url_for, session
import Conexion.config as db
import secrets
from models.registro import registro_usu
from models.PlanPublicacion import registro_plan
from models.registro_empresa import registro_empresa

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
            return render_template('index.html', message="Rol no reconocido")

    else:
        return render_template('index.html', message="Las credenciales no son correctas")
    
#esto es para dirigirnos a la tarea de usuario  
@app.route('/tasks', methods = ['GET'])
def task():
    return render_template('tasks.html')
#esto es para dirigirnos al perfil del Administrador
@app.route('/admin', methods = ['GET'])
def admin():
    return render_template('admin.html')
#esto es para dirigirnos al perfil del Manager
@app.route('/manager', methods = ['GET'])
def manager():
    return render_template('manager.html')
    
@app.route('/logout') #esto es para el cierre de cesion
def logout():
    session.clear()
    return redirect(url_for('home')) 


@app.route('/registro', methods = ['GET'])
def registro():
    return render_template('Registrarse.html')

app.register_blueprint(registro_usu, url_prefix='/registro_usuario')
app.register_blueprint(registro_plan, url_prefix='/registro_plan')
app.register_blueprint(registro_empresa, url_prefix='/registro_empresa')
  
if __name__ == ('__main__'):
        app.run(debug=True)
