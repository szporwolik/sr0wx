# -*- coding: utf-8 -*-

"""Language module for PL - Polish language,
   originally created by Michal Sadowski
"""

#
#   Copyright 2009-2014 Michal Sadowski (sq6jnx at hamradio dot pl)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

from six import u
import datetime

import src.lib.pyliczba as pyliczba
from src import lang_scaffold
   
class SR0WXSpecificLanguage(lang_scaffold.SR0WXLanguage):
    isocode = "pl"
    
    def read_number(self, value, units=None, isFraction=None):
        """Converts numbers to text."""
        if units is None:
            retval = pyliczba.lslownie(abs(value))
        else:
            retval = pyliczba.cosslownie(abs(value), units)

        if isFraction:
            if value % 1 == 0 and retval.startswith(u("jeden ")):
                retval = retval.replace(u("jeden "), u("jedna "))
            if value % 2 == 0 and retval.startswith(u("dwa ")):
                retval = retval.replace(u("dwa "), u("dwie "))
            if value % 10 % 2 == 0:
                retval = retval.replace(u("dwa "), u("dwie "))

        if retval.startswith(u("jeden tysiąc")):
            retval = retval.replace(u("jeden tysiąc"), u("tysiąc"))
        if value < 0:
            retval = " ".join(("minus", retval))
        return retval

    def read_pressure(self, value):
        hPa = ["hektopaskal", "hektopaskale", "hektopaskali"]
        return self.read_number(value, hPa)
     
    def read_distance(self, value):
        hPa = ["kilometr", "kilometry", "kilometrow"]
        return self.read_number(value, hPa)
     

    def read_percent(self, value):
        percent = ["procent", "procent", "procent"]
        return self.read_number(value, percent)

    def read_temperature(self, value):
        C = [(u("stopień celsjusza")), ("stopnie celsjusza"), ("stopni celsjusza")]
        return self.read_number(value, C)

    def read_speed(self, no, unit='mps'):
        units = {
            'mps': [
                    (u("metr na sekundę")), 
                    (u("metry na sekundę")),
                    (u("metrów na sekundę"))
                ],
            'kmph': [(u("kilometr na godzinę")), (u("kilometry na godzinę")),(u("kilometrów na godzinę"))]
        }
        return self.read_number(no, units[unit])

    
    def read_degrees(self, value):
        deg = [u("stopień"), u("stopnie"), u("stopni")]
        return self.read_number(value, deg)

    def read_micrograms(self, value):
        deg = [
                u("mikrogram na_metr_szes_cienny"),
                u("mikrogramy na_metr_szes_cienny"), 
                u("mikrogramo_w na_metr_szes_cienny"), 
            ]
        return self.read_number(value, deg)

    def read_decimal(self, value):
        deg1000 = [
                u("tysie_czna"),
                u("tysie_czne"),
                u("tysie_cznych")
            ]
            
        deg100 = [
                u("setna"),
                u("setne"), 
                u("setnych"),
            ]
            
        deg10 = [
                u("dziesia_ta"),
                u("dziesia_te"), 
                u("dziesia_tych"),
            ]

        if (value % 100 == 0 and value >= 100):
            return self.read_number( value / 100, deg10, True)
        elif (value % 10 == 0 and value > 9 ):
            return self.read_number( value / 10, deg100, True)
        else:
            return self.read_number(value, deg1000, True)
    
    def read_direction(self, value, short=False):
        directions = {
            "N": (u("północno"),   u("północny")),
            "E": (u("wschodnio"),  u("wschodni")),
            "W": (u("zachodnio"),  u("zachodni")),
            "S": (u("południowo"), u("południowy")),
        }
        if short:
            value = value[-2:]
        return '-'.join([directions[d][0 if i < 0 else 1]
                         for i, d in enumerate(value, -len(value)+1)])


    def read_datetime(self, value, out_fmt, in_fmt=None):

        if type(value) != datetime.datetime and in_fmt is not None:
            value = datetime.datetime.strptime(value, in_fmt)
        elif type(value) == datetime.datetime:
            pass
        else:
            raise TypeError('Either datetime must be supplied or both '
                            'value and in_fmt')

        MONTHS = [u(""),
                  u("stycznia"), u("lutego"), u("marca"), u("kwietnia"), u("maja"),
                  u("czerwca"), u("lipca"), u("sierpnia"), u("września"),
                  u("października"), u("listopada"), u("grudnia"),
        ]

        DAYS_N0 = [u(""), u(""), u("dwudziestego"), u("trzydziestego"),]
        DAYS_N = [u(""),
                  u("pierwszego"), u("drugiego"), u("trzeciego"), u("czwartego"),
                  u("piątego"), u("szóstego"), u("siódmego"), u("ósmego"),
                  u("dziewiątego"), u("dziesiątego"), u("jedenastego"),
                  u("dwunastego"), u("trzynastego"), u("czternastego"),
                  u("piętnastego"), u("szesnastego"), u("siedemnastego"),
                  u("osiemnastego"), u("dziewiętnastego"),
        ]
        HOURS = [u("zero"), u("pierwsza"), u("druga"), u("trzecia"), u("czwarta"),
                 u("piąta"), u("szósta"), u("siódma"), u("ósma"), u("dziewiąta"),
                 u("dziesiąta"), u("jedenasta"), u("dwunasta"), u("trzynasta"),
                 u("czternasta"), u("piętnasta"), u("szesnasta"),
                 u("siedemnasta"), u("osiemnasta"), u("dziewiętnasta"),
                 u("dwudziesta"),
        ]


        _, tm_mon, tm_mday, tm_hour, tm_min, _, _, _, _ = value.timetuple()
        retval = []
        for word in out_fmt.split(" "):
            if word == '%d':  # Day of the month
                if tm_mday <= 20:
                    retval.append(DAYS_N[tm_mday])
                else:
                    retval.append(DAYS_N0[tm_mday //10])
                    retval.append(DAYS_N[tm_mday % 10])
            elif word == '%B':  # Month as locale’s full name
                retval.append(MONTHS[tm_mon])
            elif word == '%H':  # Hour (24-hour clock) as a decimal number
                if tm_hour <= 20:
                    retval.append(HOURS[tm_hour])
                elif tm_hour > 20:
                    retval.append(HOURS[20])
                    retval.append(HOURS[tm_hour - 20])
            elif word == '%M':  # Minute as a decimal number
                if tm_min == 0:
                    retval.append(u('zero-zero'))
                else:
                    retval.append(self.read_number(tm_min))
            elif word.startswith('%'):
                raise ValueError("Token %s' is not supported!", word)
            else:
                retval.append(word)
        return ' '.join((w for w in retval if w != ''))

    def read_callsign(self, value):
        # literowanie polskie wg. "Krótkofalarstwo i radiokomunikacja - poradnik",
        # Łukasz Komsta SQ8QED, Wydawnictwa Komunikacji i Łączności Warszawa, 2001,
        # str. 130
        LETTERS = {
            'a': u('adam'), 'b': u('barbara'), 'c': u('celina'), 'd': u('dorota'),
            'e': u('edward'), 'f': u('franciszek'), 'g': u('gustaw'),
            'h': u('henryk'), 'i': u('irena'), 'j': u('józef'), 'k': u('karol'),
            'l': u('ludwik'), 'm': u('marek'), 'n': u('natalia'), 'o': u('olga'),
            'p': u('paweł'), 'q': u('quebec'), 'r': u('roman'), 's': u('stefan'),
            't': u('tadeusz'), 'u': u('urszula'), 'v': u('violetta'),
            'w': u('wacław'), 'x': u('xawery'), 'y': u('ypsilon'), 'z': u('zygmunt'),
            '/': u('łamane'),
        }
        retval = []
        for char in value.lower():
            try:
                retval.append(LETTERS[char])
            except KeyError:
                try:
                    retval.append(self.read_number(int(char)))
                except ValueError:
                    raise ValueError("\"%s\" is not a element of callsign", char)
        return ' '.join(retval)
