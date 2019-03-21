"""
Foxbs is Fox backward spell of Fox =>Xof => Extension of flask
Extension of flask: support controller like MS MVC in .net
"""
settings = None
from .base_controller import BaseController
from .controllers import controller
flask_application = None

APPS_PATH = None
REPO_ROOT = None


def load_config(path_to_dir):
    import os
    from .xml2dict import load_from_file
    config = load_from_file(os.sep.join([path_to_dir, "config.xml"]))
    global settings
    settings = __settings__(config)


def create_flask_app(name,path_to_apps):
    # import jinja2


    import os
    global APPS_PATH
    global REPO_ROOT
    APPS_PATH = path_to_apps
    REPO_ROOT = os.path.dirname(APPS_PATH)
    global flask_application
    from . import apps
    from flask import Flask
    from flask_session import Session
    from .xml2dict import load_from_file
    from flask_wtf.csrf import CSRFProtect
    # from flask_mako import MakoTemplates
    from datetime import timedelta
    config = load_from_file(os.sep.join([REPO_ROOT,"config.xml"]))
    flask_application = Flask(
        name,
        template_folder=REPO_ROOT,
        static_url_path='/resource',
        static_folder=os.sep.join([APPS_PATH ,"static"]))
    flask_application.config.from_object('config')
    flask_application.secret_key = config["SECRET_KEY"]
    flask_application.config['SESSION_TYPE'] = config.get("SESSION_TYPE",'filesystem')
    flask_application.config['SESSION_PERMANENT'] = config.get("SESSION_PERMANENT",True)
    flask_application.config['PERMANENT_SESSION_LIFETIME'] = timedelta(config.get("PERMANENT_SESSION_LIFETIME",30))
    Session(flask_application)
    # mako = MakoTemplates(flask_application)
    # environment = jinja2.Environment(
    #     loader=flask_application.jinja_loader,
    #     variable_start_string = '@{',
    #     variable_end_string = '}'
    # )
    # fx = flask_application.create_jinja_environment()
    # fx.variable_start_string = "${"
    # fx.variable_end_string = "}"
    # flask_application.jinja_env = fx

    # fx = CSRFProtect(flask_application)
    apps.load_apps(path_to_apps, flask_application)
    global settings
    if not settings:
        settings = __settings__(config)
    return flask_application

class __settings__(object):
    def __init__(self,data):
        self.__dict__.update(data)