"""Initialize Flask"""
import os
import json
import connexion
from connexion.resolver import MethodViewResolver

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, './config/conf.json')


# Create and setup flask app
def create_app():
    options = {'swagger_url': '/'}
    flask_app = connexion.App(__name__, specification_dir='./swaggers/', options=options)
    load_config(flask_app.app)
    flask_app.add_api(
        './api.yaml',
        resolver=MethodViewResolver('apis'),
        arguments=dict(
            version="1.0.0",
        ),
    )

    return flask_app.app


# Load env config file
def load_config(app, path=file_path):
    """ Load the config file """
    with open(path, 'r') as json_data_file:
        data = json.load(json_data_file)
    app.config.update(
        CONFIG=data,
    )


app = create_app()
