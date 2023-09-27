# -*- coding: utf-8 -*-

"""Plugin to send station information to the clusters
   this includes http://wx.ostol.pl/.
   
   This was oryginally created by Michal Sadowski SQ6JNX
"""

#
#   Copyright 2009-2014 Michal Sadowski (sq6jnx at hamradio dot pl)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

from base64 import urlsafe_b64encode
import logging
import json

import urllib.request
import urllib.error

from src import plugin_scaffold,module_helpers


class ActivityMap(plugin_scaffold.SR0WXPlugin):
    """This module does not give any data, it just contacts application to mark
station on the map.

Parameters:
    - `callsign`: your station callsign
    - `latitude`, `longitude`: geographic position of station
    - `above_sea_level`: antenna's height a.s.l.
    - `above_ground_level`: antenna's height a.g.l.
    - `station_range`: station's range in normal conditions, in kilometers
    - `additional_info`: additional information to show on website
    - `service_url`: mapping service url, defaults to SQ9ATK service
    - `lang`: language used by installation
    """
    def __init__(self, callsign, latitude, longitude,
                 above_sea_level, above_ground_level, station_range,
                 additional_info="", service_url="", active = False, lang=""):
        self.__callsign = callsign
        self.__latitude = latitude
        self.__longitude = longitude
        self.__hour_quarter = 0
        self.__above_sea_level = above_sea_level
        self.__above_ground_level = above_ground_level
        self.__station_range = station_range
        self.__additional_info = additional_info
        self.__service_url = service_url
        self.active = active
        self.__lang = lang
        self.__logger = logging.getLogger(__name__)

    def get_data(self):
        """This module does NOT return any data! It is here just to sendd
        data to map utilities."""
        
        # Prepare data
        self.__logger.info(module_helpers.LogEntryPluginStep(_("Preparing data")))
        station_info = {
            "callsign": self.__callsign,
            "lat": self.__latitude,
            "lon": self.__longitude,
            "q": self.__hour_quarter,
            "asl": self.__above_sea_level,
            "agl": self.__above_ground_level,
            "range": self.__station_range,
            "info": self.__additional_info,
            "lang": self.__lang
        }

        dump = json.dumps(station_info, separators=(',', ':'))
        data_bytes = dump.encode("utf-8")
        b64data = urlsafe_b64encode(data_bytes)
        url = self.__service_url + b64data.decode()
        self.__logger.info(module_helpers.LogEntryPluginStep(_("Data was prepared")))
        
        # Send data
        self.__logger.info(module_helpers.LogEntryPluginStep(_("Sending data to"))+" " + url)
        try:
            page = urllib.request.urlopen(url)
            response = page.read()

            if response == b'OK':
                self.__logger.info(module_helpers.LogEntryPluginStep(_("Data was send, confirmation received")))
            else:
                log = _("Non-OK response received from %s, (%s)")
                self.__logger.exception(_("Could't send data or wrong response from the server"))
                self.__logger.error(log, self.__service_url, response)
            return dict()

        except urllib.error.HTTPError as e:
            print(e)
            # TBD - Error handling for this plugin















