
from flask import Flask

from api.api_blueprint import api_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_blueprint)
    return app


app = create_app()
