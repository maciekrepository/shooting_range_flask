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
        # return competition_schema.jsonify(new_competition)


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
        # return challange_schema.jsonify(new_challange)


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
        # edited_result = get_result(_id)
        # edited_result = GetResult.get(_id)
        instance_db_request = DbRequest()
        instance_db_request.edit_result(body)
        # return result_schema.jsonify(edited_result)


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header"""
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "description": "Authorization header is expected",
            },
            401,
        )

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must start with" " Bearer",
            },
            401,
        )
    elif len(parts) == 1:
        raise AuthError(
            {"code": "invalid_header", "description": "Token not found"}, 401
        )
    elif len(parts) > 2:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must be" " Bearer token",
            },
            401,
        )

    token = parts[1]
    return token


def requires_auth(f):
    """Determines if the Access Token is valid"""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://" + AUTH0_DOMAIN + "/",
                )
            except jwt.ExpiredSignatureError:
                raise AuthError(
                    {"code": "token_expired", "description": "token is expired"}, 401
                )
            except jwt.JWTClaimsError:
                raise AuthError(
                    {
                        "code": "invalid_claims",
                        "description": "incorrect claims,"
                        "please check the audience and issuer",
                    },
                    401,
                )
            except Exception:
                raise AuthError(
                    {
                        "code": "invalid_header",
                        "description": "Unable to parse authentication" " token.",
                    },
                    401,
                )

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError(
            {"code": "invalid_header", "description": "Unable to find appropriate key"},
            401,
        )

    return decorated
