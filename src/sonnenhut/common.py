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
    meteo = requests.get('https://api.darksky.net/forecast/' + str(ds_api_key) + '/' + str(location.latitude) + ',' + str(location.longitude) + '?units=si').json()
    meteodict['summary'] = meteo['daily']['data'][1]['summary']
    meteodict['wind_speed'] = meteo['daily']['data'][5]['windSpeed']
    #meteodict['temp'] = w.get_temperature('celsius').get('temp', 'N/A')
    meteodict['precip'] = meteo['daily']['data'][2]['precipProbability']
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
            item = '<p style="font-family:Lato"><a href="' + post.link + '">' + post.title + '</a></p>'
            html_feed.append(item)
            count += 1
    #print(rss.feed.title)
    feed = '<h2 style="font-family:Lato; letter-spacing: 3px">' + rss['feed']['title'] +'</h2>' + '\n'.join(html_feed)
    return feed
