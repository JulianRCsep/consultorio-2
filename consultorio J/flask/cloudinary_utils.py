import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask import current_app

def configurar_cloudinary():
    """Configura Cloudinary usando las credenciales del archivo de configuración."""
    cloudinary.config(
        cloud_name=current_app.config.get('CLOUDINARY_URL').split('@')[1],
        api_key=current_app.config.get('CLOUDINARY_URL').split('://')[1].split(':')[0],
        api_secret=current_app.config.get('CLOUDINARY_URL').split(':')[2].split('@')[0]
    )

def subir_imagen(imagen, carpeta=None):

    configurar_cloudinary() 
    opciones = {"folder": carpeta} if carpeta else {}
    resultado = cloudinary.uploader.upload(imagen, **opciones)
    return resultado
