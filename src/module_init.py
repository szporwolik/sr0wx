import logging, logging.handlers
import src.lang_pl as lang_pl
import config

# constanst

COLOR_HEADER = '\033[95m'
COLOR_OKBLUE = '\033[94m'
COLOR_OKGREEN = '\033[92m'
COLOR_WARNING = '\033[93m'
COLOR_FAIL = '\033[91m'
COLOR_BOLD = '\033[1m'
COLOR_UNDERLINE = '\033[4m'
COLOR_ENDC = '\033[0m'

LICENSE = COLOR_OKBLUE + """                                      
Copyright 2009-2014 Michal Sadowski (sq6jnx at hamradio dot pl)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

-----------------------------------------------------------

You can find full list of contributors on:
- github.com/sq6jnx/sr0wx.py
- github.com/sq9atk/sr0wx

""" + COLOR_ENDC

# Logging configuration
log_line_format = '%(asctime)s %(name)s %(levelname)s: %(message)s'
log_handlers = [{
        'log_level': logging.INFO,
        'class': logging.StreamHandler,
        'config': {'stream': None},
    },{
        'log_level': logging.DEBUG,
        'class': logging.handlers.TimedRotatingFileHandler,
        'config': {
            'filename': 'logs\sr0wx.log',
            'when': 'D',
            'interval': 1,
            'backupCount': 30,
            'delay': True,
            'utc': True,
        }
    }]

lang = "pl"
pygame_bug = 0

data_sources_error_msg = ['Data source is not not available']
read_sources_msg = True
    
# -------------
# Module - activity_map
# ------------
# This module sends status messages to https://ostol.pl/, strongly recommended to have it active to track the SR0WX community

from src import plugin_activity_map
plugin_activitymap = plugin_activity_map.ActivityMap(
    service_url="http://wx.ostol.pl/map_requests?base=",
    callsign=config.callsign,
    latitude=54.655245,
    longitude=19.268097,
    above_sea_level=225,
    above_ground_level=20,
    station_range=65,
    additional_info= "Automatic weather station",
)

# ===============
# Global Modules
# ===============

# ---------------
# calendar_sq9atk
# ---------------
# Calendar module, full list of locations can be find at http://calendar.zoznam.sk
"""
from calendar_sq9atk import CalendarSq9atk
calendarsq9atk = CalendarSq9atk(
    language=pl_google,
    service_url="http://calendar.zoznam.sk/sunset-pl.php?city=",
    city_id=3094802,        # Example -> Kraków
)
"""
# ---------------
# Module - openweather_sq9atk
# ---------------
# Weather module basing on openweathermap service
# Visit https://openweathermap.org/api to get the API key, all you need is to register
"""
from openweather_sq9atk import OpenWeatherSq9atk
openweathersq9atk = OpenWeatherSq9atk(
    language = pl_google,
    api_key = 'ee78911a0fb560b58144230f46e0d4b2',
    lat = 50,
    lon = 20,
    service_url = 'http://api.openweathermap.org/data/2.5/'
)
"""
# ---------------
# Module - openweather
# ---------------
# Weather module basing on openweathermap service
# Visit https://openweathermap.org/api to get the API key, all you need is to register

from src import plugin_openweather
plugin_openweather = plugin_openweather.OpenWeather(
    language = lang_pl,
    api_key = 'ee78911a0fb560b58144230f46e0d4b2',
    lat = 50,
    lon = 20,
    service_url = 'http://api.openweathermap.org/data/2.5/'
)

# ---------------
# radioactive_sq9atk
# ---------------
# Radioactive module, full list of stations can be find at http://radioactiveathome.org/map/
"""
from radioactive_sq9atk import RadioactiveSq9atk
radioactivesq9atk = RadioactiveSq9atk(
    language=pl_google,
    service_url="http://radioactiveathome.org/map/",
    sensor_id=35167         # Example -> Kraków
)
"""
# ---------------
# airly_sq9atk
# ---------------
# Airly.org based air pollution module. 
# Visit https://developer.airly.org/ to get the API key, all you need is to register
"""
from airly_sq9atk import AirlySq9atk
airlysq9atk = AirlySq9atk(
    language = pl_google,
    api_key = '02b3a79363c3497dbb992093cd9d7779',
    service_url = 'https://airapi.airly.eu/v2/measurements', #location
    mode = 'nearest',       # Possible options: point|nearest|installationId
    lat = 50.079242,
    lon = 18.516138,
    maxDistanceKM = 5,      # Distance for 'nearest' calculation
    installationId = 8077,  # Specific airly installation ID, Example -> Kraków, ul. Mikołajska
)
"""
# ---------------
# vhf_propagation_sq9atk
# ---------------
# VHF Propagation module
"""
from vhf_tropo_sq9atk import VhfTropoSq9atk
vhftroposq9atk = VhfTropoSq9atk(
    language=pl_google,
    service_url="https://www.dxinfocentre.com/tropo_eur.html",
    qthLon=20.00,
    qthLat=50.00
)
"""
# ---------------
# propagation_sq9atk
# ---------------
# HF Propagation module
"""
from propagation_sq9atk import PropagationSq9atk
propagationsq9atk = PropagationSq9atk(
    language=pl_google,
    service_url="https://rigreference.com/solar/img/tall",
)
"""
# ===============
# Country specific modules
# ===============

# -------------
# Module - imgw_podest_sq9atk
# ------------
# Polish water gauge level module, full list of water gauges can be pulled from http://wx.ostol.pl/wodowskazy/
"""
from imgw_podest_sq9atk import ImgwPodestSq9atk
imgwpodestsq9atk = ImgwPodestSq9atk(
    wodowskazy = [
            '2.149200290',   # Example -> Name: Muszyna, river: Poprad
            '2.150190340',   # Example -> Name: Kraków-Bielany, river: Wisła
    ]
)
"""
# --------------------
# air_pollution_sq9atk
# --------------------
# Polish air pollution module, full list of stations can be pulled from http://api.gios.gov.pl/pjp-api/rest/station/findAll
"""
from datetime import datetime
from air_pollution_sq9atk import AirPollutionSq9atk
airpollutionsq9atk = AirPollutionSq9atk(
    language=pl_google,
    service_url="http://api.gios.gov.pl/pjp-api/rest/",
    station_id = 402,       # Example -> Kraków, ul. Bulwarowa
)
"""
# --------------------
# geomagnetic_sq9atk
# --------------------
# Polish air geo_magnetic module, full list of stations can be find at https://www.gismeteo.pl
"""
from geo_magnetic_sq9atk import GeoMagneticSq9atk
geomagneticsq9atk = GeoMagneticSq9atk(
    language=pl_google,
    service_url="https://www.gismeteo.pl/weather-krakow-3212/gm/",  # Example -> Kraków
)
"""
# ===============
# Enabled Modules
# ===============
modules = [
    plugin_activitymap,            # marker na mapie wx.ostol.pl
    #openweathersq9atk,      # prognoza pogody
    plugin_openweather,             # prognoza pogody
    #imgwpodestsq9atk,       # wodowskazy
    #airpollutionsq9atk,     # zanieczyszczenia powietrza z GIOŚ
    #airlysq9atk,            # zanieczyszczenia powietrza z Airly
    #vhftroposq9atk,         # vhf tropo propagacja
    #propagationsq9atk,      # propagacja KF
    #geomagneticsq9atk,      # zaburzenia geomagnetyczne
    #radioactivesq9atk,      # promieniowanie jonizujące
    #calendarsq9atk,         # wschód słońca
]
