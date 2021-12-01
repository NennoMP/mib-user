"""
Flask initialization
"""
from operator import mod
import os
import datetime

__version__ = '0.1'

import connexion
from flask_environments import Environments
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging

db = None
migrate = None
debug_toolbar = None
redis_client = None
app = None
api_app = None
logger = None


def create_app():
    """
    This method create the Flask application.
    :return: Flask App Object
    """
    global db
    global app
    global migrate
    global api_app

    # first initialize the logger
    init_logger()

    api_app = connexion.FlaskApp(
        __name__,
        server='flask',
        specification_dir='openapi/',
    )

    # getting the flask app
    app = api_app.app

    flask_env = os.getenv('FLASK_ENV', 'None')
    #flask_env = "testing"
    if flask_env == 'development':
        config_object = 'config.DevConfig'
    elif flask_env == 'testing':
        config_object = 'config.TestConfig'
    elif flask_env == 'production':
        config_object = 'config.ProdConfig'
    else:
        raise RuntimeError(
            "%s is not recognized as valid app environment. You have to setup the environment!" % flask_env)

    # Load config
    env = Environments(app)
    env.from_object(config_object)

    # registering db
    db = SQLAlchemy(
        app=app
    )

    # requiring the list of models
    from mib.models.user import User
    from mib.dao.user_manager import UserManager

    # creating migrate
    migrate = Migrate(
        app=app,
        db=db
    )

    # checking the environment
    if flask_env == 'testing' or flask_env == 'development':
        # we need to populate the db
        db.create_all(app=app)


        '''
        # Create first admin user
        with app.app_context():
            q = db.session.query(User).filter(User.email == "admin@example.com")
            user = q.first()
            if user is None:
                user = User()

                user.set_email('admin@example.com')
                user.set_password('Admin1@')
                user.set_first_name('Admin')
                user.set_last_name('Admin')
                date_of_birth = datetime.datetime.strptime('1997-09-25',    '%Y-%m-%d')
                user.set_date_of_birth(date_of_birth)
                user.set_location('Pisa')
                user.set_profile_pic('mib/static/images/default.jpg')
                user.set_admin(True)
                UserManager.create_user(user)
    '''

    # registering to api app all specifications
    register_specifications(api_app)

    return app


def init_logger():
    global logger
    """
    Initialize the internal application logger.
    :return: None
    """
    logger = logging.getLogger(__name__)
    from flask.logging import default_handler
    logger.addHandler(default_handler)


def register_specifications(_api_app):
    """
    This function registers all resources in the flask application
    :param _api_app: Flask Application Object
    :return: None
    """

    # we need to scan the specifications package and add all yaml files.
    from importlib_resources import files
    folder = files('mib.specifications')
    for _, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                file_path = folder.joinpath(file)
                _api_app.add_api(file_path)
