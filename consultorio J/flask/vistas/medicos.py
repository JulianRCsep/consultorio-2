from flask import Flask, jsonify, request, render_template
from modelos import db, Medico
import cloudinary.uploader

app = Flask(__name__)

@app.route('/medicos', methods=['GET'])
def obtener_medicos():
    medicos = Medico.query.all()
    medicos_serializados = [
        {
            'id': medico.id,
            'nombre': medico.nombre,
            'especialidad': medico.especialidad,
            'email': medico.email,
            'foto_url': medico.foto_url
        }
        for medico in medicos
    ]
    return jsonify(medicos_serializados), 200

@app.route('/medicos', methods=['POST'])
def agregar_medico():
    datos = request.form
    nombre = datos.get('nombre')
    especialidad = datos.get('especialidad')
    email = datos.get('email')

    if not nombre or not especialidad or not email:
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400

    if Medico.query.filter_by(email=email).first():
        return jsonify({'error': 'El médico con este email ya existe'}), 400

    foto = request.files.get('foto')
    foto_url = None

    if foto:
        try:
            resultado = cloudinary.uploader.upload(foto)
            foto_url = resultado.get('secure_url')
        except Exception as e:
            return jsonify({'error': 'Error al subir la foto', 'detalle': str(e)}), 500

    nuevo_medico = Medico(nombre=nombre, especialidad=especialidad, email=email, foto_url=foto_url)
    db.session.add(nuevo_medico)
    db.session.commit()

    return jsonify({'mensaje': 'Médico agregado exitosamente', 'id': nuevo_medico.id, 'foto_url': foto_url}), 201

@app.route('/subir-foto', methods=['GET'])
def formulario_subir_foto():
    return render_template('subir_foto.html')



