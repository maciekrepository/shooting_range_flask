from .test_client import client, app
from shooting_range_flask.shooting_range_front.app.requests import get_competitions
import json
import requests
from unittest.mock import patch
import unittest

class TestHome:

    @patch('requests.get')
    def test_should_return_200_if_response_is_valid(self, mocker, client):
        response = client.get('/competitions_slug')
        mocker.return_value.status_code = 200
        mocker.return_value.content = json.dumps({'name':'name1', 'slug':'competitions_slug', 'date':'2022-05-05', 'registration_opened':1})
        assert response.status_code == 200

    @patch('requests.get')
    def test_should_return_200_when_connection_error_raised(self, mocker, client):
        mocker.side_effect = requests.exceptions.ConnectionError()
        response = client.get('/competitions_slug')
        assert response.status_code == 200


    @patch('requests.get')
    def test_should_return_200_when_timeout_error_raised(self, mocker, client):
        mocker.side_effect = requests.exceptions.Timeout()
        response = client.get('/competitions_slug')
        assert response.status_code == 200