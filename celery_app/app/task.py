from . import app, mail
from flask_mail import Message
from datetime import datetime
from celery import Celery, Task
from .constants import CeleryConfig


celery_app = Celery()


@celery_app.task
def send_mail_message(json_body):
    msg = Message(
        f"Hej!",
        body=f'Witaj {json_body["name"]} {json_body["surname"]}! Właśnie zarejestrowałeś się w aplikacji zawodów strzeleckich. Od teraz możesz zapisywać się do konkurencji',
        sender="aaaa@op.pl",
        recipients=[json_body["mail"]],
    )
    with app.app_context():
        mail.send(msg)

    return "Hello!"
