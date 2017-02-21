#!/usr/bin/env python3

__author__ = 'Dmitri Popov'
__copyright__ = 'Copyleft 2017, Dmitri Popov'
__credits__ = ['Thomas Schraitle']
__license__ = 'GPLv3'
__version__ = '1.0.1'
__maintainer__ = 'Dmitri Popov'
__email__ = 'dpopov@suse.com'
__URL__ = 'https://github.com/dmpop/sonnenhut'
__status__ = 'Development'

from astral import SUN_SETTING, SUN_RISING, Astral, GoogleGeocoder
import datetime, sys, os.path, pyowm
from bottle import route, redirect, run, debug

@route('/sonnenhut')
def sonnenhut():
    if len(sys.argv) > 1:
        city = sys.argv[1]
    else:
        return (u'\u26a0 Looks like you forgot to specify a city.')
    txt_path = 'sonnenhut.txt'
    owm_api_key = 'f2871760abe7535464065759cf85bd3c'
    try:
        location = Astral(GoogleGeocoder)[city]
    except:
        sys.exit(u'\u26a0 Failed to obtain geographical coordinates of the specified city.')

    owm = pyowm.OWM(owm_api_key)

    timezone = location.timezone
    general_info = (u'\u2609 %s %s %.02f,%.02f' % (location.name, timezone, location.latitude, location.longitude))

    gh_sunrise = location.golden_hour(direction=SUN_RISING, date=None, local=True)
    gh_sunset = location.golden_hour(direction=SUN_SETTING, date=None, local=True)

    gh_sunrise_line = (u'\u263C \u2197    {hh:02d}:{mm:02d}:{ss:02d} \u231a {duration} '.format(hh=gh_sunrise[0].hour, mm=gh_sunrise[0].minute, ss=gh_sunrise[0].second, duration=gh_sunrise[1]-gh_sunrise[0]))
    gh_sunset_line = (u'\u263C \u2198    {hh:02d}:{mm:02d}:{ss:02d} \u231a {duration}    '.format(hh=gh_sunset[0].hour, mm=gh_sunset[0].minute, ss=gh_sunset[0].second, duration=gh_sunset[1]-gh_sunset[0]))

    try:
        weather = owm.weather_at_coords(location.latitude, location.longitude)
    except:
        sys.exit(u'\u26a0 Failed to obtain weather data.')

    w = weather.get_weather()
    status = w.get_status()
    icon = w.get_weather_icon_name()
    wind_speed = w.get_wind()
    temp = w.get_temperature('celsius')
    humidity = w.get_humidity()

    try:
        forecast = owm.daily_forecast_at_coords(location.latitude, location.longitude, limit=None)
        next_3_hours = pyowm.utils.timeutils.next_three_hours(date=None)
        rain = forecast.will_be_rainy_at(next_3_hours)
        snow = forecast.will_be_snowy_at(next_3_hours)
        if rain == True or snow == True:
            precip = '\u2614'
        else:
            precip = '\u2713'
    except:
        precip = '\u26a0'

    if os.path.isfile(txt_path):
        txt_note = open(txt_path,'r')
        txt_note_print =(txt_note.read())
        txt_note.close()
    else:
        open(txt_path, 'a').close()

    return (u'<meta name="viewport" content="width=device-width"><h1 style="letter-spacing: 5px; color: #ffcc00">Sonnenhut</h1>%s<br /> <hr align=left width=250px>%s<br />%s<br /> <hr align=left width=250px> %s, %s°C, %sm/s, %s%% %s<br /> <hr align=left width=250px> %s' % (general_info, gh_sunrise_line, gh_sunset_line, status, temp['temp'], wind_speed['speed'], humidity, precip, txt_note_print))

run(host='0.0.0.0', port=8080, reloader=True)
