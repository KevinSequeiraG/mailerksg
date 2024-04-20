import mysql.connector

import click
from flask import current_app, g
from flask.cli import with_appcontext
from .schema import instructions

import os
from urllib.parse import urlparse

def getDB():
    if 'db' not in g:
        if 'JAWSDB_URL' in os.environ:
            url = urlparse(os.environ['JAWSDB_URL'])
            host = url.hostname
            user = url.username
            password = url.password
            db = url.path[1:]  # El nombre de la base de datos está después del primer '/'
        else:
            host = os.environ.get('FLASK_DATABASE_HOST')
            user = os.environ.get('FLASK_DATABASE_USER')
            password = os.environ.get('FLASK_DATABASE_PASSWORD')
            db = os.environ.get('FLASK_DATABASE')

        g.db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=db
        )
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