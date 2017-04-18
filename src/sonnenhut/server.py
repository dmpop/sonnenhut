from astral import SUN_SETTING, SUN_RISING
from bottle import route, run
from sonnenhut.common import getlocation, getapi, getdarksky, goldenhour, getweather, fetchrss, getconfig
import datetime, os, configparser, markdown

@route('/sonnenhut/<city>')
def sonnenhut(city):
    config = getconfig()
    note_file = config.get('sonnenhut', 'note', fallback='').replace('$HOME', os.environ['HOME'])
    location = getlocation(city)
    api_key = getapi(config)

    golden_hour_sunrise = goldenhour(location, direction=SUN_RISING)
    golden_hour_sunset = goldenhour(location, direction=SUN_SETTING)

    general_info = ('\u2609 %s &bull; %s &bull; %.02f,%.02f' % (location.name,
                                                   location.timezone,
                                                   location.latitude,
                                                   location.longitude))
    golden_hour_sunrise_info = ('\u263C \u2197    '
                       '{hh:02d}:{mm:02d}:{ss:02d} \u231a {duration} ').format(hh=golden_hour_sunrise[0].hour,
                                                                               mm=golden_hour_sunrise[0].minute,
                                                                               ss=golden_hour_sunrise[0].second,
                                                                        duration=golden_hour_sunrise[1]-golden_hour_sunrise[0])
    golden_hour_sunset_info = ('\u263C \u2198    '
                      '{hh:02d}:{mm:02d}:{ss:02d} \u231a {duration}  ').format(hh=golden_hour_sunset[0].hour,
                                                                                 mm=golden_hour_sunset[0].minute,
                                                                                 ss=golden_hour_sunset[0].second,
                                                                        duration=golden_hour_sunset[1]-golden_hour_sunset[0])

    meteo = getdarksky(api_key, location)
        
    if os.path.isfile(note_file):
        f = open(note_file,'r')
        note = '<style>html * {font-family: Lato !important;}</style>' + (markdown.markdown(f.read()))
        f.close()
    else:
        f = open(note_file, 'w')
        f.write('Notes go here. Markdown is supported.')
        f.close()
        note = '<p style="font-family:Lato">New sonnenhut.md file has been created.</p>'
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
            '<h2 style="font-family:Lato; letter-spacing: 3px">Current Weather</h2>'
            '<p style="font-family:Lato">{} &bull; {}m/s &bull; \u2614 {}%</p>'
            '<h2 style="font-family:Lato; letter-spacing: 3px">Notes</h2>'
            '{}'
            '{}').format(general_info,
                         city,
                         golden_hour_sunrise_info,
                         golden_hour_sunset_info,
                         meteo['summary'],
                         meteo['wind_speed'],
                         meteo['precip'],
                         note,
                         rss_feed)
