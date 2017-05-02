import configparser
import os

import feedparser
import requests
from astral import Astral, GoogleGeocoder


def getconfig(configfile='sonnenhut.ini'):
    """Read INI file or raise FileNotFoundError

    :param str configfile: filename (without path) to the INI file.
                           Will be searched relative to the sonnenhut lib
    :return: configuration options
    :rtype: :class:`configparser.ConfigParser`
    :raises: FileNotFoundError
    """
    config = configparser.ConfigParser()
    configfiles = config.read(os.path.join(os.path.dirname(__file__), configfile))
    if not configfiles:
        raise FileNotFoundError("No sonnenhut.ini found!")
    return config


def getlocation(city):
    """
    Return the geographical coordinates for the specified city
    Throws AstralError if unable to locate the city.

    :param str city: The name of the desired city
    :return: geographical coordinates
    :rtype: :class:`astral.Location`
    """
    return Astral(GoogleGeocoder)[city]


def getapi(config):
    """
    Get a Dark Sky API key

    :param config: configparser already initialized
    :type config: :class:`configparser.ConfigParser`
    :return: api_key string
    :rtype: string
    """
    api_key = config.get('sonnenhut', 'api_key')
    return api_key


def goldenhour(location, direction):
    """
    Return golden hour of sunset and sunrise depending on the direction

    :param location: location of the specified city
    :type location: :class:`astral.Location`
    :param direction: sun direction (up=sunrise, down=sunset)
    :type direction: int
    :return: tuple of start and end datetimes
    :rtype: tuple
    """
    return location.golden_hour(direction=direction, date=None, local=True)


def safeget(dct, *keys, default='?'):
    """Helper function to hide the ugliness of accessing nested dictionaries with lists

    >>> exampledict = {'a': {'b': 1, 'c': [{'aa': 23, 'bb': 45}], 'd': 3}}
    >>> safeget(exampledict, 'a', 'b')
    1
    >>> safeget(exampledict, 'a', 'x')
    '?'
    >>> safeget(exampledict, 'a', 'x', default='???')
    '???'
    >>> safeget(exampledict, 'a', 'c', 0, 'bb')
    45

    :param dict dct: Dictionary
    :param tuple keys: Keys to access, usually strings or integers
    :param str default: the default value if the keys couldn't be accessed
    :return: the value in the dictionary or the default value
    """
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            return default
    return dct


def getdarksky(api_key, location):
    """Get weather data for the given location

    :param str api_key: the API key from DarkSky
    :param location: the location
    :type location: :class:`astral.Location`
    :return: weather data dictionary
    :rtype: dict
    """
    meteodict = {}
    URL = 'https://api.darksky.net/forecast/{key}/{lat},{long}?units=si'
    meteo = requests.get(URL.format(key=api_key, lat=location.latitude, long=location.longitude))
    if meteo.status_code != 200:
        raise requests.RequestException()
    meteo = meteo.json()

    meteodict['week'] = safeget(meteo, 'daily', 'summary')
    meteodict['today'] = safeget(meteo, 'daily', 'data', 1, 'summary')
    meteodict['temp'] = '{:.2f}'.format(safeget(meteo,
                                                'currently', 'temperature',
                                                default=float('NaN')))
    meteodict['wind_speed'] = '{:.2f}'.format(safeget(meteo,
                                                      'currently', 'windSpeed',
                                                      default=float('NaN')))

    meteodict['precip'] = '{:.0f}'.format(safeget(meteo,
                                                  'daily', 'data', 2, 'precipProbability',
                                                  default=float('NaN'))*100)
    return meteodict


def process_rss(rss, max_show):
    """Process RSS entries

    :param rss: the result of ``feedparser.parse``
    :type rss: :class:`feedparser.FeedParserDict`
    :param int max_show: number of RSS articles to show
    :yield: string of HTML tags
    """
    for post in rss.entries[:max_show]:
        yield ('<p style="font-family:Lato">'
               '<a href="{post.link}">{post.title}</a>'
               '</p>').format(post=post)


def fetchrss(config):
    """Fetch a RSS stream

    :param config: configparser already initialized
    :type config: :class:`configparser.ConfigParser`
    """
    rss_url = config.get('sonnenhut', 'rss_url')
    rss_count = int(config.get('sonnenhut', 'rss_article_no'))
    rss = feedparser.parse(rss_url)

    # Create the feed string:
    feed = ('<h2 style="font-family:Lato; letter-spacing: 3px">{title}</h2>'
            '{feed}').format(title=rss['feed']['title'],
                             feed='\n'.join(process_rss(rss, rss_count)))
    return feed
