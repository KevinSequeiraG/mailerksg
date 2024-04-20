import mysql.connector

import click
from flask import current_app, g
from flask.cli import with_appcontext
from .schema import instructions

import os
from urllib.parse import urlparse

def getDB():
    if 'db' not in g:
        url = urlparse(os.environ['JAWSDB_URL'])
        g.db = mysql.connector.connect(
            host=url.hostname,
            user=url.username,
            password=url.password,
            database=url.path[1:],  # El nombre de la base de datos está después del primer '/'
            port=url.port
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