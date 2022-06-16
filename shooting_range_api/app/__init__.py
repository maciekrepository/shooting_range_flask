from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from hashlib import md5
from datetime import timedelta
from .constants import Config
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    encryptor = md5()

    db.init_app(app)
    app.config.from_object(Config)


    from .main import (
        GetCompetitions,
        GetCompetition,
        AddCompetition,
        GetResults,
        GetResult,
        AddChallange,
        GetChallanges,
        GetCompetitionChallanges,
        GetEnrolledChallanges,
        AddResult,
        EditResult,
    )

    app.add_url_rule(
        "/competitions", view_func=GetCompetitions.as_view("GetCompetitions")
    )
    app.add_url_rule(
        "/competition/<slug_>", view_func=GetCompetition.as_view("GetCompetition")
    )
    app.add_url_rule(
        "/add_competition", view_func=AddCompetition.as_view("AddCompetition")
    )
    app.add_url_rule(
        "/results/<competition_id>", view_func=GetResults.as_view("GetResults")
    )
    app.add_url_rule("/result/<id>", view_func=GetResult.as_view("GetResult"))
    app.add_url_rule("/add_challange", view_func=AddChallange.as_view("AddChallange"))
    app.add_url_rule("/challanges", view_func=GetChallanges.as_view("GetChallanges"))
    app.add_url_rule(
        "/challanges/<competition_id>",
        view_func=GetCompetitionChallanges.as_view("GetCompetitionChallanges"),
    )
    app.add_url_rule(
        "/get_enrolled_challanges/<user_id>/<competition_id>",
        view_func=GetEnrolledChallanges.as_view("GetEnrolledChallanges"),
    )
    app.add_url_rule("/add_result", view_func=AddResult.as_view("AddResult"))
    app.add_url_rule("/edit_result/<_id>", view_func=EditResult.as_view("EditResult"))

    return app
