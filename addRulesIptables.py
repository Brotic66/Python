# coding=utf-8
'''
Ce fichier contient un script permettant de lier une application web en, PHP 5.6 avec Symfony et doctrine, avec l'administration d'un serveur et nottament de son pare-feu (iptables)
Permet d'ouvrir des ports pour des adresses IPs récupérer en base de données et ajouté via l'application web.
'''

__author__ = 'brice VICO'

import os
import MySQLdb
import re

PORTNUMBER = {"Silvaco Enseignement": 1000, "Cadence Enseignement": 1001, "Synopsys Enseignement": 1002,
              "Memscap Enseignement": 1003, "Coventor Enseignement": 1004}

'''
Cette fonction extrait une liste d'adresse IPs dans un tableau depuis un élément Doctrine ArrayCollection d'une BDD (array SQL étrange...)
'''
def getIps(data):
    listeIp = []
    match = re.search(r'.*a:\d+:{(.*)}}', data)
    listeNonParse = match.group(1)
    result = re.sub(r'i:\d+;s:\d+:', '', listeNonParse)
    result2 = re.search(r'"(.*?)";', result)

    while result != '':
        result2 = re.search(r'"(.*?)";', result)
        result = re.sub(r'("(.*?)";)?', '', result, 1)
        listeIp.append(result2.group(1))

    return listeIp

'''
Cette fonction récupère la liste des installations ayant été validée par un responsable via l'application web.
'''
def recupererInstallationsValide():
    db = MySQLdb.connect("localhost", "xxxxxx", "xxxxxx", "Crcc")
    cursor = db.cursor()
    query = "SELECT i.ips, l.nom FROM Installation i, Logiciel l WHERE valide = 1 AND l.id = i.logiciel_id"
    lines = cursor.execute(query)
    data = cursor.fetchall()
    db.close()

    return data

'''
Cette fonction classe par nom de logiciel dans un Dictionnary, les liste d'adresse IPs
'''
def classerParLogiciel(data):
    listeFinale = {}
    for installation in data:
        if installation[1] in listeFinale:
            listeFinale[installation[1]].append(installation[0])
        else:
            listeFinale[installation[1]] = [installation[0]]

    return listeFinale


'''
########## Main ##########
'''


data = recupererInstallationsValide()
listeFinale = {}

if data:
    listeFinale = classerParLogiciel(data)
else:
    print "Pas de données à traiter"

print os.popen("iptables -F").read()

for logiciel in listeFinale:
    print logiciel + ' : '

    for listeIp in listeFinale[logiciel]:
        ips = getIps(listeIp)
        for ip in ips:
            print os.popen("iptables -A INPUT -s " + ip + " -p tcp --dport " + str(
                PORTNUMBER[logiciel]) + " -j ACCEPT").read()
            print os.popen("iptables -A INPUT -s " + ip + " -p udp --dport " + str(
                PORTNUMBER[logiciel]) + " -j ACCEPT").read()

for logiciel in PORTNUMBER:
    print os.popen('iptables -A INPUT -p tcp --dport ' + str(PORTNUMBER[logiciel]) + " -j DROP").read()
    print os.popen('iptables -A INPUT -p udp --dport ' + str(PORTNUMBER[logiciel]) + " -j DROP").read()

# Permet de conserver la mise à jour de iptables aprés un redémarrage (coupure de courant ou autre...)
print os.popen('service iptables-persistent save').read()
