from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from apps.config import config

login_manager = LoginManager()
# 未ログイン時にリダイレクトするエンドポイントを指定
login_manager.login_view = "auth.signup"
# ログイン後に表示するメッセージを指定
login_manager.login_message = ""

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app(config_key):
    app = Flask(__name__)
    app.config.from_object(config[config_key])

    login_manager.init_app(app)
    csrf.init_app(app)

    db.init_app(app)
    Migrate(app, db)

    from apps.auth import views as auth_views
    app.register_blueprint(auth_views.auth, url_prefix="/auth")
    from apps.crud import views as crud_views
    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    from apps.detector import views as dt_views
    app.register_blueprint(dt_views.detector)

    return app
