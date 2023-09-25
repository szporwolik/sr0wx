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
from src import plugin_scaffold

class Calendar(plugin_scaffold.SR0WXPlugin):
    """Klasa pobierająca dane kalendarzowe"""

    def __init__(self,language,lat, lon):
        self.__language = language
        self.__lat = lat
        self.__lon = lon
        self.__logger = logging.getLogger(__name__)

    def hourToNumbers(self, time="00:00"):
        datetime_object = datetime.strptime(time, '%H:%M')
        time_words = self.__language.read_datetime(datetime_object, '%H %M')
        return time_words

    def datetime_from_utc_to_local(self,utc_datetime):
        now_timestamp = time.time()
        offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
        return utc_datetime + offset

    def get_data(self):
        self.__logger.info("::: Processing data")

        Location = LocationInfo(latitude=self.__lat,longitude=self.__lon)
        Sun = sun(Location.observer)
        
        words_sunrise = self.__language.read_datetime(self.datetime_from_utc_to_local(Sun["sunrise"]), '%H %M')
        words_sunset = self.__language.read_datetime(self.datetime_from_utc_to_local(Sun["sunset"]), '%H %M')
 
        phase = moon.phase(datetime.fromtimestamp(time.time()))
        if 0 <= phase < 6.99:  moon_phase= 'nów'
        if 7 <= phase < 13.99:  moon_phase= 'kwadra pierwsza'
        if 14 <= phase < 20.99:  moon_phase= 'pełnia'
        if 21 <= phase < 27.99:  moon_phase= 'ostatnia kwadra'
        
        date=self.__language.read_datetime(datetime.fromtimestamp((time.time())),"%d %B")
        sunrise = "".join(["Wschód słońca"," godzina ",words_sunrise,""])
        sunset = "".join(["Zachód słońca"," godzina ",words_sunset,""])

        message = "".join(["Kalendarium na.",date, ".",sunrise , ".",sunset ,".",moon_phase,"."])
        
        self.__logger.info("::: Data prepared")
        return {
            "message": message,
            "source": "calendar_zoznam_sk",
        }







