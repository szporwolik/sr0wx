# -*- coding: utf-8 -*-

"""Helpers definition
"""

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError 

def CheckInternetConnection():
    req = Request("http://google.com")
    try:
        response = urlopen(req)
    except HTTPError as e:
        return False
    except URLError as e:
        return False
    else:
        return True
  