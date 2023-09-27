#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is main program file for automatic weather station project;
   codename SR0WX. Refer README.md for more information and manual.
"""

import os
import pygame
import asyncio
import gettext
import sys

try:
    import config
except ImportError:
    print('\nsr0wx error: config.py configuration file does not exist, please read README.md\n')
    sys.exit(0)

from src import module_soundsamples, module_init, module_logger, module_constants, module_helpers

# Set up Gettext
en_i18n = gettext.translation(module_init.appname, module_init.localedir, fallback=False)
en_i18n.install()
_ = en_i18n.gettext

plugins_list = module_init.plugins              # List of moddules to be executed
plugin_sources = []                             # List of data sources
sr0wx_message = ""                              # All datas returned by SR0WX modules will be stored in ``message`` variable.

# Create file/folder structure
module_helpers.CheckOrCreateDir("logs")
module_helpers.CheckOrCreateDir("cache")

# Initialize root logger
logger = module_logger.setup_logging(module_init) 

# Display welcome information to the user
logger.info(module_logger.text_color(module_constants.COLOR_WARNING,"sr0wx.py " +_("has started")))
logger.info(module_logger.text_color(module_constants.COLOR_OKBLUE,module_constants.LICENSE))

# Handle no internet situation
if module_helpers.CheckInternetConnection() != True:
    plugins_list = []
    logger.info(module_logger.text_color(module_constants.COLOR_FAIL, _("No internet connection")))

# Execute modules    
for plugin in plugins_list:
    try:
        logger.info(module_logger.text_color(module_constants.COLOR_OKGREEN, _("Starting plugin: %s")),plugin)
        plugin.get_data()
        
        sr0wx_message = "".join((sr0wx_message, plugin.message))
        
        if plugin.message != "" and plugin.source != "":
            plugin_sources.append(plugin.source)
    except:
        logger.exception(module_logger.text_color(module_constants.COLOR_FAIL,_("Exception occured when running plugin")))

# When all the modules finished its' work it's time to split the received messages to sentences
sr0wx_message = [config.message_welcome] + sr0wx_message.split(sep=".") 

# Depending on the config, build data sources list to be read
if hasattr(module_init, 'read_sources_msg'):
    if module_init.read_sources_msg:
        if len(plugin_sources) >= 1:
            sr0wx_message += module_init.data_sources_info_msg
            sr0wx_message += plugin_sources
    
sr0wx_message += [config.message_goodbye]

# Prepare sound samples - generate missing ones
logger.info(module_logger.text_color(module_constants.COLOR_OKGREEN,_("Message to be transmitted:")))
for el in sr0wx_message:
    logger.info("|"+el+"|")

# Handle cache clearing, this shall prevent indefinity storage expansion
logger.info(module_logger.text_color(module_constants.COLOR_OKGREEN,_("Clearing cache")))
module_soundsamples.SoundSampleClearCache(logger,os.path.join('cache'),config.cache_max_age)

# Start ``pygame``'s mixer (and ``pygame``), define sound quality (44kHz 16bit, stereo)
pygame.mixer.init(44000, -16, 2, 1024) 

# Prepare sound samples - generate missing ones
logger.info(module_logger.text_color(module_constants.COLOR_OKGREEN,_("Preparing sound samples")))
for el in sr0wx_message:
    if el != '' and el != ' ':
        asyncio.get_event_loop().run_until_complete(module_soundsamples.SoundSampleGenerate(logger,el, module_init.language.isocode))

# Load all required samples into memory
logger.info(module_logger.text_color(module_constants.COLOR_OKGREEN,_("Preloading sound samples")))

sound_samples = {}
for el in sr0wx_message:
    if el != '' and el != ' ' and el != "_":
        if not os.path.isfile('cache' + "/" + module_soundsamples.SoundSampleGetFilename(el,module_init.language.isocode)):
            logger.warning(module_constants.COLOR_FAIL + _("Couldn't find %s") % ('cache' + "/" + module_soundsamples.SoundSampleGetFilename(el,module_init.language.isocode) + module_constants.COLOR_ENDC))
            sound_samples[el] = pygame.mixer.Sound('sounds' + "/beep.ogg")
        else:
            sound_samples[el] = pygame.mixer.Sound('cache' + "/" + module_soundsamples.SoundSampleGetFilename(el,module_init.language.isocode))

# Setting PTT via serial port
logger.info(module_logger.text_color(module_constants.COLOR_OKGREEN,_("PTT control started")))
ser = None
if config.serial_port is not None:
    import serial
    try:
        ser = serial.Serial(config.serial_port, config.serial_baud_rate)
        if config.serial_signal == 'DTR':
            logger.info(module_logger.text_color(module_constants.COLOR_OKGREEN,_("DTR/PTT set to ON")))
            ser.setDTR(1)
            ser.setRTS(0)
        else:
            logger.info(module_logger.text_color(module_constants.COLOR_OKGREEN ,_("RTS/PTT set to ON")))
            ser.setDTR(0)
            ser.setRTS(1)
    except:
        log = module_constants.COLOR_FAIL + _("Failed to open serial port %s@%i") + module_constants.COLOR_ENDC
        logger.error(log, config.serial_port, config.serial_baud_rate)
    
    pygame.time.delay(1000) # Ensure PTT is enabled and TRX is transmitting

# Playback
logger.info(module_logger.text_color(module_constants.COLOR_OKGREEN,_("Transmitting")))
for el in sr0wx_message:
    if el == "_" or el == " " or el == "":
        pygame.time.wait(500) # Pause on underline or empty letter or empty element
    else:
        voice_channel = sound_samples[el].play()
         
        while voice_channel.get_busy():
            pygame.time.Clock().tick(25)  # This defines how owthen we check if the playback is completed, higher value will reduce delays, but also increase CPU usage

# Pause to ensure playback is completed and everything is transmitted before closing transimission
pygame.time.delay(1000)

# Clean up
logger.info(module_logger.text_color(module_constants.COLOR_WARNING,_("Finishing...")))

# If we've opened serial it's now time to close it.
try:
    if config.serial_port is not None:
        if ser != None:
            ser.close()
            logger.info(module_logger.text_color(module_constants.COLOR_OKGREEN ,_("RTS/DTR set to OFF")))
except NameError:
    logger.exception(module_logger.text_color(module_constants.COLOR_FAIL , _("Couldn't close serial port" )))

logger.info(module_logger.text_color(module_constants.COLOR_WARNING , _("sr0wx.py has finished execution")))

