#

from sonnenhut.common import getconfig
from unittest.mock import patch

from pytest import raises


@patch('sonnenhut.common.configparser.ConfigParser')
def test_getconfig_valid(mock_configparser):
    mock_configparser().read.return_value = ['x']
    config = getconfig()
    assert mock_configparser().read.called


@patch('sonnenhut.common.configparser.ConfigParser')
def test_getconfig_invalid(mock_configparser):
    mock_configparser().read.return_value = None
    with raises(FileNotFoundError):
        getconfig()

#
# Alternative tests, these are basically the same
# like the above, but I just want to make sure I got
# it right...
def test_getconfig_valid_with_monkeypatch(monkeypatch):
    from sonnenhut.common import configparser
    def mock_read(filenames, encoding=None):
        return filenames
    monkeypatch.setattr(configparser.ConfigParser,
                        'read', mock_read)
    config = getconfig()
    assert config


def test_getconfig_invalid_with_monkeypatch(monkeypatch):
    from sonnenhut.common import configparser
    def mock_read(filenames, encoding=None):
        return None

    monkeypatch.setattr(configparser.ConfigParser,
                        'read', mock_read)

    with raises(FileNotFoundError):
        getconfig()
