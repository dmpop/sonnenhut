#

import configparser
import feedparser
from unittest.mock import patch, Mock, MagicMock

from sonnenhut.common import fetchrss

from data import RSS_SINGLE_ENTRY


@patch('sonnenhut.common.feedparser.parse')
def test_fetchrss(mock_parse):
    def get(section, key):
        data = {'rss_article_no': '7', 'rss_url': ''}
        return data[key]

    entries=[feedparser.FeedParserDict(RSS_SINGLE_ENTRY)]
    config = MagicMock(spec=configparser.ConfigParser)
    config.get.side_effects = get
    mock_parse.return_value = MagicMock(spec=feedparser.FeedParserDict,
                                        entries=entries)

    result = fetchrss(config)
    assert mock_parse.called


@patch('sonnenhut.common.feedparser.parse')
def test_fetchrss_empty(mock_parse):
    def get(section, key):
        data = {'rss_article_no': '7', 'rss_url': ''}
        return data[key]
    config = MagicMock(spec=configparser.ConfigParser)
    config.get.side_effects = get

    mock_parse.return_value = MagicMock(spec=feedparser.FeedParserDict,
                                        entries=[])
    result = fetchrss(config)
    # TODO: This needs a better idea how to test if there is NO entry
    # available...
    assert result

