# -*- coding: utf-8 -*-

"""Module to handle the sound samples in the cache directory.
"""

from aiogtts import aiogTTS
import re
import os
import os, time

def SoundSampleClearCache(logger,path,age):
    now = time.time()

    for filename in os.listdir(path):
        if os.path.getmtime(os.path.join(path, filename)) < now - age * 3600:
            if os.path.isfile(os.path.join(path, filename)):
                logger.info("Deleting old sound sample: " + filename )
                os.remove(os.path.join(path, filename))

def SoundSampleGetFilename(text: str,lang_isocode):
    text = text.lower()
    return lang_isocode + '_' + re.sub(r'[^A-Za-z0-9]+', '', text) + ".mp3"
    
async def SoundSampleGenerate(logger,text,lang_isocode):
    aiogtts=None
    if text == "_":
        return None
    
    if not os.path.isfile(os.path.join('cache', SoundSampleGetFilename(text,lang_isocode))):
        aiogtts = aiogTTS()
        await aiogtts.save(text,os.path.join('cache', SoundSampleGetFilename(text,lang_isocode) ), lang_isocode)