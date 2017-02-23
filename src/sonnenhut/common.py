from astral import Astral, GoogleGeocoder
import pyowm

def getlocation(city):
    """
    Return the geographical coordinates for the specified city
    Throws AstralError if unable to locate the city.

    :param str city: The name of the desired city
    :return: geographical coordinates
    :rtype: :class:`astral.Location`
    """
    return Astral(GoogleGeocoder)[city]


def initowm(apikey = 'f2871760abe7535464065759cf85bd3c'):
    """
    Initialize OpenWeatherMap service

    :param str apikey: API key for the OWM service
    :return:
    :rtype:
    """
    return pyowm.OWM(apikey)


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
    

def getweather(owm, location):
    """
    Get weather data for the given location

    :param owm: OpenWeatherMap API
    :type owm: :class:`pyowm.webapi25.owm25.OWM25`
    :param location: location of the specified city
    :type location: :class:`astral.Location`
    :return: weather data dictionary
    :rtype: dict
    """
    weatherdict = {}
    weather = owm.weather_at_coords(location.latitude, location.longitude)
    w = weather.get_weather()
    weatherdict['status'] = w.get_status()
    weatherdict['wind_speed'] = w.get_wind().get('speed', 'N/A')
    weatherdict['temp'] = w.get_temperature('celsius').get('temp', 'N/A')
    weatherdict['humidity'] = w.get_humidity()
    return weatherdict


def forecast(owm, location):
    """
    Get weather forecast, return rain and snow status

    :param owm: OpenWeatherMap API
    :type owm: :class:`pyowm.webapi25.owm25.OWM25`
    :param location: location of the specified city
    :type location: :class:`astral.Location`
    :return: tuple with Boolean rain and snow
    :rtype: tuple
    """
    forecast = owm.daily_forecast_at_coords(location.latitude, location.longitude, limit=None)
    next_3_hours = pyowm.utils.timeutils.next_three_hours(date=None)
    rain = forecast.will_be_rainy_at(next_3_hours)
    snow = forecast.will_be_snowy_at(next_3_hours)
    return rain, snow
