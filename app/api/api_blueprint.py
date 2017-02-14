from flask import Blueprint, request

api_blueprint = Blueprint('api', __name__, url_prefix='/api')

@api_blueprint.route('/states/<state>')
def get_state_stats(state):
    return 'in get_state_stats() with %s' % state
