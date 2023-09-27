# -*- coding: utf-8 -*-

"""This is plugin scaffold module. All modules 
   Shall derivate from this class.
"""

#   Copyright 2014 Michal Sadowski (sq6jnx at hamradio dot pl)
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

class SR0WXPlugin(object):
    """Base class for SR0WX plugins."""
    active = False
    message = ""
    source = ""
    
    def __init__(self):
        pass

    def get_data(self):
        """Prepares plugin object"""
        
        msg = "This method should be implemented in child class"
        raise NotImplementedError(msg)
