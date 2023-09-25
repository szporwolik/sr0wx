# -*- coding: utf-8 -*-

"""This is language scaffold module. All languages 
   Shall derivate from this class.
"""
import inflect

p = inflect.engine()

class SR0WXLanguage(object):
    isocode = "xx"
    
    def __init__(self):
        """Nothing here for now."""
        pass
    
    def read_number(self, value, units=None, isFraction=None):
        if units != None:
            return p.number_to_words(value) +" "+p.plural(units, value)
        else:
            return p.number_to_words(value)
    
    def read_pressure(self, value):
        return self.read_number(value, "hectopascal")
     
    def read_distance(self, value):
        return self.read_number(value, "kilometer")
     
    def read_percent(self, value):
        return self.read_number(value, "percent")
    
    def read_temperature(self, value):
        return self.read_number(value, "degree Celsius")
