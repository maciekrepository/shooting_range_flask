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
from .requests import (
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


class Start(MethodView):
    def get(self):
        competitions = get_competitions()
        print("start task")

        # task = send_mail.delay()
        return render_template("start.html", competitions=competitions)


class Home(MethodView):
    def get(self, competitions_slug):
        self.competition = get_competition(competitions_slug)
        # task = send_mail.delay()
        return render_template("home.html", competition=self.competition)


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
        if form.validate():
            user = User.query.filter_by(mail=form.mail.data).first()
            if user and password_checker(user.password, form.password.data):
                login_user(user)
                # task = send_mail.delay()

                session.update(
                    {
                        "roles": check_role(
                            username_=form.mail.data
                        )
                    }
                )

                flash(
                    f" your roles: {check_role(form.mail.data)}",
                    "warning",
                )
                return redirect(
                    url_for("Home", competitions_slug=self.competition["slug"])
                )
            else:
                flash("User does not exist or wrong password", "warning")
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
            try:
                hashed_password = bcrypt.generate_password_hash(form.password.data)
                new_user = User(
                    mail=form.mail.data,
                    name=form.name.data,
                    surname=form.surname.data,
                    license=form.license.data,
                    club=form.club.data,
                    password=hashed_password,
                )
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
                flash("Please provide different username", "warning")
                return render_template(
                    "register.html", form=form, competition=self.competition
                )

        else:
            flash("Please correct data in the form", "warning")
            return render_template(
                "register.html", form=form, competition=self.competition
            )


class AddCompetition(MethodView):
    decorators = [login_required]

    def form(self):
        return AddCompetitionForm()

    def __init__(self):
        self.competition = None

    def get(self, competitions_slug):
        self.competition = get_competition(competitions_slug)
        return render_template(
            "add_competition.html",
            form=AddCompetitionForm(),
            competition=self.competition,
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
            flash("Wrong values", "warning")
            return render_template(
                "add_competition.html", form=form, competition=self.competition
            )


class AddChallange(MethodView):
    decorators = [login_required]

    def form(self):
        self.form = AddChallangeForm()
        choices = [
            (competition["_id"], competition["name"])
            for competition in get_competitions()
        ]
        self.form.set_initial_values(choices=choices)
        return self.form

    def __init__(self):
        self.competition = None

    def get(self, competitions_slug):
        self.competition = get_competition(competitions_slug)
        return render_template(
            "add_challange.html", form=self.form(), competition=self.competition
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
            flash("Wrong values", "warning")
            return render_template(
                "add_challange.html", form=form, competition=self.competition
            )


class AddResult(MethodView):
    decorators = [login_required, scope_required('referee')]

    def form(self, competition):
        self.form = AddResultForm()
        challange = [
            (challange["_id"], challange["name"])
            for challange in get_competition_challanges(competition["_id"])
        ]
        self.form.set_initial_values(challange=challange)
        return self.form

    def __init__(self):
        self.competition = None

    def get(self, competitions_slug):
        self.competition = get_competition(competitions_slug)
        enrolled_challanges = get_enrolled_challanges(
            current_user.id, self.competition["_id"]
        )
        return render_template(
            "add_result.html",
            form=self.form(self.competition),
            competition=self.competition,
            enrolled_challanges=enrolled_challanges,
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
            flash("Jesteś już zapisany do tej konkurencji", "warning")
            return render_template(
                "add_result.html",
                form=form,
                competition=self.competition,
                enrolled_challanges=enrolled_challanges,
            )


class GetResults(MethodView):
    decorators = [login_required]

    def get(self, competitions_slug):
        self.competition = get_competition(competitions_slug)
        results = get_results_request(self.competition["_id"])

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
        )


class EditResult(MethodView):
    decorators = [login_required]

    def __init__(self):
        self.form = EditResultForm()
        self.competition = None

    def get(self, competitions_slug, idk):
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
        self.form.set_initial_values(
            id=id,
            competitor=competitor,
            challange=challange,
            X=X,
            ten=ten,
            nine=nine,
            eight=eight,
            seven=seven,
            six=six,
            five=five,
            four=four,
            three=three,
            two=two,
            one=one,
            penalty=penalty,
            disqualification=disqualification,
        )
        return render_template(
            "edit_result.html", form=self.form, competition=self.competition
        )

    def post(self, competitions_slug, idk):
        form = self.form
        self.competition = get_competition(competitions_slug)
        if form.validate():
            put_result_request(
                self.form.id.data,
                self.form.X.data,
                self.form.ten.data,
                self.form.nine.data,
                self.form.eight.data,
                self.form.seven.data,
                self.form.six.data,
                self.form.five.data,
                self.form.four.data,
                self.form.three.data,
                self.form.two.data,
                self.form.one.data,
                self.form.penalty.data,
                self.form.disqualification.data,
            )
            return redirect(url_for("get_results", competitions_slug=competitions_slug))
        else:
            flash("Wrong values", "warning")
            return render_template(
                "edit_result.html", form=form, competition=self.competition
            )


class GetUsers(MethodView):
    decorators = [login_required]

    def get(self, competitions_slug):
        competition = get_competition(competitions_slug)
        users = User.query.all()
        return render_template("get_users.html", users=users, competition=competition)


class EditUser(MethodView):
    decorators = [login_required]

    def __init__(self):
        self.form = EditUserForm()
        self.competition = None
        self.edited_user = None

    def get(self, competitions_slug, user_id):
        self.competition = get_competition(competitions_slug)
        self.edited_user = User.query.filter_by(id=user_id).first()
        id = self.edited_user.id
        mail = self.edited_user.mail
        password = self.edited_user.password
        name = self.edited_user.name
        surname = self.edited_user.surname
        club = self.edited_user.club
        license = self.edited_user.license
        is_admin = str(self.edited_user.is_admin)
        is_refree = str(self.edited_user.is_refree)
        self.form.set_initial_values(
            id=id,
            mail=mail,
            password=password,
            name=name,
            surname=surname,
            club=club,
            license=license,
            is_admin=is_admin,
            is_refree=is_refree,
        )

        return render_template(
            "edit_user.html",
            form=self.form,
            competition=self.competition,
            user=self.edited_user,
        )

    def post(self, competitions_slug, user_id):
        print("post")
        form = self.form
        self.edited_user = User.query.filter_by(id=user_id).first()
        self.competition = get_competition(competitions_slug)

        admin_selection = {"False": 0, "True": 1}

        if form.validate():

            self.edited_user.is_admin = admin_selection[self.form.is_admin.data]
            self.edited_user.is_refree = admin_selection[self.form.is_refree.data]
            db.session.commit()

            return redirect(url_for("GetUsers", competitions_slug=competitions_slug))
        else:
            flash("Wrong values", "warning")
            return render_template(
                "edit_user.html",
                form=form,
                competition=self.competition,
                user=self.edited_user,
            )


class Logout(MethodView):
    def get(self, competitions_slug):
        logout_user()
        return redirect(url_for("Home", competitions_slug=competitions_slug))


def password_checker(user_password, form_password):
    return bcrypt.check_password_hash(user_password, form_password)


@login_manager.user_loader
def load_user(mail):
    return User.query.get(mail)
