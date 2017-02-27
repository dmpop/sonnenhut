from astral import SUN_SETTING, SUN_RISING
from bottle import route, run
from sonnenhut.common import getlocation, initowm, goldenhour, getweather, forecast, fetchrss, getconfig
import datetime, os
import configparser

@route('/sonnenhut/<city>')
def sonnenhut(city):
    config = getconfig()
    note_file = config.get('sonnenhut', 'note', fallback='').replace('$HOME', os.environ['HOME'])
    location = getlocation(city)
    owm = initowm(config)

    gh_sunrise = goldenhour(location, direction=SUN_RISING)
    gh_sunset = goldenhour(location, direction=SUN_SETTING)

    general_info = ('\u2609 %s %s %.02f,%.02f' % (location.name,
                                                   location.timezone,
                                                   location.latitude,
                                                   location.longitude))
    gh_sunrise_line = ('\u263C \u2197    '
                       '{hh:02d}:{mm:02d}:{ss:02d} \u231a {duration} ').format(hh=gh_sunrise[0].hour,
                                                                               mm=gh_sunrise[0].minute,
                                                                               ss=gh_sunrise[0].second,
                                                                               duration=gh_sunrise[1]-gh_sunrise[0])
    gh_sunset_line = ('\u263C \u2198    '
                      '{hh:02d}:{mm:02d}:{ss:02d} \u231a {duration}    ').format(hh=gh_sunset[0].hour,
                                                                                 mm=gh_sunset[0].minute,
                                                                                 ss=gh_sunset[0].second,
                                                                                 duration=gh_sunset[1]-gh_sunset[0])

    weather = getweather(owm, location)

    rain, snow = forecast(owm, location)
    if rain == True or snow == True:
        precip = '\u2614'
    else:
        precip = '\u2713'
        
    if os.path.isfile(note_file):
        lst = []
        with open(note_file,'r') as text:
            for line in text:
                lst.append(line)
        note = '<br />'.join(lst)
    else:
        open(note_file, 'a').close()

    rss_feed = fetchrss(config)

    return ('<meta name="viewport" content="width=device-width">'
            '<h1 style="letter-spacing: 5px; color: #ffcc00">Sonnenhut</h1>'
            '<h2>Location</h2>'
            '{}<br />'
            '<h2>Unsplash Photo</h2>'
            '<img src="https://source.unsplash.com/500x350/?{}">'
            '<br />'
            '<h2>Golden Hour</h2>'
            '{} <br />'
            '{}'
            '<h2>Current Weather</h2>'
            '{}, {}°C, {}m/s, {}% {}<br />'
            '<h2>Notes</h2>'
            '{}'
            '<br />'
            '{}').format(general_info,
                         city,
                         gh_sunrise_line,
                         gh_sunset_line,
                         weather['status'],
                         weather['temp'],
                         weather['wind_speed'],
                         weather['humidity'],
                         precip,
                         note,
                         rss_feed)
