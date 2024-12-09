
from flask import Flask, request, jsonify
from modelos import db, Agendamiento, Usuario, Servicio, Medico, AgendamientoSchema
from datetime import datetime

app = Flask(__name__)

@app.route('/agendamiento', methods=['POST'])
def agendar_cita():
        datos = request.get_json()

      
        if not all(key in datos for key in ['fecha', 'usuario_id', 'servicio_id', 'medico_id']):
            return jsonify({'message': 'Faltan datos necesarios.'}), 400

        try:
      
            fecha = datetime.strptime(datos['fecha'], '%Y-%m-%dT%H:%M:%S')

           
            usuario = Usuario.query.get(datos['usuario_id'])
            servicio = Servicio.query.get(datos['servicio_id'])
            medico = Medico.query.get(datos['medico_id'])

            if not usuario or not servicio or not medico:
                return jsonify({'message': 'El usuario, servicio o médico no existen.'}), 404

           
            nuevo_agendamiento = Agendamiento(
                fecha=fecha, 
                usuario_id=datos['usuario_id'], 
                servicio_id=datos['servicio_id'], 
                medico_id=datos['medico_id']
            )

        
            db.session.add(nuevo_agendamiento)
            db.session.commit()

        
            agendamiento_schema = AgendamientoSchema()
            agendamiento_serializado = agendamiento_schema.dump(nuevo_agendamiento)

            return jsonify({'message': 'Cita agendada.', 'agendamiento': agendamiento_serializado}), 201

        except Exception as e:
            return jsonify({'message': 'Error al agendar la cita.', 'error': str(e)}), 500
