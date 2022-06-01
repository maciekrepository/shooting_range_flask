from . import db
from .models import Competition, Challange, Result
import requests


class DbRequest:
    def get_competitions(self):
        try:
            result = Competition.query.all()
            return result

        except requests.exceptions.ConnectionError:
            print("Problem z połączeniem z bazą danych")

        except requests.exceptions.Timeout:
            print("Zbyt długi czas oczekiwania")

    def get_challanges(self):
        try:
            result = Challange.query.all()
            return result

        except requests.exceptions.ConnectionError:
            print("Problem z połączeniem z bazą danych")

        except requests.exceptions.Timeout:
            print("Zbyt długi czas oczekiwania")

    def get_competition_challanges(self, competition_id):
        try:
            result = Challange.query.filter_by(competition=competition_id).all()
            return result

        except requests.exceptions.ConnectionError:
            print("Problem z połączeniem z bazą danych")

        except requests.exceptions.Timeout:
            print("Zbyt długi czas oczekiwania")

    def get_competition(self, slug_):
        try:
            result = Competition.query.filter_by(slug=slug_).first()
            return result

        except requests.exceptions.ConnectionError:
            print("Problem z połączeniem z bazą danych")

        except requests.exceptions.Timeout:
            print("Zbyt długi czas oczekiwania")

    def get_results(self, competition_id):
        try:
            challanges = Challange.query.filter_by(competition=competition_id).all()
            list_of_challanges_id = []
            for challange in challanges:
                list_of_challanges_id.append(challange._id)
            results = (
                Result.query.filter(Result.challenge.in_(list_of_challanges_id))
                .order_by(Result.X.desc(), Result.ten.desc())
                .all()
            )
            return results

        except requests.exceptions.ConnectionError:
            print("Problem z połączeniem z bazą danych")

        except requests.exceptions.Timeout:
            print("Zbyt długi czas oczekiwania")

    def get_result(self, id_):
        try:
            result = Result.query.filter_by(_id=id_).first()
            # print(f'{dir(result)}')
            return result

        except requests.exceptions.ConnectionError:
            print("Problem z połączeniem z bazą danych")

        except requests.exceptions.Timeout:
            print("Zbyt długi czas oczekiwania")

    def add_competition_to_db(self, new_competition: Competition) -> None:
        try:
            db.session.add(new_competition)
            db.session.commit()
        except requests.exceptions.ConnectionError:
            print("Problem z połączeniem z bazą danych")

        except requests.exceptions.Timeout:
            print("Zbyt długi czas oczekiwania")

    def add_challange_to_db(self, new_challange: Challange) -> None:
        try:
            db.session.add(new_challange)
            db.session.commit()
        except requests.exceptions.ConnectionError:
            print("Problem z połączeniem z bazą danych")

        except requests.exceptions.Timeout:
            print("Zbyt długi czas oczekiwania")

    def add_result_to_db(self, new_result: Result) -> None:
        try:
            db.session.add(new_result)
            db.session.commit()
        except requests.exceptions.ConnectionError:
            print("Problem z połączeniem z bazą danych")

        except requests.exceptions.Timeout:
            print("Zbyt długi czas oczekiwania")

    def edit_result(self, json_body) -> None:
        try:
            edited_result = Result.query.filter_by(_id=json_body["_id"]).first()
            edited_result.X = json_body["X"]
            edited_result.ten = json_body["ten"]
            edited_result.nine = json_body["nine"]
            edited_result.eight = json_body["eight"]
            edited_result.seven = json_body["seven"]
            edited_result.six = json_body["six"]
            edited_result.five = json_body["five"]
            edited_result.four = json_body["four"]
            edited_result.three = json_body["three"]
            edited_result.two = json_body["two"]
            edited_result.one = json_body["one"]
            edited_result.penalty = json_body["penalty"]
            edited_result.disqualification = json_body["disqualification"]
            # print(f'edited result beore: {edited_result.ten}')
            db.session.commit()
            # print(f'edited result after: {edited_result.ten}')
        except requests.exceptions.ConnectionError:
            print("Problem z połączeniem z bazą danych")

        except requests.exceptions.Timeout:
            print("Zbyt długi czas oczekiwania")

    def get_enrolled_challanges(self, user_id, competition_id):
        try:
            results = Result.query.filter_by(competitor=user_id).all()
            list_of_challanges_id = []
            for result in results:
                list_of_challanges_id.append(result.challenge)
            challanges = (
                Challange.query.filter_by(competition=competition_id)
                .filter(Challange._id.in_(list_of_challanges_id))
                .all()
            )
            return challanges

        except requests.exceptions.ConnectionError:
            print("Problem z połączeniem z bazą danych")

        except requests.exceptions.Timeout:
            print("Zbyt długi czas oczekiwania")
