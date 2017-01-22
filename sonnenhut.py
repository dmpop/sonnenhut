#!/usr/bin/env python3

__author__ = "Dmitri Popov"
__copyright__ = "Copyleft 2016, Dmitri Popov"
__credits__ = ["Thomas Schraitle"]
__license__ = "GPLv3"
__version__ = "0.0.1"
__maintainer__ = "Dmitri Popov"
__email__ = "dpopov@suse.com"
__status__ = "Testing"

from astral import SUN_SETTING, SUN_RISING, Astral, GoogleGeocoder
import datetime, sys, os.path, forecastio

if len(sys.argv) > 1:
    city = sys.argv[1]
else:
    print(u'\u26a0 Looks like you forgot to specify a city.')
    quit()

city = sys.argv[1]
location = Astral(GoogleGeocoder)[city]

ds_api_key = "a07923ea4e7611a5501706475d5a9687"

print('---------------------------------')
timezone = location.timezone
print (u'\u2609 %s %s %.02f,%.02f' % (location.name, timezone, location.latitude, location.longitude))
print('---------------------------------')
sunrise = location.sunrise(date=None, local=True)
print (u'\u2600 \u2197    %s' % sunrise)
sunset = location.sunset(date=None, local=True)
print (u'\u2600 \u2198    %s' % sunset)
print('---------------------------------')

gh_sunrise = location.golden_hour(direction=SUN_RISING, date=None, local=True)
gh_sunset = location.golden_hour(direction=SUN_SETTING, date=None, local=True)

print (u"\u263C \u2197    {hh:02d}:{mm:02d}:{ss:02d} \u231a {duration} ".format(hh=gh_sunrise[0].hour, mm=gh_sunrise[0].minute, ss=gh_sunrise[0].second, duration=gh_sunrise[1]-gh_sunrise[0]))
print (u"\u263C \u2198    {hh:02d}:{mm:02d}:{ss:02d} \u231a {duration}    ".format(hh=gh_sunset[0].hour, mm=gh_sunset[0].minute, ss=gh_sunset[0].second, duration=gh_sunset[1]-gh_sunset[0]))
print('---------------------------------')

forecast = forecastio.load_forecast(ds_api_key, location.latitude, location.longitude)
hourly = forecast.hourly()
currently = forecast.currently()
print (u'\u2601 %s' % hourly.summary)
print (u'\u26C5 %s \u2614 %s' % (currently.temperature, currently.precipProbability))
print('---------------------------------')

if os.path.isfile('sonnenhut.txt'):
    tnote = open('sonnenhut.txt','r')
    print (tnote.read())
    tnote.close()
else:
    open(x, 'sonnenhut.txt').close()
