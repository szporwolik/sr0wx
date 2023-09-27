# About & History
Every automatic station's callsign in Poland (SP) is prefixed by "SR".
This software is intended to read aloud weather information and other
data pulled from the internet and sensors - that's why Michał Sadowski 
(SQ6JNX) initially called it SR0WX (sr0wx.py).

This software was initially created by Dawid SQ6EMM and Michał SQ6JNX.
The first installation was started in February 2009 at SQ6EMM's QTH, next 
station was started as SP6YRE with the support of Wrocław, PL 
authorities and some local EMCOM community. 

Then the idea was spread across Poland, actual list and map of the 
working sr0wx.py stations can be checked at http://wx.ostol.pl/.

Michał SQ6JNX actively supported the project till 2016. In the 2019 
Paweł SQ9ATK forked it at github and keep the support till 2023, 
when main activity was carried over by hams from SP9MOA club at 
Niepołomice, Poland.

Extensions are called ``plugins`` (or ``languages``).
Main part of SR0WX is called ``core``.

**Note:** this software connects to the internet and exchanges 
data, sending some of the information about your installation. 
**Please refer to code if this is a concern for you.**

# Installation
## System requirements
Development is made with the assumption that those stations are usually
running at the low-end machines. Old terminals or Raspberry PI based 
installations are common. 

While this software can run on 32bit machines, we strongly recommend
to purchase 64bit terminal. Most of the linux distributions do not
support 32bit anymore and setting up the system may be challenging.

sr0wx.py does not require specific OS, but we strongly recommend to use
Debian/Ubuntu based Linux distros, as this is what the sr0wx team is 
using and this was assumed in the documentation. 

Internet connection is required and for most of the installations you 
will likely need a sound card.

## Radio hardware
Most of the installations are basing on either PTT control from serial
port (which is supported by this software) or VOX solution.

## Environment
The following system dependencies are to be met or are recommended:
``git``

Python version shall be 3.7.3 at least to ensure proper execution. 

Also the software requires Python 3.7 with the following modules:
``pygame numpy aiogTTS six astral serial inflect``

## Cloning the code
You can download the script using git by running the following command
``git clone https://github.com/szporwolik/sr0wx``

## Configuration
Rename ``config.py_example`` to ``config.py``. 
Modify ``config.py``, so it suits your needs.

**Please ensure that your callsign is transmitted at the begining and
end of each transmission**.

## System config
In most of the systems the following permissions are usually needed 
to execute the script:
``sudo gpasswd --add ${USER} dialout`` 
``sudo gpasswd --add ${USER} audio``

## Runing
Runing the script:
``python3 ./sr0wx.py``

## Cron installation
You can make ensure automatic execution with the crontab:
``crontab -e``

Please refer to the crontab documentation.

# Writing a plugin
Write a plugin and add it into ``src`` direcotory. Add init code into ``src\module_init.py`` and sample config into ``config.py_example``

# Translation
Translations are handled by the ``gettext`` module, you can support the project by creating translation for your language.

# Contributors
You can find full list of contributors at:
- github.com/sq6jnx/sr0wx.py
- github.com/sq9atk/sr0wx

# License
Initial code was released by SQ6JNX using Apache License, Version 2.0. This license applies to the whole repository.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
