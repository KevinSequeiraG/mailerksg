import mysql.connector
import os

import click
from flask import current_app, g
from flask.cli import with_appcontext
from .schema import instructions

def getDB():
    if 'db' not in g:
        url = os.getenv('JAWSDB_URL')
        config = {
          'user': url.username,
          'password': url.password,
          'host': url.hostname,
          'port': url.port,
          'database': url.path[1:],  # quita el slash inicial
        }
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