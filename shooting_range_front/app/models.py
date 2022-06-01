from __future__ import annotations
from . import db
from flask_login import UserMixin
from marshmallow import Schema, fields


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    club = db.Column(db.String(80))
    license = db.Column(db.String(80))
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_refree = db.Column(db.Boolean, nullable=False, default=False)


class UserDeserializer(UserMixin):
    def __init__(self, mail_, password_, name_, surname_, club_, license_):
        self.mail = mail_
        self.password = password_
        self.name = name_
        self.surname = surname_
        self.club = club_
        self.license = license_


class UserDeserializerSchema(Schema):
    mail = fields.String()
    password = fields.String()
    name = fields.String()
    surname = fields.String()
    club = fields.String()
    license = fields.String()
