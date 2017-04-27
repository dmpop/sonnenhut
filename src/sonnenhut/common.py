from astral import Astral, GoogleGeocoder
import configparser, feedparser, os, requests
import json


def getconfig(configfile = 'sonnenhut.ini'):
    """
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


def getdarksky(api_key, location):
    """
    Get weather data for the given location
    :return: weather data dictionary
    :rtype: dict
    """
    meteodict = {}
    URL = 'https://api.darksky.net/forecast/{key}/{lat},{long}?units=si'
    meteo = requests.get(URL.format(key=api_key, lat=location.latitude, long=location.longitude))
    if meteo.status_code != 200:
        raise requests.RequestException()
    meteo = meteo.json()
    try:
        meteodict['week'] = meteo['daily']['summary']
    except:
        meteodict['week'] = '?'
    try:
        meteodict['today'] = meteo['daily']['data'][1]['summary']
    except:
        meteodict['today'] = '?'
    try:
        meteodict['temp'] = '{:.2f}'.format(meteo['currently']['temperature'])
    except:
        meteodict['temp'] = '?'
    try:
        meteodict['wind_speed'] = '{:.2f}'.format(meteo['currently']['windSpeed'])
    except:
        meteodict['wind_speed'] = '?'
    try:
        meteodict['precip'] = '{:.0f}'.format(meteo['daily']['data'][2]['precipProbability']*100)
    except:
        meteodict['precip']  = '?'
    return meteodict
        

def fetchrss(config):
    """

    :param config: configparser already initialized
    :type config: :class:`configparser.ConfigParser`
    """
    rss_url = config.get('sonnenhut', 'rss_url')
    rss_count = config.get('sonnenhut', 'rss_article_no')
    rss = feedparser.parse(rss_url)
    count = 1
    html_feed = []
    for post in rss.entries:
        if count <= int(rss_count):
            item = '<p style="font-family:Lato"><a href="{post.link}">{post.title}</a></p>'.format(post=post)
            html_feed.append(item)
            count += 1
    feed = '<h2 style="font-family:Lato; letter-spacing: 3px">{title}</h2>{feed}'.format(title=rss['feed']['title'],
                                                                                         feed='\n'.join(html_feed))
    return feed
