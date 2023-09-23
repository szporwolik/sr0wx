# sr0wx
## About
Every automatic station's callsign in Poland (SP) is prefixed by "SR".
This software is intended to read aloud weather informations (mainly).
That's why we (or I) called it SR0WX.

Extensions (mentioned above) are called ``modules`` (or ``languages``).
Main part of SR0WX is called ``core``.

SR0WX consists quite a lot of independent files so I (SQ6JNX) suggest
reading other manuals (mainly configuration- and internationalization
manual) in the same time as reading this one. Really.

## History

## Installation
### Environment
    This software requires Python 3.11 and following dependencies:
    sudo apt-get install git python-pygame python-tz python-imaging python-serial python-six curl php7.0 php7.0-curl php7.0-xml ffmpeg

### System config
sudo gpasswd --add ${USER} dialout
sudo gpasswd --add ${USER} audio 

### Cron instalation

## Configuration
Configuration is handled within config.py file, you shall not modify anything out of that file.

### Sample generation
GENEROWANIE SAMPLI
Będąc w katalogu audio_generator:
  php index.php

Generowane są sample z tablicy $słownik z pliku slownik.php.
Pozostałe tablice to tylko przechowalnia fraz go wygenerowania.
