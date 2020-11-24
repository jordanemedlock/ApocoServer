import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from collections import namedtuple

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


Resource = namedtuple('Resource', 'id,name,url,type,status,file_location,notes,extra_fields,created,updated')

def get_resources(db):
    resources = db.execute(
        'SELECT * FROM resources'
    ).fetchall()

    for res in resources:
        yield Resource(**res)

def insert_resource(db, resource):
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO resources 
            (name, url, type, status, file_location, notes, extra_fields) VALUES 
            (?, ?, ?, ?, ?, ?, ?)
        ''',
        resource[1:8]
        )
    return cursor.lastrowid

def remove_resource(db, id):
    cursor = db.cursor()
    cursor.execute('DELETE FROM resources WHERE id=?', id)
    
