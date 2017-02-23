#

from sonnenhut.common import getlocation, forecast, getweather
from unittest.mock import patch, Mock, MagicMock
import astral
import pyowm
import datetime


@patch('sonnenhut.common.Astral')
def test_getlocation(mock_astral):
    city = 'tokyo'
    mock_astral.return_value = {city: city}
    assert getlocation(city) == city


@patch('sonnenhut.common.pyowm.utils.timeutils')
@patch('sonnenhut.common.pyowm')
def test_forecast(mock_owm, mock_timeutils):
    nbg_loc = astral.Location(info=("Germany", "Nürnberg", 49.43, 11.08, "Europe/Berlin", 318))

    fc = Mock() # spec=pyowm.webapi25.forecaster.Forecaster
    fc.will_be_rainy_at.return_value = True
    fc.will_be_snowy_at.return_value = False

    mock_owm.daily_forecast_at_coords.return_value = fc
    mock_timeutils.next_three_hours.return_value = Mock(spec=datetime.datetime)
    
    rain, snow = forecast(mock_owm, nbg_loc)
    assert mock_owm.daily_forecast_at_coords.called
    assert mock_timeutils.next_three_hours.called
    assert fc.will_be_rainy_at.called
    assert fc.will_be_snowy_at.called


@patch('sonnenhut.common.pyowm')
def test_getweather(mock_owm):
    nbg_loc = astral.Location(info=("Germany", "Nürnberg", 49.43, 11.08, "Europe/Berlin", 318))
    observation = Mock()
    resultdict = {'wind_speed': 1.1, 'temp': 5.7, 'status': "Clear", 'humidity': 87, }
    weather = Mock()
    observation.get_weather.return_value = weather
    weather.get_status.return_value = "Clear"
    weather.get_wind.return_value = {"speed": 1.1}
    weather.get_temperature.return_value = {"temp": 5.7}
    weather.get_humidity.return_value = 87
    mock_owm.weather_at_coords.return_value = observation
    weatherdict = getweather(mock_owm, nbg_loc)
    assert observation.get_weather.called
    assert weatherdict == resultdict
