from .test_client import client, app
from shooting_range_flask.shooting_range_front.app.requests import get_competitions
import json
import requests
from unittest.mock import patch
import unittest


class FakeUser:
    def __init__(self):
        self.password = 'test'

class TestLoginView:


    @patch('requests.get')
    @patch('shooting_range_flask.shooting_range_front.app.keycloak_requests.check_role')
    @patch("shooting_range_flask.shooting_range_front.app.forms.LoginForm")
    @patch('shooting_range_flask.shooting_range_front.app.models.User')
    @patch('shooting_range_flask.shooting_range_front.app.main.password_checker')
    @patch('shooting_range_flask.shooting_range_front.app.main.login_user')
    def test_should_log_in_user_when_credentials_are_correct(self, login_user_mock, password_checker_mock, user_mock,
                                                             form_mocker, check_role_mock, request_mocker, client):
        request_mocker.return_value.content = json.dumps(
            {'name': 'name1', 'slug': 'name1', 'date': '2022-05-05', 'registration_opened': 1})
        request_mocker.return_value.status_code = 200
        form_mocker.validate.return_value = True
        user_mock.query.filter_by.return_value.first.return_value = FakeUser()
        password_checker_mock.return_value = True
        check_role_mock.return_value = 'admin'
        session_mock = dict()
        with patch('shooting_range_front.app.main.session', dict()) as session:
            response = client.post('/slug/login')
        user_mock.query.filter_by.return_value.first.assert_called_once()
        login_user_mock.assert_called_once()
        assert response.status_code == 302

    @patch('requests.get')
    @patch("shooting_range_flask.shooting_range_front.app.forms.LoginForm")
    @patch('shooting_range_flask.shooting_range_front.app.models.User')
    @patch('shooting_range_flask.shooting_range_front.app.main.password_checker')
    def test_should_log_in_user_when_credentials_are_not_correct(self, password_checker_mock, user_mock,
                                                             form_mocker, request_mocker, client):
        request_mocker.return_value.content = json.dumps(
            {'name': 'name1', 'slug': 'name1', 'date': '2022-05-05', 'registration_opened': 1})
        request_mocker.return_value.status_code = 200
        form_mocker.validate.return_value = True
        user_mock.query.filter_by.return_value.first.return_value = FakeUser()
        password_checker_mock.return_value = False
        session_mock = dict()
        with patch('shooting_range_front.app.main.session', dict()) as session:
            response = client.post('/slug/login')
        user_mock.query.filter_by.return_value.first.assert_called_once()
        assert response.status_code == 200

