# -*- coding: utf-8 -*-

"""Core module to handle all the plugin initialisation.
"""

import logging, logging.handlers
import config

# Setup proper language class basing on locale from main config file
if config.lang == "pl":
    from src import lang_pl as lang_module
else:
    from src import lang_en as lang_module
language = lang_module.SR0WXSpecificLanguage()
    
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

data_sources_error_msg = ['Data source is not not available']
data_sources_info_msg = ['Prepared basing on']
read_sources_msg = False

plugins=[]

# -------------
# Module - activity_map
# ------------

if hasattr(config,"plugin_activity_map"):
    from src import plugin_activity_map
    plugin_activitymap = plugin_activity_map.ActivityMap(
        service_url="http://wx.ostol.pl/map_requests?base=",
        callsign=config.station_callsign,
        latitude=config.station_latitude,
        longitude=config.station_longitude,
        above_sea_level=config.station_ASL,
        above_ground_level=config.station_ASL,
        station_range=config.station_range,
        additional_info= config.station_additional_info,
        lang=config.lang
    )
    if(config.plugin_activity_map):
        plugins+=[plugin_activitymap]


# ===============
# Global Modules
# ===============

# ---------------
# Module - calendar
# ---------------

if hasattr(config,"plugin_calendar"):
    from src import plugin_calendar
    plugin_calendar = plugin_calendar.Calendar(
        language=language,
        lat = config.station_latitude,
        lon = config.station_longitude,
    )
    if(config.plugin_calendar):
        plugins+=[plugin_calendar]
        
# ---------------
# Module - openweather
# ---------------
if hasattr(config,"plugin_openweather"):
    from src import plugin_openweather
    plugin_openweather = plugin_openweather.OpenWeather(
        language = language,
        api_key = config.plugin_openweather_api_key,
        lat = config.station_latitude,
        lon = config.station_longitude,
        service_url = 'http://api.openweathermap.org/data/2.5/'
    )
    if(config.plugin_openweather):
        plugins+=[plugin_openweather]

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
