import os

from flask import Flask

def create_app():
    app = Flask(__name__)
    
    app.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY'),
        DATABASE_HOST = os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD = os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER = os.environ.get('FLASK_DATABASE_USER'),
        DATABASE = os.environ.get('FLASK_DATABASE'),
        MAILGUN_KEY = os.environ.get('MAILGUN_API_KEY'),
        MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN')
    )
    
    from . import db
    
    db.init_app(app)
    
    from . import mail
    
    app.register_blueprint(mail.bp)
    
    # Forzar el modo de depuración
    app.debug = True
    
    return app