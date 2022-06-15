from flask import Blueprint, request, jsonify, Response
from . import db
from .models import (
    Challange,
    Competition,
    Result,
    CompetitionSchema,
    ChallangeSchema,
    ResultSchema,
)
from flask_sqlalchemy import sqlalchemy
from .DbRequests import DbRequest
from flask.views import View, MethodView


competitions_schema = CompetitionSchema(many=True)
competition_schema = CompetitionSchema()

challanges_schema = ChallangeSchema(many=True)
challange_schema = ChallangeSchema()

results_schema = ResultSchema(many=True)
result_schema = ResultSchema()


class GetCompetitions(MethodView):
    def get(self):
        instance_db_request = DbRequest()
        competitions = instance_db_request.get_competitions()
        return competitions_schema.jsonify(competitions)


class GetCompetition(MethodView):
    def get(self, slug_):
        instance_db_request = DbRequest()
        competition = instance_db_request.get_competition(slug_)
        return competition_schema.jsonify(competition)


class AddCompetition(MethodView):
    def post(self):
        body = request.json
        new_competition = Competition.create_from_json(json_body=body)
        instance_db_request = DbRequest()
        instance_db_request.add_competition_to_db(new_competition)


class GetResults(MethodView):
    def get(self, competition_id):
        instance_db_request = DbRequest()
        results = instance_db_request.get_results(competition_id)
        return results_schema.jsonify(results)


class GetResult(MethodView):
    def get(self, id):
        instance_db_request = DbRequest()
        result = instance_db_request.get_result(id)
        return result_schema.jsonify(result)


class AddChallange(MethodView):
    def post(self):
        body = request.json
        new_challange = Challange.create_from_json(json_body=body)
        instance_db_request = DbRequest()
        instance_db_request.add_challange_to_db(new_challange)


class GetChallanges(MethodView):
    def get(self):
        instance_db_request = DbRequest()
        challanges = instance_db_request.get_challanges()
        return challanges_schema.jsonify(challanges)


class GetCompetitionChallanges(MethodView):
    def get(self, competition_id):
        instance_db_request = DbRequest()
        challanges = instance_db_request.get_competition_challanges(competition_id)
        return challanges_schema.jsonify(challanges)


class GetEnrolledChallanges(MethodView):
    def get(self, user_id, competition_id):
        instance_db_request = DbRequest()
        challanges = instance_db_request.get_enrolled_challanges(
            user_id, competition_id
        )
        return challanges_schema.jsonify(challanges)


class AddResult(MethodView):
    def post(self):
        body = request.json
        new_result = Result.create_from_json(json_body=body)
        instance_db_request = DbRequest()
        instance_db_request.add_result_to_db(new_result)
        # return result_schema.jsonify(new_result)


class EditResult(MethodView):
    def put(self, _id):
        body = request.json
        instance_db_request = DbRequest()
        instance_db_request.edit_result(body)


