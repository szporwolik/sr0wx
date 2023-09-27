# -*- coding: utf-8 -*-

"""This is language scaffold module. All languages 
   Shall derivate from this class.
"""
import inflect
import datetime

from src import module_helpers

p = inflect.engine()

class SR0WXLanguage():
    isocode = "xx"
    
    def __init__(self):
        """Nothing here for now."""
        pass
    
    def read_number(self, value, units=None, isFraction=None):
    # Reads number - this is for english only, other languages needs to have own version of this function
        if units != None:
            return p.number_to_words(value) +" "+p.plural(units, value)
        else:
            return p.number_to_words(value)
    
    def read_pressure(self, value):
    # TBD
        return self.read_number(value, "hectopascal")
     
    def read_distance(self, value):
    # TBD
        return self.read_number(value, "kilometer")
     
    def read_percent(self, value):
    # TBD
        return self.read_number(value, "percent")
    
    def read_temperature(self, value):
    # TBD
        return self.read_number(value, "degree Celsius")
    
    def read_datetime(self, value, out_fmt, in_fmt=None):
    # Conerts date and time to text
        _=module_helpers.en_i18n.gettext
        if type(value) != datetime.datetime and in_fmt is not None:
            value = datetime.datetime.strptime(value, in_fmt)
        elif type(value) == datetime.datetime:
            pass
        else:
            raise TypeError('Either datetime must be supplied or both '
                            'value and in_fmt')
        
        MONTHS = ["",
                _("January"), _("February"), _("March"), _("April"), _("May"),
                _("June"), _("July"), _("August"), _("September"),
                _("October"), _("November"), _("December"),
            ]
        DAYS_N0 = ["", "", _("twentieth"), _("thirtieth")]
        DAYS_N = ["",
            _("first"), _("second"), _("third"), _("fourth"),
            _("fifth"), _("sixth"), _("seventh"), _("eighth"),
            _("ninth"), _("tenth"), _("eleventh"),
            _("twelfth"), _("thirteenth"), _("fourteenth"),
            _("fifteenth"), _("sixteenth"), _("seventeenth"),
            _("eighteenth"), _("nineteenth"),
        ]
        HOURS = [_("zero"), _("one"), _("two"), _("three"), _("four"),
            _("five"), _("six"), _("seven"), _("eight"), _("nine"),
            _("ten"), _("eleven"), _("twelve"), _("thirteen"),
            _("fourteen"), _("fifteen"), _("sixteen"), _("seventeen"),
            _("eighteen"), _("nineteen"), _("twenty"),
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
                raise ValueError(_("Token %s' is not supported!"), word)
            else:
                retval.append(word)
        return ' '.join((w for w in retval if w != ''))
    
    def read_callsign(self, value):
    # Reades given callsign - this shall work for all languages
        LETTERS = {
            'a': _('Alpha'), 'b': _('Bravo'), 'c': _('Charlie'), 'd': _('Delta'),
            'e': _('Echo'), 'f': _('Foxtrot'), 'g': _('Golf'),
            'h': _('Hotel'), 'i': _('India'), 'j': _('Juliett'), 'k': _('Kilo'),
            'l': _('Lima'), 'm': _('Mike'), 'n': _('November'), 'o': _('Oscar'),
            'p': _('Papa'), 'q': _('Quebec'), 'r': _('Romeo'), 's': _('Sierra'),
            't': _('Tango'), 'u': _('Uniform'), 'v': _('Victor'),
            'w': _('Whiskey'), 'x': _('X-ray'), 'y': _('Yankee'), 'z': _('Zulu'),
            '/': _('Slash')
        }
        retval = []
        for char in value.lower():
            try:
                retval.append(LETTERS[char])
            except KeyError:
                try:
                    retval.append(self.read_number(int(char)))
                except ValueError:
                    raise ValueError(_("\"%s\" is not a element of callsign"), char)
        return ' '.join(retval)

