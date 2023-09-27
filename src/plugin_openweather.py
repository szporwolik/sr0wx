# -*- coding: utf-8 -*-

"""This is plugin tp get OpenWeather information.
   The code is basind on openweather_sq9atk module
   created by Paweł SQ9ATK.
"""

import urllib.request
import urllib.error
import logging
from datetime import datetime
import json as JSON
from src import plugin_scaffold,module_helpers

class OpenWeather(plugin_scaffold.SR0WXPlugin):
    def __init__(self, language, api_key, lat, lon, service_url):

        self.__service_url = service_url
        self.__lat = lat
        self.__lon = lon
        self.__api_key = api_key   
        self.__language = language
        self.__logger = logging.getLogger(__name__)

    def downloadFile(self, url):
        # Get data from the remote sercer
        try:
            page = urllib.request.urlopen(url)
            return page.read()
        except urllib.error.HTTPError as e:
            print(e)
        return ""
    
        #TBD: Handle erros

    def getHour(self):
        # Get actual time
        time =  ":".join([str(datetime.now().hour), str(datetime.now().minute)])
        datetime_object = datetime.strptime(time, '%H:%M')
        time_words = self.__language.read_datetime(datetime_object, '%H %M')
        return time_words
    
        #TBD: do we really need it here ?

    def getWeather(self, json):
        # Get main weather situation 
        
        # Required for translations
        self.events = {
            200: _('thunderstorm with light rain'),
            201: _('thunderstorm with rain'),
            202: _('thunderstorm with heavy rain'),
            210: _('light thunderstorm'),
            211: _('thunderstorm'),
            212: _('heavy thunderstorm'),
            221: _('ragged thunderstorm'),
            230: _('thunderstorm with light drizzle'),
            231: _('thunderstorm with drizzle'),
            232: _('thunderstorm with heavy drizzle'),

            300: _('light intensity drizzle'),
            301: _('drizzle'),
            302: _('heavy intensity drizzle'),
            310: _('light intensity drizzle rain'),
            311: _('drizzle rain'),
            312: _('heavy intensity drizzle rain'),
            313: _('shower rain and drizzle'),
            314: _('heavy shower rain and drizzle'),
            321: _('shower drizzle'),

            500: _('light rain'),
            501: _('moderate rain'),
            502: _('heavy intensity rain'),
            503: _('very heavy rain'),
            504: _('extreme rain'),
            511: _('freezing rain'),
            520: _('light intensity shower rain'),
            521: _('shower rain'),
            522: _('heavy intensity shower rain'),
            531: _('ragged shower rain'),

            600: _('light snow'),
            601: _('snow'),
            602: _('heavy snow'),
            611: _('sleet'),
            612: _('shower sleet'),
            615: _('light rain and snow'),
            616: _('rain and snow'),
            620: _('light shower snow'),
            621: _('showersnow'),
            622: _('heavy shower snow'),

            701: _('mist'),
            711: _('smoke'),
            721: _('haze'),
            731: _('sand, dust whirls'),
            741: _('fog'),
            751: _('sand'),
            761: _('dust'),
            762: _('volcanic ash'),
            771: _('squalls'),
            781: _('tornado'),

            800: _('clear sky'),
            801: _('few clouds'),
            802: _('scattered clouds'),
            803: _('broken clouds'),
            804: _('overcast clouds')
        }
        # Generate response   
        message = ''
        for row in json:
            if row['id'] in self.events:
                message += '' + self.events[row['id']] + '.'
        return message

    def getClouds(self, json):
        # Get clould coverage
        msg = ''
        if json['all'] > 0:
            msg += _('cloud coverage') + self.__language.read_percent( int(json['all']) )
        return msg

    def getMainConditions(self, json):
        # Get main conditions
        msg = ''
        msg += '' + self.__language.read_temperature( int(json['temp']) ) + '.'
        return msg

    def getVisibility(self, json):
        # Gets visibility
        msg = ''
        msg += _('visibility') + self.__language.read_distance( int(json/1000) )
        return msg

    def getWind(self, json):
        # Gets the wind conditions
        msg = ''
        
        if 'speed' in json:
            if 0 <= int(json['speed']) < 1:  msg += _('no wind')
            if 1 <= int(json['speed']) < 5:  msg += _('light breeze')
            if 5 <= int(json['speed']) < 11:  msg += _('gentle wind')
            if 11 <= int(json['speed']) < 19:  msg += _('moderate wind')
            if 19 <= int(json['speed']) < 28:  msg += _('moderately strong wind')
            if 28 <= int(json['speed']) < 38:  msg += _('quite strong wind')
            if 38 <= int(json['speed']) < 49:  msg += _('strong wind')
            if 49 <= int(json['speed']) < 61:  msg += _('very strong wind')
            if 61 <= int(json['speed']) < 74:  msg += _('storm')
            if 74 <= int(json['speed']) < 88:  msg += _('strong storm')
            if 88 <= int(json['speed']) < 102:  msg += _('very strong storm')
            if 102 <= int(json['speed']) < 117:  msg += _('violent storm')
            if 117 <= int(json['speed']):  msg += _('hurricane')
            
        if 'deg' in json and int(json['speed']) >= 5:
            msg += " %s " % _('from direction')
            if 0 <= json['deg'] < 23:  msg += _('north')
            if 23 <= json['deg'] < 67:  msg += _('northeast')
            if 67 <= json['deg'] < 112:  msg += _('east')
            if 112 <= json['deg'] < 157:  msg += _('southeast')
            if 157 <= json['deg'] < 202:  msg += _('south')
            if 202 <= json['deg'] < 247:  msg += _('southwest')
            if 247 <= json['deg'] < 292:  msg += _('west')
            if 292 <= json['deg'] < 337:  msg += _('northwest')
            if 337 <= json['deg'] < 360:  msg += _('north')
            msg += ' '
            
        msg += '.'
        return msg

    def get_data(self):
        # Pull actual weather information
        self.__logger.info(module_helpers.LogEntryPluginStep(_("Getting actual weather")))
        weather_service_url = self.__service_url + 'weather?lat=' + str(self.__lat) + '&lon='+str(self.__lon) + '&units=metric&appid=' + self.__api_key
        weatherJson = JSON.loads( self.downloadFile(weather_service_url) )
        # TBD: handle connection issues

        # Pull weather forecast
        self.__logger.info(module_helpers.LogEntryPluginStep(_("Getting forecast")))
        forecast_service_url = self.__service_url + 'forecast?lat=' + str(self.__lat) + '&lon='+str(self.__lon) + '&units=metric&appid=' + self.__api_key
        forecastJsonAll = JSON.loads( self.downloadFile(forecast_service_url) )
        # TBD: handle connection issues

        # Data preparation
        self.__logger.info(module_helpers.LogEntryPluginStep(_("Preparing data")))

        # Actual weather
        message = "".join([ _("Actual weather."), 
                        self.getWeather( weatherJson['weather'] ), \
                        self.getMainConditions( weatherJson['main'] ), \
                        self.getWind( weatherJson['wind'] ), \
                     ])

        # 4h forecast
        forecastJson = forecastJsonAll['list'][1]
        message += "".join([ \
                        _("Weather forecast for the next four hours."), 
                        self.getWeather( forecastJson['weather'] ), \
                        self.getMainConditions( forecastJson['main'] ), \
                        self.getWind( forecastJson['wind'] ), \
                     ])
        
        # 12h forecast
        forecastJson = forecastJsonAll['list'][4]
        message += "".join([ \
                        _("Weather forecast for the next twelve hours."), 
                        self.getWeather( forecastJson['weather'] ), \
                        self.getMainConditions( forecastJson['main'] ), \
                        self.getWind( forecastJson['wind'] ), \
                     ])

        
        # Set variables and finish execution
        self.message = message
        self.source = "openweather map"
        
        self.__logger.info(module_helpers.LogEntryPluginStep(_("Data was prepared")))
        