from flask import(Blueprint)

blueprint = Blueprint('small_heritage_url', __name__)


@blueprint.route("/")
def hello():
    return "API Small Heritage"