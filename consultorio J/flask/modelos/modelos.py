from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contraseña = db.Column(db.LargeBinary(200), nullable=False)  # Almacenar como binario
    tipo = db.Column(db.String(50), nullable=False, default='usuario')  # 'usuario' o 'admin'
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, nombre, email, contraseña, tipo='usuario'):
        self.nombre = nombre
        self.email = email
        self.contraseña = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())
        self.tipo = tipo

    def verificar_contraseña(self, contraseña):
        return bcrypt.checkpw(contraseña.encode('utf-8'), self.contraseña)



class Servicio(db.Model):
    __tablename__ = 'servicios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    categoria = db.Column(db.String(100), nullable=False)
    
    def __init__(self, nombre, descripcion, categoria):
        self.nombre = nombre
        self.descripcion = descripcion
        self.categoria = categoria

class Agendamiento(db.Model):
    __tablename__ = 'agendamientos'

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    servicio_id = db.Column(db.Integer, db.ForeignKey('servicios.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)

    usuario = db.relationship('Usuario', backref=db.backref('agendamientos', lazy=True))
    servicio = db.relationship('Servicio', backref=db.backref('agendamientos', lazy=True))
    medico = db.relationship('Medico', backref=db.backref('agendamientos', lazy=True))

    def __init__(self, fecha, usuario_id, servicio_id, medico_id):
        self.fecha = fecha
        self.usuario_id = usuario_id
        self.servicio_id = servicio_id
        self.medico_id = medico_id


class Medico(db.Model):
    __tablename__ = 'medicos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=True)

    def __init__(self, nombre, especialidad, email, telefono=None):
        self.nombre = nombre
        self.especialidad = especialidad
        self.email = email
        self.telefono = telefono


class Foto(db.Model):
    __tablename__ = 'fotos'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    tipo = db.Column(db.String(50), nullable=False)  # en este caso medico o consultorio 

    def __init__(self, url, descripcion, tipo):
        self.url = url
        self.descripcion = descripcion
        self.tipo = tipo


def crear_superadmin():
    superadmin = Usuario.query.filter_by(email='admin@consultorio.com').first()
    if not superadmin:
        superadmin = Usuario(nombre='Super Admin', email='admin@consultorio.com', contraseña='admin1234', tipo='admin')
        db.session.add(superadmin)
        db.session.commit()

if __name__ == "__main__":
    db.create_all()  
    crear_superadmin()  


# Serializacion consultorio HU
 
class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
        exclude = ['contraseña']

class ServicioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Servicio
        include_relationships = True

class AgendamientoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Agendamiento
        include_relationships = True

class MedicoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Medico
        include_relationships = True    

class FotoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Foto
        include_relationships = False

    
