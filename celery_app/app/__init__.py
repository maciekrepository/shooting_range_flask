from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from hashlib import md5
from datetime import timedelta
from .constants import Config
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object(Config)
mail = Mail()
mail.init_app(app)


def create_app():
    app = Flask(__name__)

    # db.init_app(app)

    from .views import SendMail, TaskStatus

    app.add_url_rule("/send_mail", view_func=SendMail.as_view("SendMail"))
    app.add_url_rule("/status/<task_id>", view_func=TaskStatus.as_view("TaskStatus"))

    return app
