# -*- coding: utf-8 -*-

"""Helpers definition
"""

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError 
import os
import config
import gettext

def CheckInternetConnection():
# Checks for internet connection
    req = Request("http://google.com")
    try:
        response = urlopen(req)
    except HTTPError as e:
        return False
    except URLError as e:
        return False
    else:
        return True

def CheckOrCreateDir(dir):
# Check if folder exist, if not - creates one
    if not os.path.exists(dir):
        os.makedirs(dir) 
        
def LogEntryPluginStep(text):
# Formating for status changes of the plugins
    return " > %s" %text

# Setup i18n function
appname = 'sr0wx'
localedir = './locales/'
en_i18n = gettext.translation(appname, localedir, languages=[config.lang])
en_i18n.install()
_ = en_i18n.gettext