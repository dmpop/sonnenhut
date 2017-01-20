#!/usr/bin/env python3

__author__ = "Dmitri Popov"
__copyright__ = "Copyleft 2016, Dmitri Popov"
__credits__ = ["Thomas Schraitle"]
__license__ = "GPLv3"
__version__ = "0.0.1"
__maintainer__ = "Dmtiri Popov"
__email__ = "dpopov@suse.com"
__status__ = "Testing"

from astral import SUN_SETTING, SUN_RISING, Astral, GoogleGeocoder
import datetime, sys

city = sys.argv[1]
location = Astral(GoogleGeocoder)[city]

print('---------------------------------')
timezone = location.timezone
print('Timezone: %s' % timezone)
print('Coordinates: %.02f,%.02f' % (location.latitude, location.longitude))
print('---------------------------------')
sunrise = location.sunrise(date=None, local=True)
print (u'\u2600 \u2191    %s' % sunrise)
sunset = location.sunset(date=None, local=True)
print (u'\u2600 \u2193    %s' % sunset)
print('---------------------------------')

golden_hour_sunrise = location.golden_hour(direction=SUN_RISING, date=None, local=True)
golden_hour_sunset = location.golden_hour(direction=SUN_SETTING, date=None, local=True)

print (u"\u263C \u2191 {hh:02d}:{mm:02d}:{ss:02d} \u231a {duration} ".format(hh=golden_hour_sunrise[0].hour, mm=golden_hour_sunrise[0].minute, ss=golden_hour_sunrise[0].second, duration=golden_hour_sunrise[1]-golden_hour_sunrise[0]))
print (u"\u263C \u2193 {hh:02d}:{mm:02d}:{ss:02d} \u231a {duration} ".format(hh=golden_hour_sunset[0].hour, mm=golden_hour_sunset[0].minute, ss=golden_hour_sunset[0].second, duration=golden_hour_sunset[1]-golden_hour_sunset[0]))
print('---------------------------------')
