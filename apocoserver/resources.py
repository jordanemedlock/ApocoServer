import functools

from flask import (
    Blueprint, render_template, request, redirect
)

import datetime

from apocoserver.db import get_db, get_resources, Resource, insert_resource, remove_resource



bp = Blueprint("resources", __name__, url_prefix='/resources')

@bp.route('/index', methods=('GET','POST'))
@bp.route('/', methods=('GET','POST'))
def index():
    db = get_db()
    if request.method == 'POST':
        new_resource = Resource(
            id=None, 
            name=request.form['name'],
            url=request.form['url'],
            type=request.form['type'],
            status='REQUESTED',
            file_location=None,
            notes=request.form['notes'],
            extra_fields=None,
            created=datetime.datetime.today(),
            updated=datetime.datetime.today()
        )
        resource_id = insert_resource(db, new_resource)
        db.commit()
    resources = get_resources(db)
    return render_template('resources/index.html', resources=resources)

@bp.route('/delete/<id>', methods=('GET',))
def delete_resource(id):
    db = get_db()
    remove_resource(db, id)
    db.commit()
    return redirect('/resources/index')