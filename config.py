# -*- coding: utf-8 -*-

"""This is main config file for sr0wx.px.
   Refer README.md for more information and manual.
"""

# ===============
# General Config
# ===============

# Localisation settings
lang = "pl"                                                                 # Text: Station language, PL (Polish) is the ONLY ONE supported for now

# CTSS
ctcss_tone = 88.5                                                           # Number: CTCSS Tone frequency, put number or 0 to disable

# Serial port for PTT
serial_port = '/dev/ttyS0'                                                  # Text: Serial port to be used for PTTY config, set to '' to disable
serial_baud_rate = 9600                                                     # Number: Serial port baud rate
serial_signal = 'DTR'                                                       # Text: PTT serial port signal to be used 'DTR' or 'RTS'

# Cache settings
cache_max_age = 1                                                           # Number: Maximum number of hours after which sound sample shall be regenerated

# Station information
station_callsign = "SR0WX"                                                  # Text: Station callsign
station_latitude=54.655245                                                  # Number: Latitude coordinate of the station 
station_longitude=19.268097                                                 # Number: Longitude coordinate of the station 
station_AGL=20                                                              # Number: AGL - above ground level height in meters
station_ASL = 200                                                           # Number: ASL - above sea level height in meters
station_range=65                                                            # Number: Station range in kilometers
station_additional_info= "Automatyczna stacja pogodowa",                    # Text: Additional description to be send to the clusters (inc. https://ostol.pl/stacja-pogodowa-sr0wx-py), please KEEP IT SHORT

# Messages
message_welcome = 'Tutaj stacja pogodowa SR0WX'                             # Text: Welcome message, played at the begining of transmission - ensure to keep your callsign in
message_goodbye = 'Tutaj Stefan Roman Zero Wanda Ksawery'                   # Text: Closing message, played at the end of transmission - ensure to keep your callsign in

# ===============
# Plugins configuration
# ===============

plugin_activity_map = True                                                  # Bool: Send station information to cluster (inc. https://ostol.pl/stacja-pogodowa-sr0wx-py) if True, this module sends status messages to https://ostol.pl/, strongly recommended to have it active to track the SR0WX community

plugin_openweather = True                                                   # Bool: Enables weather module basing on openweathermap service if True
plugin_openweather_api_key = 'ee78911a0fb560b58144230f46e0d4b2'             # Text: Openweather API key visit https://openweathermap.org/api to get it, all you need is to register (service if FREE)

                          