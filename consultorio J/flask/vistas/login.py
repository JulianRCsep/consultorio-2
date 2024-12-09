from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token
from modelos import Usuario

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def iniciar_sesion():
    datos = request.get_json()

    if not datos.get('email') or not datos.get('contraseña'):
        return jsonify({'error': 'Faltan datos: email y contraseña son requeridos'}), 400

    usuario = Usuario.query.filter_by(email=datos['email']).first()

    if not usuario or not usuario.verificar_contraseña(datos['contraseña']):
        return jsonify({'error': 'Credenciales inválidas'}), 401

    access_token = create_access_token(identity={'id': usuario.id, 'email': usuario.email, 'tipo': usuario.tipo})

    return jsonify({
        'mensaje': 'Inicio de sesión exitoso',
        'access_token': access_token
    }), 200
