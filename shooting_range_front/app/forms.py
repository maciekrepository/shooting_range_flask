from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from .models import User
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    StringField,
    validators,
    DateField,
    SelectField,
    IntegerField,
)
from .requests import get_competitions


class RegisterForm(FlaskForm):
    mail = StringField(
        validators=[InputRequired(), Length(min=1, max=50)],
        render_kw={"placeholder": "Email"},
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=1, max=20)],
        render_kw={"placeholder": "Password"},
    )
    name = StringField(
        validators=[InputRequired(), Length(min=1, max=20)],
        render_kw={"placeholder": "Imię"},
    )
    surname = StringField(
        validators=[InputRequired(), Length(min=1, max=20)],
        render_kw={"placeholder": "Nazwisko"},
    )
    club = StringField(render_kw={"placeholder": "Klub"})
    license = StringField(render_kw={"placeholder": "Licencja"})
    submit = SubmitField("Rejestruj")

    def validate_username(self, mail):
        existing_user_mail = User.query.filter_by(mail=mail.data).first()
        if existing_user_mail:
            raise ValidationError("User already exists")


class LoginForm(FlaskForm):
    mail = StringField(
        validators=[InputRequired(), Length(min=1, max=50)],
        render_kw={"placeholder": "Mail"},
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=1, max=20)],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Login")


class AddCompetitionForm(FlaskForm):
    name = StringField(
        validators=[InputRequired(), Length(min=1, max=20)],
        render_kw={"placeholder": "Nazwa"},
    )
    date = DateField(validators=[InputRequired()], render_kw={"placeholder": "Data"})
    registration_opened = SelectField(
        validators=[InputRequired(), Length(min=1, max=20)],
        choices=[("Otwarta", "Otwarta"), ("Zamknięta", "Zamknięta")],
        render_kw={"placeholder": "Rejestracja otwarta"},
    )
    submit = SubmitField("Dodaj zawody")


class AddChallangeForm(FlaskForm):
    name = StringField(
        validators=[InputRequired(), Length(min=1, max=20)],
        render_kw={"placeholder": "Nazwa konkurencji"},
    )
    number_of_missiles = IntegerField(
        validators=[InputRequired()], render_kw={"placeholder": "Liczba strzałów"}
    )
    competition = SelectField(
        validators=[InputRequired(), Length(min=1, max=20)],
        choices=[],
        render_kw={"placeholder": "Zawody"},
        label="Zawody:0",
    )
    submit = SubmitField("Dodaj zawody")

    def set_initial_values(self, *args, **kwargs):
        self.competition.choices = kwargs["choices"]


class AddResultForm(FlaskForm):
    challange = SelectField(
        validators=[InputRequired(), Length(min=1, max=20)],
        choices=[],
        render_kw={"placeholder": "Zawody"},
        label="Zawody:0",
    )

    submit = SubmitField("Dodaj zawody")

    def set_initial_values(self, *args, **kwargs):
        self.challange.choices = kwargs["challange"]


class EditResultForm(FlaskForm):
    id = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Id"})
    challange = IntegerField(
        validators=[InputRequired()], render_kw={"placeholder": "konkurencja"}
    )
    competitor = IntegerField(
        validators=[InputRequired()], render_kw={"placeholder": "zawodnik"}
    )
    X = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "X"})
    ten = IntegerField(
        validators=[InputRequired()], render_kw={"placeholder": "10"}, label="10"
    )
    nine = IntegerField(
        validators=[InputRequired()], render_kw={"placeholder": "9"}, label="9"
    )
    eight = IntegerField(
        validators=[InputRequired()], render_kw={"placeholder": "8"}, label="8"
    )
    seven = IntegerField(
        validators=[InputRequired()], render_kw={"placeholder": "7"}, label="7"
    )
    six = IntegerField(
        validators=[InputRequired()], render_kw={"placeholder": "6"}, label="6"
    )
    five = IntegerField(
        validators=[InputRequired()], render_kw={"placeholder": "5"}, label="5"
    )
    four = IntegerField(
        validators=[InputRequired()], render_kw={"placeholder": "4"}, label="4"
    )
    three = IntegerField(
        validators=[InputRequired()], render_kw={"placeholder": "3"}, label="3"
    )
    two = IntegerField(
        validators=[InputRequired()], render_kw={"placeholder": "2"}, label="2"
    )
    one = IntegerField(
        validators=[InputRequired()], render_kw={"placeholder": "1"}, label="1"
    )
    penalty = IntegerField(
        validators=[InputRequired()], render_kw={"placeholder": "kara"}, label="Kara"
    )
    disqualification = IntegerField(
        validators=[InputRequired()],
        render_kw={"placeholder": "dyskwalifikacja"},
        label="Dyskwalifikacja",
    )

    submit = SubmitField("Dodaj zawody")

    def set_initial_values(self, *args, **kwargs):
        self.id.data = kwargs["id"]
        self.challange.data = kwargs["challange"]
        self.competitor.data = kwargs["competitor"]
        self.X.data = kwargs["X"]
        self.ten.data = kwargs["ten"]
        self.nine.data = kwargs["nine"]
        self.eight.data = kwargs["eight"]
        self.seven.data = kwargs["seven"]
        self.six.data = kwargs["six"]
        self.five.data = kwargs["five"]
        self.four.data = kwargs["four"]
        self.three.data = kwargs["three"]
        self.two.data = kwargs["two"]
        self.one.data = kwargs["one"]
        self.penalty.data = kwargs["penalty"]
        self.disqualification.data = kwargs["disqualification"]


class EditUserForm(FlaskForm):
    id = IntegerField(validators=[InputRequired()], render_kw={"placeholder": "Id"})
    mail = StringField(validators=[InputRequired()], render_kw={"placeholder": "mail"})
    password = StringField(
        validators=[InputRequired()], render_kw={"placeholder": "password"}
    )
    name = StringField(validators=[InputRequired()], render_kw={"placeholder": "name"})
    surname = StringField(
        validators=[InputRequired()], render_kw={"placeholder": "surname"}
    )
    club = StringField(validators=[], render_kw={"placeholder": "club"})
    license = StringField(validators=[], render_kw={"placeholder": "license"})
    is_admin = SelectField(
        validators=[InputRequired(), Length(min=1, max=20)],
        choices=[(False, False), (True, True)],
        render_kw={"placeholder": "Admin"},
        label="Admin",
    )
    is_refree = SelectField(
        validators=[InputRequired(), Length(min=1, max=20)],
        choices=[(False, False), (True, True)],
        render_kw={"placeholder": "Refree"},
        label="Refree",
    )
    submit = SubmitField("Zapisz")

    def set_initial_values(self, *args, **kwargs):
        self.id.data = kwargs["id"]
        self.mail.data = kwargs["mail"]
        self.password.data = kwargs["password"]
        self.name.data = kwargs["name"]
        self.surname.data = kwargs["surname"]
        self.club.data = kwargs["club"]
        self.license.data = kwargs["license"]
        self.is_admin.data = kwargs["is_admin"]
        self.is_refree.data = kwargs["is_refree"]
