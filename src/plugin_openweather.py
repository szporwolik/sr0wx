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
from src import plugin_scaffold

class OpenWeather(plugin_scaffold.SR0WXModule):
    """Klasa pobierająca dane o promieniowaniu"""

    def __init__(self, language, api_key, lat, lon, service_url):

        self.__service_url = service_url
        self.__lat = lat
        self.__lon = lon
        self.__api_key = api_key   
        self.__language = language
        self.__logger = logging.getLogger(__name__)

        self.events = {
            200: 'burza z lekkimi opadami deszczu', # thunderstorm with light rain
            201: 'burza z opadami deszczu',           # thunderstorm with rain
            202: 'burza z silnymi opadami deszczu', # thunderstorm with heavy rain
            210: 'niewielka burza',                 # light thunderstorm
            211: 'burza',                           # thunderstorm
            212: 'silna burza',                     # heavy thunderstorm
            221: 'przelotna burza',                 # ragged thunderstorm
            230: 'burza z lekką mżawką',            # thunderstorm with light drizzle
            231: 'burza z mżawką',                  # thunderstorm with drizzle
            232: 'burza z silną mżawką',            # thunderstorm with heavy drizzle

            300: 'lekka mżawka',                 # light intensity drizzle
            301: 'mżawka',                       # drizzle
            302: 'silna mżawka',                 # heavy intensity drizzle
            310: 'lekki mżący deszcz',           # light intensity drizzle rain
            311: 'mżący deszcz',                 # drizzle rain
            312: 'silny mżący deszcz',           # heavy intensity drizzle rain
            313: 'ulewa z mżawką',               # shower rain and drizzle
            314: 'silna ulewa z mżawką',         # heavy shower rain and drizzle
            321: 'ulewa z mżawką',               # shower drizzle

            500: 'lekkie opady deszczu',             # light rain     10d
            501: 'umiarkowane opady deszczu ',       # moderate rain     10d
            502: 'intensywne opady deszczu',         # heavy intensity rain     10d
            503: 'bardzo intensywne opady deszczu',  # very heavy rain     10d
            504: 'oberwanie chmury',                 # extreme rain     10d
            511: 'marznacy deszcz',                  # freezing rain 
            520: 'lekka ulewa',                      # light intensity shower rain     09d
            521: 'ulewa',                            # shower rain     09d
            522: 'silna ulewa',                      # heavy intensity shower rain     09d
            531: 'przelotna ulewa',                  # ragged shower rain     09d

            600: 'niewielkie opady śniegu',      #light snow 
            601: 'opady śniegu',                 #snow 
            602: 'intensywne opady śniegu',      #heavy snow 
            611: 'śnieg z deszczem',             #sleet 
            612: 'śnieg z deszczem',             #shower sleet 
            615: 'śnieg z niewielkim deszczem',  #light rain and snow 
            616: 'śnieg z deszczem',             #rain and snow 
            620: 'lekka śnieżyca',               #light shower snow 
            621: 'śnieżyca',                     #showersnow 
            622: 'intensywna śnieżyca',          #heavy shower snow  

            701: 'zamglenia',           # mist     
            711: 'zadymienie',          # smoke     
            721: 'mgła',                # haze     
            731: 'kurz i piach',        # sand, dust whirls     
            741: 'mgła',                # fog     
            751: 'piasek',              # sand     
            761: 'pył',                 # dust     
            762: 'pył wulkaniczny',     # volcanic ash     
            771: 'szkwały',             # squalls     
            781: 'tornado',             # tornado     

            800: 'bezchmurnie',
            801: 'lekkie zachmurzenie', 
            802: 'niewielkie zachmurzenie', 
            803: 'zachmurzenie umiarkowane', 
            804: 'pochmurno'
        }

    def downloadFile(self, url):
        try:
            page = urllib.request.urlopen(url)
            return page.read()
        except urllib.error.HTTPError as e:
            print(e)
        return ""

    def getHour(self):
        time =  ":".join([str(datetime.now().hour), str(datetime.now().minute)])
        datetime_object = datetime.strptime(time, '%H:%M')
        time_words = self.__language.read_datetime(datetime_object, '%H %M')
        return time_words

    def getWeather(self, json):    
        message = '';
        for row in json:
            if row['id'] in self.events:
                message += '' + self.events[row['id']] + '.'
        return message

    def getClouds(self, json):
        msg = '';
        if json['all'] > 0:
            msg += 'pokrywa chmur ' + self.__language.read_percent( int(json['all']) )
        return msg

    def getMainConditions(self, json):
        msg = ''
        msg += '' + self.__language.read_temperature( int(json['temp']) ) + '.'
        return msg

    def getVisibility(self, json):
        msg = '';
        msg += 'widoczność' + self.__language.read_distance( int(json/1000) )
        return msg

    def getWind(self, json):
        msg = '';
        
        if 'deg' in json and int(json['speed']) > 5:
            if 0 <= json['deg'] < 23:  msg += 'północny'
            if 23 <= json['deg'] < 67:  msg += 'północno wschodni'
            if 67 <= json['deg'] < 112:  msg += ' wschodni '
            if 112 <= json['deg'] < 157:  msg += 'południowo wschodni'
            if 157 <= json['deg'] < 202:  msg += 'południowy'
            if 202 <= json['deg'] < 247:  msg += 'południowo zachodni'
            if 247 <= json['deg'] < 292:  msg += 'zachodni'
            if 292 <= json['deg'] < 337:  msg += 'północno zachodni'
            if 337 <= json['deg'] < 360:  msg += 'północny'
        msg += '.'
        
        if 'speed' in json:
            if 0 <= int(json['speed']) < 1:  msg += 'brak wiatru'
            if 1 <= int(json['speed']) < 5:  msg += 'lekkie powiewy wiatru'
            if 5 <= int(json['speed']) < 11:  msg += 'słaby wiatr'
            if 11 <= int(json['speed']) < 19:  msg += 'łagodny wiatr'
            if 19 <= int(json['speed']) < 28:  msg += 'umiarkowany wiatr'
            if 28 <= int(json['speed']) < 38:  msg += 'dość silny wiatr'
            if 38 <= int(json['speed']) < 49:  msg += 'silny wiatr'
            if 49 <= int(json['speed']) < 61:  msg += 'bardzo silny wiatr'
            if 61 <= int(json['speed']) < 74:  msg += 'sztorm'
            if 74 <= int(json['speed']) < 88:  msg += 'silny sztorm'
            if 88 <= int(json['speed']) < 102:  msg += 'bardzo silny sztorm'
            if 102 <= int(json['speed']) < 117:  msg += 'gwałtowny sztorm'
            if 117 <= int(json['speed']):  msg += 'huragan'
            
        msg += '.'
        #msg += '' + self.__language.read_speed( int(json['speed']/1000*3600),'kmph')
        #msg += '.'
        return msg

    def get_data(self):
        
        self.__logger.info("::: Getting actual weather...")
        
        weather_service_url = self.__service_url + 'weather?lat=' + str(self.__lat) + '&lon='+str(self.__lon) + '&units=metric&appid=' + self.__api_key
        self.__logger.info( weather_service_url )
        weatherJson = JSON.loads( self.downloadFile(weather_service_url) )

        self.__logger.info("::: Getting forecast...")
        
        forecast_service_url = self.__service_url + 'forecast?lat=' + str(self.__lat) + '&lon='+str(self.__lon) + '&units=metric&appid=' + self.__api_key
        self.__logger.info( forecast_service_url )
        forecastJsonAll = JSON.loads( self.downloadFile(forecast_service_url) )

        self.__logger.info("::: Processing data...")

        message = "".join([ "Aktualna pogoda.", 
                        self.getWeather( weatherJson['weather'] ), \
                        self.getMainConditions( weatherJson['main'] ), \
                        self.getWind( weatherJson['wind'] ), \
                     ])

        forecastJson = forecastJsonAll['list'][1]
        message += "".join([ \
                        "Prognoza na kolejne cztery godziny..", 
                        self.getWeather( forecastJson['weather'] ), \
                        self.getMainConditions( forecastJson['main'] ), \
                        self.getWind( forecastJson['wind'] ), \
                     ])
        
        forecastJson = forecastJsonAll['list'][4]
        message += "".join([ \
                        "Prognoza na kolejne dwanaście godzin.", 
                        self.getWeather( forecastJson['weather'] ), \
                        self.getMainConditions( forecastJson['main'] ), \
                        self.getWind( forecastJson['wind'] ), \
                     ])

        self.__logger.info("::: Data prepared\n")
                
        return {
            "message": message,
            "source": "open weather map",
        }
