#
from unittest.mock import patch, MagicMock
import pytest

from astral import SUN_RISING, SUN_SETTING
from sonnenhut.common import getapi, goldenhour


def test_getapi():
    from configparser import ConfigParser
    config = ConfigParser()
    apikey = '12345'
    config['sonnenhut'] = {'api_key': apikey}
    key = getapi(config)
    assert key == apikey


@pytest.mark.parametrize('direction',
                         [SUN_RISING, SUN_SETTING],
                         ids=['sun_up', 'sun_down'])
def test_goldenhour(direction):
    result = (123, 456)
    mock_location = MagicMock()
    mock_location.golden_hour.return_value = result

    gh = goldenhour(mock_location, direction)
    assert mock_location.golden_hour.called
    assert gh == result
