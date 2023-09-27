
# Initial version - this will automate localisation

import subprocess,os

if os.path.exists(r'C:\Dev\sr0wx\tools\files.txt'):
    os.remove(r'C:\Dev\sr0wx\tools\files.txt')

lines = ['C:\Dev\sr0wx\sr0wx.py']

import glob
lines +=glob.glob("C:\Dev\sr0wx\src\*.py")

with open(r'C:\Dev\sr0wx\tools\temp_files.txt', 'w') as f:
    for line in lines:
        f.write(line)
        f.write('\n')

subprocess.call([r'C:\Program Files\gettext-iconv\bin\xgettext.exe',"-f",r'C:\Dev\sr0wx\tools\temp_files.txt',"-o",r'C:\Dev\sr0wx\locales\sr0wx.pot'])
subprocess.call([r'C:\Program Files\gettext-iconv\bin\msgmerge.exe',"--update",r'C:\Dev\sr0wx\locales\pl\LC_MESSAGES\sr0wx.po',r'C:\Dev\sr0wx\locales\sr0wx.pot'])
subprocess.call([r'C:\Program Files\gettext-iconv\bin\msgfmt.exe',"-o",r'C:\Dev\sr0wx\locales\pl\LC_MESSAGES\sr0wx.mo',r'C:\Dev\sr0wx\locales\pl\LC_MESSAGES\sr0wx.po'])

if os.path.exists(r'C:\Dev\sr0wx\tools\files.txt'):
    os.remove(r'C:\Dev\sr0wx\tools\files.txt')