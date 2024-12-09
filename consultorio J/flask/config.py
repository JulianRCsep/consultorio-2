import os
import cloudinary

class Config:
    """Configuración base del proyecto"""

    SQLALCHEMY_DATABASE_URI = 'sqlite:///consultorio.db' 
    SQLALCHEMY_TRACK_MODIFICATIONS = False      
    SECRET_KEY = os.getenv('SECRET_KEY', 'frase-secreta')
    PROPAGATE_EXCEPTIONS = True 

cloudinary.config(
    cloud_name = 'dvtvke8be',
    api_key = '351389888829945',
    api_secret = 'cvoupUwcXTNgatbNJQlEmuLe4kA'
)