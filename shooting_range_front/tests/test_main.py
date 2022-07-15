from .test_client import client, app
from shooting_range_flask.shooting_range_front.app.requests import get_competitions



def test_should_return_200_if_response_is_valid(client, mocker):
    expected = [{'name':'name1', 'slug':'name1', 'date':'2022-05-05', 'registration_opened':1}, {'name':'name2', 'slug':'name2', 'date':'2022-05-05', 'registration_opened':1}]
    response = client.get('/')
    mocker.patch('shooting_range_flask.shooting_range_front.app.requests.get_competitions', return_value=expected)
    assert response.status_code == 200




# @patch('mymodule.requests.get')
# def test_should_return_200_if_response_is_valid(client, fake_get):
#     expected = [{'name':'name1', 'slug':'name1', 'date':'2022-05-05', 'registration_opened':1}]
#     fake_get.return_value.json.return_value = expected
#     e = ExampleAPI()
#     self.assertEqual(e.fetch('http://web1:4000/competitions'), expected)
