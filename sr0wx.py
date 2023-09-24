#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is main program file for automatic weather station project;
   codename SR0WX. Refer README.md for more information and manual.
"""

import getopt
import os
import pygame
import sys
import logging, logging.handlers
import numpy
import urllib.request
import urllib.error
import asyncio
from src import module_soundsamples, module_init
import config


logger = None

# Logging configuration
def setup_logging(config):
    # create formatter and add it to the handlers
    formatter = logging.Formatter(config.log_line_format)

    # Creating logger with the lowest log level in config handlers
    min_log_level = min([h['log_level'] for h in config.log_handlers])
    logger = logging.getLogger()
    logger.setLevel(min_log_level)

    # create logging handlers according to its definitions
    for handler_definition in config.log_handlers:
        handler = handler_definition['class'](**handler_definition['config'])
        handler.setLevel(handler_definition['log_level'])
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod
        
#
# All datas returned by SR0WX modules will be stored in ``data`` variable.

message = ""

# Information about which modules are to be executed is written in SR0WX
# config file. Program starts every single of them and appends it's return
# value in ``data`` variable. As you can see every module is started with
# language variable, which is also defined in configuration.
# Refer configuration and internationalization manuals for further
# informations.
#
# Modules may be also given in commandline, separated by a comma.

module_init.config = None
try:
    opts, args = getopt.getopt(sys.argv[1:], "c:", ["config="])
except getopt.GetoptError:
    pass
for opt, arg in opts:
    if opt in ("-c", "--config"):
        if arg[-3:] == '.py':
            arg = arg[:-3]
        src.config = __import__(arg)

if module_init.config is None:
    import src.module_init as module_init

logger = setup_logging(module_init)

logger.info(module_init.COLOR_WARNING + "sr0wx.py has started it's execution" + module_init.COLOR_ENDC)
logger.info(module_init.LICENSE)


if len(args) > 0:
    modules = args[0].split(",")
else:
    modules = module_init.modules

try:
    dane = urllib.request.urlopen('http://google.pl')
except urllib.error.HTTPError as e:
    modules = []
    message += " ".join(module_init.data_sources_error_msg)
    logger.info(module_init.COLOR_FAIL + "No internet connection" + module_init.COLOR_ENDC + "\n")

#lang = my_import('.'.join((config.lang, config.lang)))
sources = []

for module in modules:
    try:
        logger.info(module_init.COLOR_OKGREEN + "starting %s..." + module_init.COLOR_ENDC, module)
        module_data = module.get_data()
        module_message = module_data.get("message", "")
        module_source = module_data.get("source", "")

        message = "".join((message, module_message))
        if module_message != "" and module_source != "":
            sources.append(module_data['source'])
    except:
        logger.exception(module_init.COLOR_FAIL + "Exception when running %s"+ module_init.COLOR_ENDC, module)

# When all the modules finished its' work it's time to ``.split()`` returned
# data. Every element of returned list is actually a filename of a sample.

message = [config.message_welcome] + message.split(sep=".")

if hasattr(module_init, 'read_sources_msg'):
    if module_init.read_sources_msg:
        if len(sources) > 1:
            message += sources
else:
    message += sources
message += [config.message_goodbye]

# It's time to init ``pygame``'s mixer (and ``pygame``). Possibly defined
# sound quality is far-too-good (44kHz 16bit, stereo), so you can change it.

pygame.mixer.init(16000, -16, 2, 1024)

# Next (as a tiny timesaver & memory eater ;) program loads all necessary
# samples into memory. I think that this is better approach than reading
# every single sample from disk in the same moment when it's time to play it.

# Just for debug: our playlist (whole message as a list of filenames)

playlist = []

logger.info(module_init.COLOR_OKGREEN + "Clearing cache" + module_init.COLOR_ENDC)
module_soundsamples.SoundSampleClearCache(logger,os.path.join('cache'),config.cache_max_age)

logger.info(module_init.COLOR_OKGREEN + "Preparing sound samples" + module_init.COLOR_ENDC)
for el in message:
    if el != '' and el != ' ':
        asyncio.get_event_loop().run_until_complete(module_soundsamples.SoundSampleGenerate(logger,el, module_init.lang))
    
        if "upper" in dir(el):
            playlist.append(el)
        else:
            playlist.append("[sndarray]")

if hasattr(module_init, 'ctcss_tone'):
    volume = 25000
    arr = numpy.array([volume * numpy.sin(2.0 * numpy.pi * round(module_init.ctcss_tone) * x / 16000) for x in range(0, 16000)]).astype(numpy.int16)
    arr2 = numpy.c_[arr,arr]
    #ctcss = pygame.sndarray.make_sound(arr2)
    logger.info(module_init.COLOR_WARNING + "CTCSS tone %sHz" + module_init.COLOR_ENDC, "%.1f" % module_init.ctcss_tone)
    #ctcss.play(-1)

logger.info(module_init.COLOR_OKGREEN + "Preloading sound samples" + module_init.COLOR_ENDC)

sound_samples = {}
for el in message:
    if el != '' and el != ' ':
        if "upper" in dir(el):
            if el[0:7] == 'file://':
                sound_samples[el] = pygame.mixer.Sound(el[7:])

            if el != "_" and el not in sound_samples:
                if not os.path.isfile('cache' + "/" + module_soundsamples.SoundSampleGetFilename(el,module_init.lang)):
                    logger.warning(module_init.COLOR_FAIL + "Couldn't find %s" % ('cache' + "/" + module_soundsamples.SoundSampleGetFilename(el,module_init.lang) + module_init.COLOR_ENDC))
                    sound_samples[el] = pygame.mixer.Sound('sounds' + "/beep.ogg")
                else:
                    sound_samples[el] = pygame.mixer.Sound('cache' + "/" + module_soundsamples.SoundSampleGetFilename(el,module_init.lang))


# Program should be able to "press PTT" via RSS232. See ``config`` for
# details.
ser = None
if config.serial_port is not None:
    
    import serial
    try:
        ser = serial.Serial(config.serial_port, config.serial_baud_rate)
        if config.serial_signal == 'DTR':
            logger.info(module_init.COLOR_OKGREEN + "DTR/PTT set to ON\n" + module_init.COLOR_ENDC)
            ser.setDTR(1)
            ser.setRTS(0)
        else:
            logger.info(module_init.COLOR_OKGREEN + "RTS/PTT set to ON\n" + module_init.COLOR_ENDC)
            ser.setDTR(0)
            ser.setRTS(1)
    except:
        log = module_init.COLOR_FAIL + "Failed to open serial port %s@%i" + module_init.COLOR_ENDC
        logger.error(log, config.serial_port, config.serial_baud_rate)


pygame.time.delay(1000)

# OK, data prepared, samples loaded, let the party begin!
#
# Take a look at ``while`` condition -- program doesn't check if the
# sound had finished played all the time, but only 25 times/sec (default).
# It is because I don't want 100% CPU usage. If you don't have as fast CPU
# as mine (I think you have, though) you can always lower this value.
# Unfortunately, there may be some pauses between samples so "reading
# aloud" will be less natural.

logger.info(module_init.COLOR_OKGREEN + "Playing and transmitting" + module_init.COLOR_ENDC)
for el in message:
    if el == "_":
        pygame.time.wait(500)
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
            pygame.time.Clock().tick(25)

# Possibly the argument of ``pygame.time.Clock().tick()`` should be in
# config file...
#
# The following four lines give us a one second break (for CTCSS, PTT and
# other stuff) before closing the ``pygame`` mixer and display some debug
# informations.

logger.info(module_init.COLOR_WARNING + "Finishing..." + module_init.COLOR_ENDC)

pygame.time.delay(1000)

# If we've opened serial it's now time to close it.
try:
    if config.serial_port is not None:
        if ser != None:
            ser.close()
            logger.info(module_init.COLOR_OKGREEN + "RTS/PTT set to OFF\n" + module_init.COLOR_ENDC)
except NameError:
    logger.exception(module_init.COLOR_FAIL + "Couldn't close serial port" + module_init.COLOR_ENDC)

logger.info(module_init.COLOR_WARNING + "sr0wx.py has finished execution. Bye!" + module_init.COLOR_ENDC)

