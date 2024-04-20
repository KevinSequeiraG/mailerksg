import click
from flask import current_app, g
from flask.cli import with_appcontext
from .schema import instructions

from flask import g
import mysql.connector
import os
from urllib.parse import urlparse

def getDB():
    if 'db' not in g:
        # Obtiene la URL de conexión de la variable de entorno
        db_url = os.getenv('JAWSDB_URL')
        if db_url is None:
            raise Exception("Database URL not found")

        url = urlparse(db_url)

        # Parsea los componentes de la URL
        config = {
            'user': url.username,
            'password': url.password,
            'host': url.hostname,
            'port': url.port or 3306,
            'database': url.path.lstrip('/'),
        }

        # Establece la conexión
        g.db = mysql.connector.connect(**config)
        g.c = g.db.cursor(dictionary=True)

    return g.db, g.c

def closeDB(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
        
def initDB():
    db, c = getDB()
    
    for i in instructions:
        c.execute(i)
    
    db.commit()
    
@click.command('init-db')
@with_appcontext
def init_db_command():
    initDB()
    click.echo('Base de datos inicializada.')
    
def init_app(app):
    app.teardown_appcontext(closeDB)
    app.cli.add_command(init_db_command)