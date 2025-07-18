from flask import Flask, render_template, request, session, url_for, flash, make_response, redirect
import os
from dotenv import load_dotenv
from flask_mail import Mail, Message
from datetime import timedelta
from utils import leer_visitas, guardar_visitas

app = Flask(__name__)
load_dotenv()

# ----------------------------- CONFIGURACION PARA VISITAS ---------------------------------------
VISITAS = 'visitas.txt'
# Asegurarse que el archivo exista
if not os.path.exists(VISITAS):
    with open(VISITAS, 'w') as f:
        f.write("0\n") 

app.secret_key = os.getenv('SESSIONS') #password para sessiones

titulo = 'RealizART3D'

app.permanent_session_lifetime = timedelta(days=365) #define cuánto tiempo dura la sesión del usuario

# --------------------- CONFIGURACION PARA USAR EL MAIL ---------------------------
PASSWORD = os.getenv('GMAIL_APP_PASSWORD')
MAIL = os.getenv('GMAIL')

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = MAIL
app.config['MAIL_PASSWORD'] = PASSWORD  

mail = Mail(app)

# --------------------- PAGINA DE ERROR ---------------------------
@app.errorhandler(404)
def pagina_No_Encontrada(error):
    return render_template('error.html', error=error, title=titulo), 404


# ----------------- PAGINAS --------------------
@app.route("/")
def inicio():
    ip = request.remote_addr

    with open(VISITAS, 'r') as f:
        lines = f.readlines()

    total_visitas = int(lines[0].strip())
    ips = set(line.strip() for line in lines[1:])

    if ip not in ips:
        total_visitas += 1
        with open(VISITAS, 'a') as f:
            f.write(f"{ip}\n")
        with open(VISITAS, 'r+') as f:
            f.seek(0)
            f.write(f"{total_visitas}\n")  # Actualiza la línea 0
    return render_template('paginas/index.html', title=titulo, visitas = total_visitas, ip=ip)

@app.route("/empresa")
def empresa():
    return render_template('paginas/empresa.html', title=titulo)

@app.route("/multimedia")
def multimedia():
    return render_template('paginas/multimedia.html', title=titulo)

@app.route("/contacto")
def contacto():
    return render_template('paginas/contacto.html', title=titulo)

# ----------------- PAGINA DE PRODUCTOS --------------------
@app.route("/productos")
def productos():
    return render_template('paginas/productos.html', title=titulo)

# ----------------- ENVIAR MAIL --------------------
@app.route('/enviar_mail', methods=['POST'])
def enviar_mail():
    nombre = request.form['nombre']
    email = request.form['email']
    mensaje = request.form['mensaje']
    
    try:
        msg = Message('Nueva consulta desde el sitio', 
                      sender=app.config['MAIL_USERNAME'], 
                      recipients=['boomartsfs@gmail.com'])
        msg.body = f'''
        Nombre: {nombre}
        Email: {email}
        Mensaje: {mensaje}
        '''
        mail.send(msg)

        flash(f'¡Gracias {nombre} por su consulta! Te responderemos pronto al mail: {email}', 'success')
    except Exception as e:
        flash('Error al enviar el mensaje. Por favor intentá nuevamente más tarde.', 'error')
        print(e)

    return redirect(url_for('contacto'))

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)