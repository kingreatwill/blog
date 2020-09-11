from flask import Blueprint, Flask, jsonify

from iblog import target
from iblog.api_server.util import params
from iblog.issue import Issue

blueprint = Blueprint(name='api', import_name=__name__)


def register_api(app: Flask):
    app.register_blueprint(blueprint, url_prefix='/api/issue')


"""
Content-Type : application/json
{
    "title":"testing",
    "body": "this is testing.",
    "labels":"testing"
}
"""
@blueprint.route('/create', methods=['POST'])
def create():
    issue = Issue()
    issue.__dict__.update(params())
    return jsonify(target.sync_create(issue))

"""
{
    "number": "1",
    "title": "testing1",
    "body": "this is testing1.",
    "labels":"testing1"
}
"""
@blueprint.route('/update', methods=['POST'])
def update():
    issue = Issue()
    issue.__dict__.update(params())
    return jsonify(target.sync_update(issue))


"""
{
    "number": "2"
}
"""
@blueprint.route('/delete', methods=['POST'])
def delete():
    issue = Issue()
    issue.__dict__.update(params())
    return jsonify(target.sync_delete(issue))
