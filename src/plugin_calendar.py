# -*- coding: utf-8 -*-

"""This is plugin tp get calendar information.
   The code is basind on calendar_sq9atk module
   created by Paweł SQ9ATK.
"""

import logging
from astral import LocationInfo
from astral.sun import sun
from astral import moon
from datetime import datetime
import time
from datetime import datetime
from src import plugin_scaffold, module_helpers

class Calendar(plugin_scaffold.SR0WXPlugin):
    """Class to handle calendar data"""

    def __init__(self,language,lat, lon):
        self.__language = language
        self.__lat = lat
        self.__lon = lon
        self.__logger = logging.getLogger(__name__)

    def datetime_from_utc_to_local(self,utc_datetime):
        # Convert time to localtime
        now_timestamp = time.time()
        offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
        return utc_datetime + offset

    def get_data(self):
        # Main fuction to prepare and get data
        self.__logger.info(module_helpers.LogEntryPluginStep(_("Preparing data")))

        # Set location for calculations
        Location = LocationInfo(latitude=self.__lat,longitude=self.__lon)
        Sun = sun(Location.observer)
        
        # Prepare today's date
        date=self.__language.read_datetime(datetime.fromtimestamp((time.time())),"%d %B")
        
        # Calculate sunrise and sunset
        words_sunrise = self.__language.read_datetime(self.datetime_from_utc_to_local(Sun["sunrise"]), '%H %M')
        words_sunset = self.__language.read_datetime(self.datetime_from_utc_to_local(Sun["sunset"]), '%H %M')

        # Calculate moon phase
        phase = moon.phase(datetime.fromtimestamp(time.time()))
        if 0 <= phase < 6.99:  moon_phase = _('new moon')
        if 7 <= phase < 13.99:  moon_phase = _('first quarter')
        if 14 <= phase < 20.99:  moon_phase = _('full moon')
        if 21 <= phase < 27.99:  moon_phase = _('last quarter')
        
        # Build message
        sunrise = "".join([_("Sunrise"),".",words_sunrise,""])
        sunset = "".join([_("Sunset"),".",words_sunset,""])
        message = "".join([_("Timeline for"),".",date, ".",sunrise , ".",sunset ,".",moon_phase,"."])
        
        # Cleanup and return
        self.message = message
        self.source = "astral module"
        self.__logger.info(module_helpers.LogEntryPluginStep(_("Data was prepared")))
        
        # TBD: What else can astral provide?
        # TBD: Fix needed for english