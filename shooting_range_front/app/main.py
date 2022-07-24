from flask import (
    render_template,
    redirect,
    url_for,
    Blueprint,
    request,
    session,
    flash,
    jsonify,
    session,
)
from .forms import (
    LoginForm,
    RegisterForm,
    AddCompetitionForm,
    AddChallangeForm,
    AddResultForm,
    EditResultForm,
    EditUserForm,
)
from . import db, login_manager, bcrypt, mail
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)
from .models import User, UserDeserializerSchema
from shooting_range_flask.shooting_range_front.app.requests import (
    get_competitions,
    get_competition,
    get_challanges,
    add_competition_request,
    add_challange_request,
    add_result_request,
    get_results_request,
    get_result_request,
    put_result_request,
    get_competition_challanges,
    get_enrolled_challanges,
    send_mail_request

)
from .keycloak_requests import (
    add_user_to_keycloak,
    get_access_token,
    check_role
)

from flask.views import View, MethodView
from .utils.decorators import scope_required
from flask_mail import Message
import datetime
import requests
import json
from sqlalchemy import exc


def create_initial_competition():
    if not get_challanges():
        add_competition_request('Zawody1', '2022-05-05', 'Otwarta')


class Start(MethodView):
    def get(self):
        create_initial_competition()
        competitions = get_competitions()

        return render_template("start.html", competitions=competitions)


class Home(MethodView):
    def get(self, competitions_slug):
        self.competition = get_competition(competitions_slug)
        if 'roles' in session:
            user_context = session['roles']
        else:
            user_context = 'none'

        return render_template("home.html", competition=self.competition, user_context=user_context)


class Login(MethodView):
    def form(self):
        return LoginForm()

    def __init__(self):
        self.competition = None

    def get(self, competitions_slug):
        self.competition = get_competition(competitions_slug)
        return render_template(
            "login.html", form=LoginForm(), competition=self.competition
        )

    def post(self, competitions_slug):
        form = self.form()
        self.competition = get_competition(competitions_slug)
        print('101')
        if form.validate():
            user = User.query.filter_by(mail=form.mail.data).first()
            print('103', flush=True)
            if user and password_checker(user.password, form.password.data):
                print('104', flush=True)
                login_user(user)
                print('before session update', flush=True)
                session.update(
                    {
                        "roles": check_role(
                            username_=form.mail.data
                        )
                    }
                )
                print('after session update', flush=True)

                return redirect(
                    url_for("Home", competitions_slug=self.competition["slug"])
                )
            else:
                flash_message("Użykownik nie istnieje lub hasło jest błędne")
                return render_template(
                    "login.html", form=form, competition=self.competition
                )


class Register(MethodView):
    def form(self):
        return RegisterForm()

    def __init__(self):
        self.competition = None

    def get(self, competitions_slug):
        self.competition = get_competition(competitions_slug)
        return render_template(
            "register.html", form=self.form(), competition=self.competition
        )

    def post(self, competitions_slug):
        form = self.form()
        self.competition = get_competition(competitions_slug)
        if form.validate():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(
                mail=form.mail.data,
                name=form.name.data,
                surname=form.surname.data,
                license=form.license.data,
                club=form.club.data,
                password=hashed_password,
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                add_user_to_keycloak(
                    username_=form.mail.data,
                    firstname_=form.name.data,
                    lastname_=form.surname.data,
                    email_=form.mail.data,
                    password_=form.password.data,
                )
                # send_mail_request(form.mail.data, form.name.data, form.surname.data)

                return redirect(url_for("Home", competitions_slug=self.competition["slug"]))

            except exc.IntegrityError:
                flash_message("Podaj inny username")
                return render_template(
                    "register.html", form=form, competition=self.competition
                )

        else:
            flash_message("Popraw wartości w formularzu")
            return render_template(
                "register.html", form=form, competition=self.competition
            )


class AddCompetition(MethodView):
    decorators = [login_required, scope_required('admin')]

    def form(self):
        return AddCompetitionForm()

    def __init__(self):
        self.competition = None

    def get(self, competitions_slug):
        user_context = session['roles']
        self.competition = get_competition(competitions_slug)
        return render_template(
            "add_competition.html",
            form=AddCompetitionForm(),
            competition=self.competition,
            user_context=user_context
        )

    def post(self, competitions_slug):
        form = self.form()
        self.competition = get_competition(competitions_slug)
        if form.validate():
            add_competition_request(
                form.name.data, form.date.data, form.registration_opened.data
            )
            return redirect(
                url_for("add_competition", competitions_slug=competitions_slug)
            )
        else:
            flash_message("Niepoprawna wartość")
            return render_template(
                "add_competition.html", form=form, competition=self.competition
            )


class AddChallange(MethodView):
    decorators = [login_required, scope_required('admin')]


    def form(self):
        self.form = AddChallangeForm()

        choices = []
        x = lambda a: (a["_id"], a["name"])
        for y in get_competitions():
            choices.append(x(y))

        self.form.set_initial_values(choices=choices)
        return self.form

    def __init__(self):
        self.competition = None

    def get(self, competitions_slug):
        user_context = session['roles']
        self.competition = get_competition(competitions_slug)
        return render_template(
            "add_challange.html", form=self.form(), competition=self.competition, user_context=user_context
        )

    def post(self, competitions_slug):
        form = self.form()
        self.competition = get_competition(competitions_slug)
        if form.validate():
            add_challange_request(
                form.name.data, form.competition.data, form.number_of_missiles.data
            )
            return redirect(
                url_for("add_challange", competitions_slug=competitions_slug)
            )
        else:
            flash_message("Niepoprawna wartość")
            return render_template(
                "add_challange.html", form=form, competition=self.competition
            )


class AddResult(MethodView):
    decorators = [login_required, scope_required('default-roles-shooting-app')]

    def form(self, competition):
        self.form = AddResultForm()
        # challange = [
        #     (challange["_id"], challange["name"])
        #     for challange in get_competition_challanges(competition["_id"])
        # ]

        challange = []
        x = lambda a: (a["_id"], a["name"])
        for y in get_competition_challanges(competition["_id"]):
            challange.append(x(y))


        self.form.set_initial_values(challange=challange)
        return self.form

    def __init__(self):
        self.competition = None

    def get(self, competitions_slug):
        user_context = session['roles']
        self.competition = get_competition(competitions_slug)
        enrolled_challanges = get_enrolled_challanges(
            current_user.id, self.competition["_id"]
        )
        return render_template(
            "add_result.html",
            form=self.form(self.competition),
            competition=self.competition,
            enrolled_challanges=enrolled_challanges,
            user_context=user_context
        )

    def post(self, competitions_slug):
        self.competition = get_competition(competitions_slug)
        form = self.form(self.competition)
        enrolled_challanges = get_enrolled_challanges(
            current_user.id, self.competition["_id"]
        )
        enrolled_challanges_id = []
        for enrolled_challange in enrolled_challanges:
            enrolled_challanges_id.append(enrolled_challange["_id"])

        if form.validate() and (
            int(self.form.data["challange"]) not in enrolled_challanges_id
        ):
            add_result_request(form.challange.data, current_user.id)
            return redirect(url_for("add_result", competitions_slug=competitions_slug))
        else:
            flash_message("Jesteś już zapisany do tej konkurencji")
            return render_template(
                "add_result.html",
                form=form,
                competition=self.competition,
                enrolled_challanges=enrolled_challanges,
            )


class GetResults(MethodView):
    decorators = [login_required, scope_required('default-roles-shooting-app')]

    def get(self, competitions_slug):
        self.competition = get_competition(competitions_slug)
        results = get_results_request(self.competition["_id"])
        user_context = session['roles']

        challanges = get_challanges()
        challange_dict = {}

        for challange in challanges:
            if challange["competition"] == self.competition["_id"]:
                challange_dict[challange["_id"]] = challange["name"]

        competitors = User.query.all()
        competitors_dict = {}
        for competitor in competitors:
            competitors_dict[competitor.id] = competitor.name + " " + competitor.surname

        for result in results:
            result["challenge"] = challange_dict[result["challenge"]]
            result["competitor"] = competitors_dict[result["competitor"]]
            result["sum"] = (
                result["X"] * 10
                + result["ten"] * 10
                + result["nine"] * 9
                + result["eight"] * 8
                + result["seven"] * 7
                + result["six"] * 6
                + result["five"] * 5
                + result["four"] * 4
                + result["three"] * 3
                + result["two"] * 2
                + result["one"] * 1
                - result["penalty"]
            )

        sorted_results = sorted(results, key=lambda i: i["sum"], reverse=True)

        splitted_results = {}

        for y in challange_dict.values():
            splitted_results[y] = []

        for i in sorted_results:
            for y in challange_dict.values():
                if i["challenge"] == y:
                    splitted_results[y].append(i)

        return render_template(
            "results.html",
            competition=self.competition,
            results=sorted_results,
            splitted_results=splitted_results,
            user_context=user_context
        )


class EditResult(MethodView):
    decorators = [login_required, scope_required('referee')]


    def __init__(self):
        self.form = EditResultForm()
        self.competition = None

    def get(self, competitions_slug, idk):
        user_context = session['roles']
        self.competition = get_competition(competitions_slug)
        edited_result = get_result_request(idk)
        id = edited_result["_id"]
        competitor = edited_result["competitor"]
        challange = edited_result["challenge"]
        X = edited_result["X"]
        ten = edited_result["ten"]
        nine = edited_result["nine"]
        eight = edited_result["eight"]
        seven = edited_result["seven"]
        six = edited_result["six"]
        five = edited_result["five"]
        four = edited_result["four"]
        three = edited_result["three"]
        two = edited_result["two"]
        one = edited_result["one"]
        penalty = edited_result["penalty"]
        disqualification = edited_result["disqualification"]
        initial_values = {
            'id':id,
            'competitor':competitor,
            'challange':challange,
            'X':X,
            'ten':ten,
            'nine':nine,
            'eight':eight,
            'seven':seven,
            'six':six,
            'five':five,
            'four':four,
            'three':three,
            'two':two,
            'one':one,
            'penalty':penalty,
            'disqualification':disqualification
        }
        self.form.set_initial_values(**initial_values)

        return render_template(
            "edit_result.html", form=self.form, competition=self.competition, user_context=user_context
        )

    def post(self, competitions_slug, idk):
        form = self.form
        self.competition = get_competition(competitions_slug)
        if form.validate():
            put_result_request(
                _id = self.form.id.data,
                X = self.form.X.data,
                ten = self.form.ten.data,
                nine = self.form.nine.data,
                eight = self.form.eight.data,
                seven = self.form.seven.data,
                six = self.form.six.data,
                five = self.form.five.data,
                four = self.form.four.data,
                three = self.form.three.data,
                two = self.form.two.data,
                one = self.form.one.data,
                penalty = self.form.penalty.data,
                disqualification= self.form.disqualification.data,
            )
            return redirect(url_for("get_results", competitions_slug=competitions_slug))
        else:
            flash_message("Niepoprawna wartość")
            return render_template(
                "edit_result.html", form=form, competition=self.competition
            )


class GetUsers(MethodView):
    decorators = [login_required, scope_required('admin')]

    def get(self, competitions_slug):
        user_context = session['roles']
        competition = get_competition(competitions_slug)
        users = User.query.all()
        return render_template("get_users.html", users=users, competition=competition, user_context=user_context)





class Logout(MethodView):
    def get(self, competitions_slug):
        logout_user()
        session.update({"roles": 'none'})
        return redirect(url_for("Home", competitions_slug=competitions_slug))


def password_checker(user_password, form_password):
    return bcrypt.check_password_hash(user_password, form_password)

def flash_message(message):
    flash(message, "warning")



@login_manager.user_loader
def load_user(mail):
    return User.query.get(mail)
