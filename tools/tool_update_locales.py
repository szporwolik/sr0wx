#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Tool to automatically update locale i18n
    files.
    
    GNU gettext is required to run it, bins for
    windows can be downloaded from:
    https://mlocati.github.io/articles/gettext-iconv-windows.html
    
    This shall be run from /tools directory
"""

import subprocess,os,glob,platform

# Hack to make in runing on both Linux and windows
if platform.system() == 'Windows':
    path_xgettext=r'C:\Program Files\gettext-iconv\bin\xgettext.exe'
    path_msgmerge=r'C:\Program Files\gettext-iconv\bin\msgmerge.exe'
    path_msgfmt=r'C:\Program Files\gettext-iconv\bin\msgfmt.exe'
else:
    path_xgettext=r'xgettext'
    path_msgmerge=r'msgmerge'
    path_msgfmt=r'msgfmt'
    
# Get current path
path_currentdir = os.getcwd()

# Preparation
if os.path.exists(path_currentdir + r'\temp_files.txt'):
    os.remove(path_currentdir + r'\temp_files.txt')

# Create list of files to merge
lines = ['..\sr0wx.py']
lines +=glob.glob("..\src\*.py")
with open(path_currentdir + r'\temp_files.txt', 'w') as f:
    for line in lines:
        f.write(line)
        f.write('\n')

# Re-create pot file
subprocess.call([path_xgettext,"-f",r'temp_files.txt',"-o",r'..\locales\sr0wx.pot'])

# Lang 
languages = ['en','pl']

for el in languages:
    print("Preparing - "+el)
    path_po = r'..\locales\%s\LC_MESSAGES\sr0wx.po' % el
    path_mo = r'..\locales\%s\LC_MESSAGES\sr0wx.mo' % el
    
    subprocess.call([path_msgmerge,"--update",path_po,r'..\locales\sr0wx.pot'])
    subprocess.call([path_msgfmt,"-o",path_mo,r'..\locales\pl\LC_MESSAGES\sr0wx.po'])
    # TBD add additional languages here

# Cleanup
if os.path.exists(path_currentdir + r'\temp_files.txt'):
    os.remove(path_currentdir + r'\temp_files.txt')