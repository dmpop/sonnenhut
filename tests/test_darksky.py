#
#

from unittest.mock import patch, Mock, MagicMock
from pytest import raises
import requests

from data import JSONDATA

from sonnenhut.common import getdarksky

APIKEY='123456789'

def create_mock(mock_get, **kwargs):
    """Change the requests.get object and return a pseudo astral.Location
       mock object

       :param mock_get: the requests.get Mock object
       :param dict kwargs: Currently recognize the following keys:
          * ok: the status of the response (bool)
          * status_code: a number indicates the response (200=ok, other is not ok;
            should be in line with ok. ok=True and status_code=400
            contradicts itself
          * return_value: something that should be returned after requests.get()
            is called (can be anything, but usually something dict-alike)
       :return: a Mock object with the attributes latitude and longitude
    """
    # Retrieve our keys from the kwargs dictionary and set default values
    # if there isn't a key available
    ok = kwargs.get('ok', False)
    status_code = kwargs.get('status_code', 400)
    return_value = kwargs.get('return_value', {})

    # Configure the mock to return a response with a status code.
    # Also, the mock should have a `json()` method that returns our data:
    mock_get.return_value = Mock(ok=ok, status_code=status_code)
    mock_get.return_value.json.return_value = return_value
    mock_loc = Mock(latitude=49.455556, longitude=11.078611)
    return mock_loc


@patch('sonnenhut.common.requests.get')
def test_getdarksky_called(mock_get):
    mock_loc = create_mock(mock_get, ok=True, status_code=200,
                           return_value=JSONDATA)
    result = getdarksky(APIKEY, mock_loc)
    assert mock_get.called


@patch('sonnenhut.common.requests.get')
def test_getdarksky__when_response_is_not_ok(mock_get):
    mock_loc = create_mock(mock_get, ok=False, status_code=400)
    with raises(requests.RequestException):
        result = getdarksky(APIKEY, mock_loc)


@patch('sonnenhut.common.requests.get')
def test_getdarksky_check_values(mock_get):
    mock_loc = create_mock(mock_get,
                           ok=True, status_code=200,
                           return_value=JSONDATA)
    result = getdarksky(APIKEY, mock_loc)

    # We check if we we have the following keys and values:
    for key, value in (('today', 'Light rain starting in the afternoon.'),
                       ('wind_speed', '5.64'),
                       ('precip', '59'),
                       ('temp', '8.70'),
                       ('week', ('Light rain today through Sunday, '
                                 'with temperatures rising to 21°C on Saturday.')),
                       ):
        assert result[key] == value
