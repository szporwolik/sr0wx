# SR0WX configuration file

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

# Station configuration
hello_msg = 'Tutaj stacja pogodowa SR0WX'                                   # Text: Welcome message, played at the begining of transmission - ensure to keep your callsign in
goodbye_msg = 'Tutaj Stefan Roman Zero Wanda Ksawery'                       # Text: Closing message, played at the begining of transmission - ensure to keep your callsign in
callsign = "SR0WX"                                                          # Text: Station callsign
latitude=54.655245,                                                         # Number: Latitude coordinate of the station 
longitude=19.268097,                                                        # Number: Longitude coordinate of the station 
above_ground_level=20,                                                      # Number: AGL heigh in meters
station_range=65,                                                           # Number: Station range in kilometers
additional_info= "Automatyczna stacja pogodowa",                            # Text: Additional description to be send to the clusters, please KEEP IT SHORT

# ===============
# Module configuration
# ===============