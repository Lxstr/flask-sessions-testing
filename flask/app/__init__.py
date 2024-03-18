from flask_session import Session

from app.config import Config
from app.database.db import db
from flask import Flask

sess = Session()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    db.init_app(app)
    app.config["SESSION_SQLALCHEMY"] = db

    sess.init_app(app)

    from app.guest.routes import guest

    app.register_blueprint(guest)

    return app
