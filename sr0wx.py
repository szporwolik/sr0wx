#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is main program file for automatic weather station project;
   codename SR0WX. Refer README.md for more information and manual.
"""

import os
import pygame
import logging, logging.handlers
import numpy
import asyncio

from src import module_soundsamples, module_init, module_logger, module_constants, module_helpers
import config

message = ""   # All datas returned by SR0WX modules will be stored in ``message`` variable.
sources = []

modules = module_init.modules # List of moddules to be executed
logger = module_logger.setup_logging(module_init) # Initialize root logger

logger.info(module_logger.text_color(module_constants.COLOR_WARNING,"sr0wx.py has started it's execution"))
logger.info(module_logger.text_color(module_constants.COLOR_OKBLUE,module_constants.LICENSE))

# Handle no internet situation
if module_helpers.CheckInternetConnection() != True:
    modules = []
    logger.info(module_logger.text_color(module_constants.COLOR_FAIL, "No internet connection"))

# Execute modules    
for module in modules:
    try:
        logger.info(module_constants.COLOR_OKGREEN + "starting %s..." + module_constants.COLOR_ENDC, module)
        module_data = module.get_data()
        module_message = module_data.get("message", "")
        module_source = module_data.get("source", "")

        message = "".join((message, module_message))
        if module_message != "" and module_source != "":
            sources.append(module_data['source'])
    except:
        logger.exception(module_logger.text_color(module_constants.COLOR_FAIL,"Exception when running " +module))

# When all the modules finished its' work it's time to ``.split()`` returned
# data. We split the message by comas, every sentence shall be a seperate
# sound sample

message = [config.message_welcome] + message.split(sep=".") 

# Depending on the config, we may want to list all the sources 
if hasattr(module_init, 'read_sources_msg'):
    if module_init.read_sources_msg:
        if len(sources) >= 1:
            message += module_init.data_sources_info_msg
            message += sources
else:
    message += sources
    
message += [config.message_goodbye]

# Handle cache clering, this shall prevent indefinity storage expansion
logger.info(module_logger.text_color(module_constants.COLOR_OKGREEN,"Clearing cache"))
module_soundsamples.SoundSampleClearCache(logger,os.path.join('cache'),config.cache_max_age)

# Start ``pygame``'s mixer (and ``pygame``) and define sound quality (44kHz 16bit, stereo)
pygame.mixer.init(16000, -16, 2, 1024) 

# Prepare sound samples - generate missing ones
logger.info(module_logger.text_color(module_constants.COLOR_OKGREEN,"Preparing sound samples"))
for el in message:
    if el != '' and el != ' ':
        asyncio.get_event_loop().run_until_complete(module_soundsamples.SoundSampleGenerate(logger,el, module_init.lang))

# Handle CTSS
# TBD
#if hasattr(module_init, 'ctcss_tone'):
    #volume = 25000
    #arr = numpy.array([volume * numpy.sin(2.0 * numpy.pi * round(module_init.ctcss_tone) * x / 16000) for x in range(0, 16000)]).astype(numpy.int16)
    #arr2 = numpy.c_[arr,arr]
    #ctcss = pygame.sndarray.make_sound(arr2) # TBD
    #ctcss.play(-1) TBD
    #logger.info(module_constants.COLOR_WARNING + "CTCSS tone %sHz" + module_constants.COLOR_ENDC, "%.1f" % module_init.ctcss_tone)
    

logger.info(module_logger.text_color(module_constants.COLOR_OKGREEN,"Preloading sound samples"))

# Load all required samples into memory
sound_samples = {}
for el in message:
    if el != '' and el != ' ':
        if "upper" in dir(el):
            if el[0:7] == 'file://':
                sound_samples[el] = pygame.mixer.Sound(el[7:])

            if el != "_" and el not in sound_samples:
                if not os.path.isfile('cache' + "/" + module_soundsamples.SoundSampleGetFilename(el,module_init.lang)):
                    logger.warning(module_constants.COLOR_FAIL + "Couldn't find %s" % ('cache' + "/" + module_soundsamples.SoundSampleGetFilename(el,module_init.lang) + module_constants.COLOR_ENDC))
                    sound_samples[el] = pygame.mixer.Sound('sounds' + "/beep.ogg")
                else:
                    sound_samples[el] = pygame.mixer.Sound('cache' + "/" + module_soundsamples.SoundSampleGetFilename(el,module_init.lang))


# Setting PTT via serial port
ser = None
if config.serial_port is not None:
    import serial
    try:
        ser = serial.Serial(config.serial_port, config.serial_baud_rate)
        if config.serial_signal == 'DTR':
            logger.info(module_logger.text_color(module_constants.COLOR_OKGREEN,"DTR/PTT set to ON" ))
            ser.setDTR(1)
            ser.setRTS(0)
        else:
            logger.info(module_logger.text_color(module_constants.COLOR_OKGREEN ,"RTS/PTT set to ON"  ))
            ser.setDTR(0)
            ser.setRTS(1)
    except:
        log = module_constants.COLOR_FAIL + "Failed to open serial port %s@%i" + module_constants.COLOR_ENDC
        logger.error(log, config.serial_port, config.serial_baud_rate)
    
    pygame.time.delay(1000) # Ensure PTT is enabled and TRX is transmitting

# Playback
logger.info(module_logger.text_color(module_constants.COLOR_OKGREEN,"Transmitting"))
for el in message:
    if el == "_" or el == " ":
        pygame.time.wait(500) # Pause on underline or empty letter
    else:
        if "upper" in dir(el):
            try:
                voice_channel = sound_samples[el].play()
            except:
                a=1

        elif "upper" not in dir(el):
            sound = pygame.sndarray.make_sound(el)
            if module_init.pygame_bug == 1:
                sound = pygame.sndarray.make_sound(pygame.sndarray.array(sound)[:len(pygame.sndarray.array(sound))/2])
            voice_channel = sound.play()
        while voice_channel.get_busy():
            pygame.time.Clock().tick(25)  # This defines how owthen we check if the playback is completed, higher value will reduce delays, but also increase CPU usage

# Pause to ensure playback is completed and everything is transmitted before closing transimission
pygame.time.delay(1000)

# Clean up
logger.info(module_logger.text_color(module_constants.COLOR_WARNING,"Finishing..."))

# If we've opened serial it's now time to close it.
try:
    if config.serial_port is not None:
        if ser != None:
            ser.close()
            logger.info(module_logger.text_color(module_constants.COLOR_OKGREEN ,"RTS/PTT set to OFF\n" ))
except NameError:
    logger.exception(module_logger.text_color(module_constants.COLOR_FAIL , "Couldn't close serial port" ))

logger.info(module_logger.text_color(module_constants.COLOR_WARNING , "sr0wx.py has finished execution. Bye!"))

