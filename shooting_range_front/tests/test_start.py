from .test_client import client, app
from shooting_range_flask.shooting_range_front.app.requests import get_competitions
import json
import requests
from unittest.mock import patch
import unittest

class TestStart:

    @patch('requests.get')
    def test_should_return_200_if_response_is_valid(self, mocker, client):
        response = client.get('/')
        mocker.return_value.status_code = 200
        mocker.return_value.content = json.dumps({'name':'name1', 'slug':'name1', 'date':'2022-05-05', 'registration_opened':1})
        assert response.status_code == 200

    @patch('requests.get')
    def test_should_return_200_when_connection_error_raised(self, mocker, client):
        mocker.side_effect = requests.exceptions.ConnectionError()
        response = client.get('/')
        assert response.status_code == 200


    @patch('requests.get')
    def test_should_return_200_when_timeout_error_raised(self, mocker, client):
        mocker.side_effect = requests.exceptions.Timeout()
        response = client.get('/')
        assert response.status_code == 200




# @patch('mymodule.requests.get')
# def test_should_return_200_if_response_is_valid(client, fake_get):
#     expected = [{'name':'name1', 'slug':'name1', 'date':'2022-05-05', 'registration_opened':1}]
#     fake_get.return_value.json.return_value = expected
#     e = ExampleAPI()
#     self.assertEqual(e.fetch('http://web1:4000/competitions'), expected)
if __name__ == '__main__':
    unittest.main()