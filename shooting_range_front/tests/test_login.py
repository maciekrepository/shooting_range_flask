from .test_client import client, app
from shooting_range_flask.shooting_range_front.app.requests import get_competitions
import json
import requests
from unittest.mock import patch
import unittest

class TestLoginView:

    # @patch('requests.get')
    # def test_should_return_200_if_response_is_valid(self, mocker, client):
    #     response = client.get('/slug/login')
    #     mocker.return_value.status_code = 200
    #     mocker.return_value.content = json.dumps({'name':'name1', 'slug':'name1', 'date':'2022-05-05', 'registration_opened':1})
    #     assert response.status_code == 200
    #
    # @patch('requests.get')
    # def test_should_return_200_when_connection_error_raised(self, mocker, client):
    #     mocker.side_effect = requests.exceptions.ConnectionError()
    #     response = client.get('/slug/login')
    #     assert response.status_code == 200
    #
    #
    # @patch('requests.get')
    # def test_should_return_200_when_timeout_error_raised(self, mocker, client):
    #     mocker.side_effect = requests.exceptions.Timeout()
    #     response = client.get('/slug/login')
    #     assert response.status_code == 200

    @patch('requests.get')
    @patch('shooting_range_flask.shooting_range_front.app.forms.LoginForm.validate')
    @patch('shooting_range_flask.shooting_range_front.app.models.User')
    @patch('shooting_range_flask.shooting_range_front.app.main.password_checker')
    @patch('shooting_range_flask.shooting_range_front.app.main.login_user')
    # @patch('shooting_range_front.app.main.session')
    def test_should_log_in_user_when_credentials_are_correct(self, login_user_mock,  password_checker_mock, user_mock, form_mocker, request_mocker,  client):
        request_mocker.return_value.content = json.dumps({'name': 'name1', 'slug': 'name1', 'date': '2022-05-05', 'registration_opened': 1})
        request_mocker.return_value.status_code = 200
        form_mocker.return_value = True
        user_mock.filter_by.return_value.first.return_value = 'dummy_data'
        user_mock.filter_by.return_value.first.assert_called_once()
        password_checker_mock.return_value = True
        login_user_mock.assert_called_once()
        session_mock = dict()
        with patch('shooting_range_front.app.main.session', dict()) as session:
            response = client.post('/slug/login')
        assert response.status_code == 302



