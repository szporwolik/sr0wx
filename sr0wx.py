#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is main program file for automatic weather station project;
   codename SR0WX. Refer README.md for more information and manual.
"""

import os
import pygame
import asyncio
import sys

# Try to import main config file
try:
    import config
except ImportError:
    print('\nsr0wx error: config.py configuration file does not exist, please read README.md\n')
    sys.exit(0)

# Load rest of our modules
from src import module_helpers,module_soundsamples, module_init, module_logger, module_constants, module_helpers

# Global variables definition
helper_test = False                             # Used for development
plugins_list = module_init.plugins              # List of moddules to be executed
plugin_sources = []                             # List of data sources
sr0wx_message = ""                              # All datas returned by SR0WX modules will be stored in ``message`` variable.

# Handle arguments
n = len(sys.argv)
for i in range(0, n):
    if sys.argv[i]=='t':
        helper_test = True

# Create file/folder structure
module_helpers.CheckOrCreateDir("logs")
module_helpers.CheckOrCreateDir("cache")

# Initialize root logger
logger = module_logger.setup_logging(module_init) 

# Display welcome information to the user
logger.info(module_logger.text_color(module_constants.COLOR_BLUE,"sr0wx.py " +_("has started")))
logger.info(module_logger.text_color(module_constants.COLOR_PURPLE,module_constants.LICENSE))

# Handle no internet situation
if module_helpers.CheckInternetConnection() != True:
    plugins_list = []
    logger.info(module_logger.text_color(module_constants.COLOR_RED, _("No internet connection")))

# Execute modules    
for plugin in plugins_list:
    try:
        logger.info(module_logger.text_color(module_constants.COLOR_BLUE, _("Starting plugin: %s")),plugin)
        plugin.get_data()
        
        sr0wx_message = "".join((sr0wx_message, plugin.message))
        
        if plugin.message != "" and plugin.source != "":
            plugin_sources.append(plugin.source)
    except:
        logger.exception(module_logger.text_color(module_constants.COLOR_RED,_("Exception occured when running plugin")))

# When all the modules finished its' work it's time to split the received messages to sentences
sr0wx_message = [config.message_welcome] + sr0wx_message.split(sep=".") 

# Depending on the config, build data sources list to be read
if hasattr(module_init, 'read_sources_msg'):
    if module_init.read_sources_msg:
        if len(plugin_sources) >= 1:
            sr0wx_message += module_init.data_sources_info_msg
            sr0wx_message += plugin_sources
    
sr0wx_message += [config.message_goodbye]
sr0wx_message += [module_init.language.read_callsign(config.station_callsign)]

# Prepare sound samples - generate missing ones
logger.info(module_logger.text_color(module_constants.COLOR_BLUE,_("Message to be transmitted:")))
for el in sr0wx_message:
    logger.info("|"+el+"|")

# Handle cache clearing, this shall prevent indefinity storage expansion
logger.info(module_logger.text_color(module_constants.COLOR_BLUE,_("Clearing cache")))
module_soundsamples.SoundSampleClearCache(logger,os.path.join('cache'),config.cache_max_age)

# Start ``pygame``'s mixer (and ``pygame``), define sound quality (44kHz 16bit, stereo)
pygame.mixer.init(44000, -16, 2, 1024) 

# Prepare sound samples - generate missing ones
logger.info(module_logger.text_color(module_constants.COLOR_BLUE,_("Preparing sound samples")))
for el in sr0wx_message:
    if el != '' and el != ' ':
        asyncio.get_event_loop().run_until_complete(module_soundsamples.SoundSampleGenerate(logger,el, module_init.language.isocode))

# Load all required samples into memory
logger.info(module_logger.text_color(module_constants.COLOR_BLUE,_("Preloading sound samples")))

sound_samples = {}
for el in sr0wx_message:
    if el != '' and el != ' ' and el != "_":
        if not os.path.isfile('cache' + "/" + module_soundsamples.SoundSampleGetFilename(el,module_init.language.isocode)):
            logger.warning(module_constants.COLOR_RED + _("Couldn't find %s") % ('cache' + "/" + module_soundsamples.SoundSampleGetFilename(el,module_init.language.isocode) + module_constants.COLOR_ENDC))
            sound_samples[el] = pygame.mixer.Sound('sounds' + "/beep.ogg")
        else:
            sound_samples[el] = pygame.mixer.Sound('cache' + "/" + module_soundsamples.SoundSampleGetFilename(el,module_init.language.isocode))

# Setting PTT via serial port
ser = None
if config.serial_port != None and config.serial_port != '':
    logger.info(module_logger.text_color(module_constants.COLOR_BLUE,_("PTT control started")))
    import serial
    try:
        ser = serial.Serial(config.serial_port, config.serial_baud_rate)
        if config.serial_signal == 'DTR':
            logger.info(module_logger.text_color(module_constants.COLOR_GREEN,_("DTR/PTT set to ON")))
            ser.setDTR(1)
            ser.setRTS(0)
        else:
            logger.info(module_logger.text_color(module_constants.COLOR_GREEN ,_("RTS/PTT set to ON")))
            ser.setDTR(0)
            ser.setRTS(1)
    except:
        log = module_constants.COLOR_RED + _("Failed to open serial port %s@%i") + module_constants.COLOR_ENDC
        logger.error(log, config.serial_port, config.serial_baud_rate)
    
    pygame.time.delay(1000) # Ensure PTT is enabled and TRX is transmitting
else:
    logger.info(module_logger.text_color(module_constants.COLOR_YELLOW,_("Serial port was not configured, PTT control is disabled")))
    
# Playback
if not helper_test:
    logger.info(module_logger.text_color(module_constants.COLOR_BLUE,_("Transmitting")))
    for el in sr0wx_message:
        if el == "_" or el == " " or el == "":
            pygame.time.wait(500) # Pause on underline or empty letter or empty element
        else:
            voice_channel = sound_samples[el].play()
            
            while voice_channel.get_busy():
                pygame.time.Clock().tick(25)  # This defines how owthen we check if the playback is completed, higher value will reduce delays, but also increase CPU usage
else:
    logger.info(module_logger.text_color(module_constants.COLOR_BLUE,_("Test Mode is enabled - transmitting was skipped")))

# Pause to ensure playback is completed and everything is transmitted before closing transimission
pygame.time.delay(1000)

# Clean up
logger.info(module_logger.text_color(module_constants.COLOR_BLUE,_("Cleaning up and finishig execution")))

# If we've opened serial it's now time to close it.
try:
    if config.serial_port != None and config.serial_port != '':
        if ser != None:
            ser.close()
            logger.info(module_logger.text_color(module_constants.COLOR_GREEN ,_("RTS/DTR set to OFF")))
except NameError:
    logger.exception(module_logger.text_color(module_constants.COLOR_RED , _("Couldn't close serial port" )))

logger.info(module_logger.text_color(module_constants.COLOR_BLUE , _("sr0wx.py has finished execution")))

