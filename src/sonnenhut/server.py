import os
import markdown
import requests
import sys
from astral import SUN_RISING, SUN_SETTING
from bottle import route, run
from sonnenhut.common import (fetchrss, getapi, getconfig, getdarksky,
                              getlocation, goldenhour)


@route('/sonnenhut/<city>')
def sonnenhut(city):

    config = getconfig()
    note_file = config.get('sonnenhut', 'note', fallback='').replace('$HOME', os.environ['HOME'])

    if os.path.isfile(note_file):
        f = open(note_file, 'r')
        note = '<style>html * {font-family: Lato !important;}</style>' + \
            (markdown.markdown(f.read()))
        f.close()
    else:
        f = open(note_file, 'w')
        f.write('Notes go here. Markdown is supported.')
        f.close()
        note = '<p style="font-family:Lato">New sonnenhut.md file has been created.</p>'

    try:
        response = requests.get("http://unsplash.com")
    except requests.ConnectionError:
            return ('<meta name="viewport" content="width=device-width">'
            '<title>S o n n e n h u t</title>'
            '<style>@import url("http://fonts.googleapis.com/css?family=Lato");</style>'
            '<h1 style="font-family:Lato; letter-spacing: 7px; color: #ffcc00">Sonnenhut</h1>'
            '<h2 style="font-family:Lato; letter-spacing: 3px">Notes</h2>'
            '{}').format(note)
            sys.exit()

    location = getlocation(city)
    api_key = getapi(config)

    golden_hour_sunrise = goldenhour(location, direction=SUN_RISING)
    golden_hour_sunset = goldenhour(location, direction=SUN_SETTING)

    general_info = ('\u2609 %s &bull; %s &bull; %.02f,%.02f' % (location.name,
                                                                location.timezone,
                                                                location.latitude,
                                                                location.longitude))
    golden_hour_sunrise_info = ('\u263C \u2197    '
                                '{hh:02d}:{mm:02d}:{ss:02d} \u231a {duration}'
                                ).format(hh=golden_hour_sunrise[0].hour,
                                         mm=golden_hour_sunrise[0].minute,
                                         ss=golden_hour_sunrise[0].second,
                                         duration=golden_hour_sunrise[1] - golden_hour_sunrise[0])
    golden_hour_sunset_info = ('\u263C \u2198    '
                               '{hh:02d}:{mm:02d}:{ss:02d} \u231a {duration}'
                               ).format(hh=golden_hour_sunset[0].hour,
                                        mm=golden_hour_sunset[0].minute,
                                        ss=golden_hour_sunset[0].second,
                                        duration=golden_hour_sunset[1] - golden_hour_sunset[0])

    meteo = getdarksky(api_key, location)
    rss_feed = fetchrss(config)

    return ('<meta name="viewport" content="width=device-width">'
            '<title>S o n n e n h u t</title>'
            '<style>@import url("http://fonts.googleapis.com/css?family=Lato");</style>'
            '<h1 style="font-family:Lato; letter-spacing: 7px; color: #ffcc00">Sonnenhut</h1>'
            '<h2 style="font-family:Lato; letter-spacing: 3px">Location</h2>'
            '<p style="font-family:Lato">{}</p>'
            '<h2 style="font-family:Lato; letter-spacing: 3px">Unsplash Photo</h2>'
            '<img src="https://source.unsplash.com/300x200/?{}">'
            '<br />'
            '<h2 style="font-family:Lato; letter-spacing: 3px">Golden Hour</h2>'
            '<p style="font-family:Lato">{}</p>'
            '<p style="font-family:Lato">{}</p>'
            '<h2 style="font-family:Lato; letter-spacing: 3px">Weather</h2>'
            '<p style="font-family:Lato">Forecast: {}'
            '<p style="font-family:Lato">Today: {}'
            '<p style="font-family:Lato">Temperature: {}°C</p>'
            '<p style="font-family:Lato">Wind speed: {}m/s</p>'
            '<p style="font-family:Lato">Precipitation probability: {}%</p>'
            '<p style="font-family:Lato">'
            '<a href="https://darksky.net/poweredby">Powered by Dark Sky</a></p>'
            '<h2 style="font-family:Lato; letter-spacing: 3px">Notes</h2>'
            '{}'
            '{}').format(general_info,
                         city,
                         golden_hour_sunrise_info,
                         golden_hour_sunset_info,
                         meteo['week'],
                         meteo['today'],
                         meteo['temp'],
                         meteo['wind_speed'],
                         meteo['precip'],
                         note,
                         rss_feed)
