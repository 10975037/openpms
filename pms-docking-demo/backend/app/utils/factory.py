from app.utils import mail
from flask import Flask
from app.models import db
from app.api import api
from app.marshalling import ma
from flask_cors import CORS
from app.utils import log


def register_plugin(app):
    api.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    CORS().init_app(app)
    log.init_app(app)
    mail.init_app(app)

    with app.app_context():
        # db.drop_all()
        db.create_all()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.APP_ENV')
    register_plugin(app)
    return app