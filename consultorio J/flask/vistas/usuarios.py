from flask import Flask, jsonify, request
from modelos import db, Usuario

app = Flask(__name__)


@app.route('/usuarios', methods=['POST'])
def registrar_usuario():
    datos = request.form
    nombre = datos.get('nombre')
    email = datos.get('email')
    contraseña = datos.get('contraseña')

    if not nombre or not email or not contraseña:
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({'error': 'El email ya está registrado'}), 400

    # Crear un nuevo usuario con contraseña encriptada
    nuevo_usuario = Usuario(nombre=nombre, email=email, contraseña=contraseña)
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({'mensaje': 'Usuario registrado exitosamente'}), 201
