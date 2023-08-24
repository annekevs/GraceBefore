import os
import subprocess as sp

# Path above are for windows applications
paths_win = {
    'notepad': "C:\\Program Files\\Notepad++\\notepad++.exe",
    'discord': "C:\\Users\\ashut\\AppData\\Local\\Discord\\app-1.0.9003\\Discord.exe",
    'calculator': "C:\\Windows\\System32\\calc.exe"
}

paths = {
    'firefox': "~/snap/bin/firefox",
    'libreoffice': "~/usr/bin/libreoffice"
}

def open_firefox():
    os.startfile(paths['firefox'])
    
def open_libreoffice():
    os.startfile(paths['libreoffice'])
