import pytest
from x_client import XClient
from unittest.mock import MagicMock, patch

API_KEY = 'test_key'


@pytest.fixture
def client():
    client = XClient()
    client._api_key = API_KEY
    return client


@pytest.fixture
def tweet_data():
    tweet_data = {'data': [{'id': 41, 'text': 'first tweet'},
                           {'id': 42, 'text': 'second tweet'}]}
    return tweet_data


def test_get_auth_header(client):
    header = client._get_auth_header()

    assert header == {'Authorization': f'Bearer {API_KEY}'}


@patch('requests.get')
def test_make_request_success(mock_requests_get, client, tweet_data):

    response = MagicMock()
    response.ok = True
    response.status_code = 200
    response.json.return_value = tweet_data

    mock_requests_get.return_value = response

    data, status = client.make_request('/tweets/recent', query='xdevelopers',
                                       max_results=10)

    mock_requests_get.assert_called_once_with(
            'https://api.x.com/2/tweets/recent',
            params={'query': 'xdevelopers', 'max_results': 10},
            headers={'Authorization': f'Bearer {API_KEY}'})

    assert status == 200
    assert data == tweet_data['data']


@patch('requests.get')
def test_make_request_error(mock_requests_get, client):

    response_data = {'status': 429, 'reason': 'Rate limit exceeded'}

    response = MagicMock()
    response.ok = False
    response.status_code = 429
    response.json.return_value = response_data

    mock_requests_get.return_value = response

    data, status = client.make_request('/tweets/recent', query='xdevelopers',
                                       max_results=10)

    mock_requests_get.assert_called_once_with(
            'https://api.x.com/2/tweets/recent',
            params={'query': 'xdevelopers', 'max_results': 10},
            headers={'Authorization': f'Bearer {API_KEY}'})

    assert status == 429
    assert data == response_data


def test_get_user_posts(client):
    make_request_mock = MagicMock()
    client.make_request = make_request_mock

    client.get_user_posts('xdevelopers', max_results=11)
    make_request_mock.assert_called_once_with(
            '/tweets/search/recent',
            query='from:xdevelopers',
            max_results=11)


def test_get_hashtag_posts(client):
    make_request_mock = MagicMock()
    client.make_request = make_request_mock

    client.get_hashtag_posts('grumpycat', max_results=12)
    make_request_mock.assert_called_once_with(
            '/tweets/search/recent',
            query='#grumpycat',
            max_results=12)
