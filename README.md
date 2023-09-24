# About & History
Every automatic station's callsign in Poland (SP) is prefixed by "SR".
This software is intended to read aloud weather informations (mainly).
That's why Michał Sadowski (SQ6JNX) initially called it SR0WX.

Extensions are called ``plugins`` (or ``languages``).
Main part of SR0WX is called ``core``.

This software was initially created by Dawid SQ6EMM and Michał SQ6JNX.
Intial instalation was startre in Feb 2009 at SQ6EMM QTH, next station was 
started as SP6YRE and the idea was spread across Poland.

Michał SQ6JNX supported the project to 2016. In the 2019 Paweł SQ9ATK forked it
and keep the support till 2023, when main activity was continued by the hams from
SP9MOA.

# Installation
## Operating system
sr0wx.py does not reqire specific OS, but we strongly recommend to use Debian/Ubuntu based distros.

Ubuntu does not support 32bit images which will be required for some of the installations, in that 
case we recommend Debian 12 install.

## Environment
This software requires Python 3.11 and following dependencies:
``sudo apt-get install git python-pygame python-tz python-imaging python-serial python-six curl php7.0 php7.0-curl php7.0-xml ffmpeg``
Ubuntu and Debian distros are recommended.

## System config
In most of the systems the following persmissions are usually needed to execute the script:
``sudo gpasswd --add ${USER} dialout
sudo gpasswd --add ${USER} audio``

## Configuration
Rename ``config.py_example`` to ``config.py``. 
Modify ``config.py`` to suit your needs 

## Runing


## Cron instalation
``crontab -e``

# Transimitting
Configuration is handled within config.py file, you shall not modify anything out of that file.

# Writting a plugin
Write a plugin and add it into ``src`` direcotory. Add init code into ``src\module_init.py`` and sample config into ``config.py``

# License
Initial code was released by SQ6JNX using Apache License, Version 2.0. This license applies to the whole repository.