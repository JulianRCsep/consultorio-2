from flask import Flask, request, jsonify
from modelos import Servicio, ServicioSchema


app = Flask(__name__)

@app.route('/servicios', methods=['GET'])
def obtener_servicios():
    categoria = request.args.get('categoria', None)

    if categoria:
        servicios = Servicio.query.filter_by(categoria=categoria).all()
    else:
        servicios = Servicio.query.all()

    servicio_schema = ServicioSchema(many=True)
    servicios_serializados = servicio_schema.dump(servicios)

    return jsonify(servicios_serializados), 200
