"""
Foxbs is Fox backward spell of Fox =>Xof => Extension of flask
Extension of flask: support controller like MS MVC in .net
"""
from .controllers import controller
flask_application = None
def create_flask_app(name):
    from flask import Flask
    from flask_wtf.csrf import CSRFProtect
    flask_application = Flask(name)
    flask_application.config.from_object('config')
    flask_application.config.from_object('config')
    CSRFProtect(flask_application)
    return flask_application

