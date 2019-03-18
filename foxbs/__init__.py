"""
Foxbs is Fox backward spell of Fox =>Xof => Extension of flask
Extension of flask: support controller like MS MVC in .net
"""

from .base_controller import BaseController
from .controllers import controller
flask_application = None

APPS_PATH = None
REPO_ROOT = None


def create_flask_app(name,path_to_apps):
    import os
    global APPS_PATH
    global REPO_ROOT
    APPS_PATH = path_to_apps
    REPO_ROOT = os.path.dirname(APPS_PATH)
    global flask_application
    from . import apps
    from flask import Flask
    from flask_wtf.csrf import CSRFProtect
    flask_application = Flask(
        name,
        template_folder=REPO_ROOT,
        static_url_path='/resource',
        static_folder=os.sep.join([APPS_PATH,"static"]))
    flask_application.config.from_object('config')

    CSRFProtect(flask_application)
    apps.load_apps(path_to_apps, flask_application)
    return flask_application
