"""
issue views
"""

import json

from flask import Blueprint, request, jsonify
from flask.ext.login import current_user
from flask.ext.restful import abort
from ..models import db, Ticket, Repo

issue = Blueprint('issue', __name__, static_folder='../static')


@issue.route('/tickets/<string:rgroup>/<string:rname>')
def index(rgroup, rname):
    filters = [
        (Repo.group == rgroup),
        (Repo.name == rname),
    ]
    result = Ticket.query.join(Repo).filter(*filters).all()
    tickets = [t.to_dict(pretty_date=True) for t in result]
    return jsonify(dict(tickets=tickets))


@issue.route('/tickets/<string:rgroup>/<string:rname>', methods=['POST'])
def create(rgroup, rname):
    form = json.loads(request.data.decode('utf-8'))
    try:
        repo_id = Repo.query.filter(
            (Repo.group == rgroup),
            (Repo.name == rname),
        ).first().id
    except:
        abort(500)

    ticket = Ticket()
    ticket.repo_id = repo_id
    ticket.user_id = current_user.id
    ticket.summary = form['summary']
    ticket.content = form['content']
    db.session.add(ticket)
    db.session.commit()
    return jsonify(dict(result=True))


@issue.route('/tickets/<int:id>', methods=['PUT'])
def update(id):
    form = json.loads(request.data.decode('utf-8'))

    ticket = Ticket.query.get(id)
    ticket.summary = form['summary']
    ticket.content = form['content']
    db.session.add(ticket)
    db.session.commit()
    return jsonify(dict(result=True))


@issue.route('/tickets/<int:id>', methods=['DELETE'])
def destroy(id):
    ticket = Ticket.query.get(id)
    db.session.delete(ticket)
    db.session.commit()
    return jsonify(dict(result=True))
