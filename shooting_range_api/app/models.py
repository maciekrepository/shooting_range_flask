from __future__ import annotations
from . import db, ma
from flask_marshmallow import fields
from slugify import slugify
from datetime import datetime

REGISTRATION = {"Otwarta": 1, "Zamknieta": 0}


class Competition(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    date = db.Column(db.Date, nullable=False)
    registration_opened = db.Column(db.Boolean, default=1)
    slug = db.Column(db.String(80), nullable=False)

    def __init__(self, name_, date_, registration_opened_):
        self.name = name_
        self.date = datetime.strptime(date_, "%Y-%m-%d")
        self.registration_opened = REGISTRATION[registration_opened_]
        self.slug = slugify(name_)

    @staticmethod
    def create_from_json(json_body: dict) -> Competition:
        return Competition(
            name_=json_body["name"],
            date_=json_body["date"],
            registration_opened_=json_body["registration_opened"],
        )


class CompetitionSchema(ma.Schema):
    _id = fields.fields.Integer()
    name = fields.fields.Str()
    slug = fields.fields.Str()
    date = fields.fields.Date()
    registration_opened = fields.fields.Boolean()


class Challange(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    competition = db.Column(
        db.Integer, db.ForeignKey("competition._id"), nullable=False
    )
    name = db.Column(db.String(80), nullable=False)
    number_of_missiles = db.Column(db.Integer, nullable=False)
    slug = db.Column(db.String(80), nullable=False)

    def __init__(self, name_, competition_, number_of_missiles_):
        self.name = name_
        self.competition = competition_
        self.number_of_missiles = number_of_missiles_
        self.slug = slugify(name_)

    @staticmethod
    def create_from_json(json_body: dict) -> Challange:
        return Challange(
            name_=json_body["name"],
            competition_=json_body["competition"],
            number_of_missiles_=json_body["number_of_missiles"],
        )


class ChallangeSchema(ma.Schema):
    _id = fields.fields.Integer()
    competition = fields.fields.Integer()
    name = fields.fields.Str()
    number_of_missiles = fields.fields.Integer()
    slug = fields.fields.Str()


class Result(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    challenge = db.Column(db.Integer, db.ForeignKey("challange._id"), nullable=False)
    competitor = db.Column(db.Integer, nullable=False)
    X = db.Column(db.Integer, default=0, nullable=False)
    ten = db.Column(db.Integer, default=0, nullable=False)
    nine = db.Column(db.Integer, default=0, nullable=False)
    eight = db.Column(db.Integer, default=0, nullable=False)
    seven = db.Column(db.Integer, default=0, nullable=False)
    six = db.Column(db.Integer, default=0, nullable=False)
    five = db.Column(db.Integer, default=0, nullable=False)
    four = db.Column(db.Integer, default=0, nullable=False)
    three = db.Column(db.Integer, default=0, nullable=False)
    two = db.Column(db.Integer, default=0, nullable=False)
    one = db.Column(db.Integer, default=0, nullable=False)
    penalty = db.Column(db.Integer, default=0, nullable=False)
    disqualification = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, challange_, competitor_):
        self.challenge = challange_
        self.competitor = competitor_

    @staticmethod
    def create_from_json(json_body: dict) -> Result:
        return Result(
            challange_=json_body["challange"], competitor_=json_body["competitor"]
        )


class ResultSchema(ma.Schema):
    _id = fields.fields.Integer()
    challenge = fields.fields.Integer()
    competitor = fields.fields.Integer()
    X = fields.fields.Integer()
    ten = fields.fields.Integer()
    nine = fields.fields.Integer()
    eight = fields.fields.Integer()
    seven = fields.fields.Integer()
    six = fields.fields.Integer()
    five = fields.fields.Integer()
    four = fields.fields.Integer()
    three = fields.fields.Integer()
    two = fields.fields.Integer()
    one = fields.fields.Integer()
    penalty = fields.fields.Integer()
    disqualification = fields.fields.Integer()
