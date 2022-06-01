from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from hashlib import md5
from datetime import timedelta
from flask_bcrypt import Bcrypt
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)
from flask_mail import Mail

from .constants import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()
mail.init_app(app)


def create_app():

    encryptor = md5()

    db.init_app(app)

    # mail = Mail(app)

    login_manager.init_app(app)
    login_manager.login_view = "login"

    from .main import (
        Start,
        Home,
        Login,
        Logout,
        Register,
        AddCompetition,
        AddChallange,
        AddResult,
        GetResults,
        EditResult,
        GetUsers,
        EditUser,
    )

    app.add_url_rule("/", view_func=Start.as_view("Start"))
    app.add_url_rule("/<competitions_slug>", view_func=Home.as_view("Home"))
    app.add_url_rule("/<competitions_slug>/login", view_func=Login.as_view("login"))
    app.add_url_rule("/<competitions_slug>/logout", view_func=Logout.as_view("Logout"))
    app.add_url_rule(
        "/<competitions_slug>/register", view_func=Register.as_view("register")
    )
    app.add_url_rule(
        "/<competitions_slug>/add_competition",
        view_func=AddCompetition.as_view("add_competition"),
    )
    app.add_url_rule(
        "/<competitions_slug>/add_challange",
        view_func=AddChallange.as_view("add_challange"),
    )
    app.add_url_rule(
        "/<competitions_slug>/add_result", view_func=AddResult.as_view("add_result")
    )
    app.add_url_rule(
        "/<competitions_slug>/get_results", view_func=GetResults.as_view("get_results")
    )
    app.add_url_rule(
        "/edit_result/<competitions_slug>/<idk>",
        view_func=EditResult.as_view("edit_result"),
    )
    app.add_url_rule(
        "/<competitions_slug>/get_users", view_func=GetUsers.as_view("GetUsers")
    )
    app.add_url_rule(
        "/edit_user/<competitions_slug>/<user_id>",
        view_func=EditUser.as_view("EditUser"),
    )

    return app
