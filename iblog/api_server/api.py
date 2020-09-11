from flask import Blueprint

blueprint = Blueprint(name='api', import_name=__name__)


def register_api(server):
    server.app.register_blueprint(blueprint, url_prefix='/api')


@blueprint.route('/issue', methods=['POST'])
def create():
    return 'Hello World'


@blueprint.route('/issue', methods=['POST'])
def update():
    return 'Hello World'


@blueprint.route('/issue', methods=['POST'])
def delete():
    return 'Hello World'
