import requests
import json


def get_competitions():
    try:
        result = requests.get("http://web1:4000/competitions")
        return result.json()

    except requests.exceptions.ConnectionError:
        print("Problem z połączeniem z bazą danych")

    except requests.exceptions.Timeout:
        print("Zbyt długi czas oczekiwania")


def get_challanges():
    try:
        result = requests.get("http://web1:4000/challanges")
        return result.json()
    except requests.exceptions.ConnectionError:
        print("Problem z połączeniem z bazą danych")

    except requests.exceptions.Timeout:
        print("Zbyt długi czas oczekiwania")


def get_competition_challanges(competition_id):
    try:
        result = requests.get("http://web1:4000/challanges/" + str(competition_id))
        return result.json()
    except requests.exceptions.ConnectionError:
        print("Problem z połączeniem z bazą danych")

    except requests.exceptions.Timeout:
        print("Zbyt długi czas oczekiwania")


def get_competition(slug_):
    try:
        result = requests.get("http://web1:4000/competition/" + slug_)
        return result.json()
    except requests.exceptions.ConnectionError:
        print("Problem z połączeniem z bazą danych")

    except requests.exceptions.Timeout:
        print("Zbyt długi czas oczekiwania")


def get_results_request(competition_id):
    try:
        result = requests.get("http://web1:4000/results/" + str(competition_id))
        return result.json()
    except requests.exceptions.ConnectionError:
        print("Problem z połączeniem z bazą danych")

    except requests.exceptions.Timeout:
        print("Zbyt długi czas oczekiwania")


def get_result_request(id):
    try:
        result = requests.get("http://web1:4000/result/" + id)
        return result.json()
    except requests.exceptions.ConnectionError:
        print("Problem z połączeniem z bazą danych")

    except requests.exceptions.Timeout:
        print("Zbyt długi czas oczekiwania")


def get_enrolled_challanges(user_id, competition_id):
    try:
        result = requests.get(
            "http://web1:4000/get_enrolled_challanges/"
            + str(user_id)
            + "/"
            + str(competition_id)
        )
        return result.json()
    except requests.exceptions.ConnectionError:
        print("Problem z połączeniem z bazą danych")

    except requests.exceptions.Timeout:
        print("Zbyt długi czas oczekiwania")


def add_competition_request(name_, date_, registration_opened_):
    try:
        requests.post(
            "http://web1:4000/add_competition",
            json={
                "name": name_,
                "date": str(date_),
                "registration_opened": registration_opened_,
            },
        )
    except requests.exceptions.ConnectionError:
        print("Problem z połączeniem z bazą danych")

    except requests.exceptions.Timeout:
        print("Zbyt długi czas oczekiwania")


def add_challange_request(name_, competition_, number_of_missiles_):
    try:
        requests.post(
            "http://web1:4000/add_challange",
            json={
                "name": name_,
                "competition": competition_,
                "number_of_missiles": number_of_missiles_,
            },
        )
    except requests.exceptions.ConnectionError:
        print("Problem z połączeniem z bazą danych")

    except requests.exceptions.Timeout:
        print("Zbyt długi czas oczekiwania")


def add_result_request(challange_, competitor_):
    try:
        requests.post(
            "http://web1:4000/add_result",
            json={"challange": challange_, "competitor": competitor_},
        )
    except requests.exceptions.ConnectionError:
        print("Problem z połączeniem z bazą danych")

    except requests.exceptions.Timeout:
        print("Zbyt długi czas oczekiwania")


def put_result_request(
    _id,
    X,
    ten,
    nine,
    eight,
    seven,
    six,
    five,
    four,
    three,
    two,
    one,
    penalty,
    disqualification,
):
    try:
        requests.put(
            "http://web1:4000/edit_result/<_id>",
            json={
                "_id": _id,
                "X": X,
                "ten": ten,
                "nine": nine,
                "eight": eight,
                "seven": seven,
                "six": six,
                "five": five,
                "four": four,
                "three": three,
                "two": two,
                "one": one,
                "penalty": penalty,
                "disqualification": disqualification,
            },
        )
    except requests.exceptions.ConnectionError:
        print("Problem z połączeniem z bazą danych")

    except requests.exceptions.Timeout:
        print("Zbyt długi czas oczekiwania")


def send_mail_request(mail_, name_, surname_):
    try:
        requests.post(
            "http://celery_app:3000/send_mail",
            json={"mail": mail_, "name": name_, "surname": surname_},
        )
    except requests.exceptions.ConnectionError:
        print("Problem z połączeniem z bazą danych")

    except requests.exceptions.Timeout:
        print("Zbyt długi czas oczekiwania")



