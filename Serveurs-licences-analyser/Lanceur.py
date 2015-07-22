#!/usr/bin/env python3.4

__author__ = 'Brice VICO'
"""
date: 21/07/2015

Permet d'informer l'application web du lancement / arrêt du programme d'écoute de connexion.
"""

import subprocess
import os

proc = subprocess.Popen("/home/brice/PycharmProjects/stats/Main.py")
print(proc.pid)
print(os.popen('curl http://localhost/StageLirmm/PCM/web/app_dev.php/serviceIsStart/1/' + str(proc.pid)).read())

proc.wait()

print(os.popen('curl http://localhost/StageLirmm/PCM/web/app_dev.php/serviceIsStop/1').read())

print(os.popen("/etc/init.d/statsBV stop").read())