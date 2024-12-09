from flask import Flask, render_template
from flask_migrate import Migrate
from config import Config
from modelos import db
from vistas.medicos import obtener_medicos, agregar_medico
from vistas.usuarios import registrar_usuario 


app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)
migrate = Migrate(app, db)

app.add_url_rule('/usuarios', 'registrar_usuario', registrar_usuario, methods=['POST'])
app.add_url_rule('/medicos', 'obtener_medicos', obtener_medicos, methods=['GET'])
app.add_url_rule('/medicos', 'agregar_medico', agregar_medico, methods=['POST'])


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
