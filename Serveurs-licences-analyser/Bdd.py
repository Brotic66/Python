__author__ = 'Brice VICO'

import pymysql
from collections import defaultdict
from netaddr import IPNetwork
import re

class Bdd:

    def __init__(self):
        """
        :return:
        """
        self.db = pymysql.connect(host='localhost',
                             user='root',
                             passwd='password',
                             db='Crcc',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
        self.listeIp = defaultdict()

    def updateListeIp(self):
        """
        :return:

        Récupère en base de donnée la liste des Installations valide et le nom du logiciel associé afin d'en extraire
        les adresses Ips.
        """
        with self.db.cursor() as cursor:
            sql = "SELECT i.id, i.ips, l.nom FROM Installation i, Logiciel l WHERE i.valide = 1" \
                  " AND l.id = i.logiciel_id"
            cursor.execute(sql)
            result = cursor.fetchall()

        self.listeIp = self.resultatToListe(result)

    def resultatToListe(self, data):
        """
        :param data:
        :return defaultdict:

        Met le résultat d'une requête SQL (celle de updateListeIp) dans un dictionaire indéxé par le nom des logiciel.
        """
        toReturn = defaultdict(list)

        for installation in data:
            final = defaultdict(list)
            listeIp = self.getIps(installation['ips'])

            for ip in listeIp:
                final[installation['id']].append(ip)

            toReturn[installation['nom']].append(final)

        return toReturn

    def getIps(self, data):
        """
        :param data:
        :return array:

        Retourne un tableau contenant une liste d'adresse IP(passage d'un ArrayCollection de Doctrine vers un tableau classique)
        """
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

    def addNbrConnexion(self, logiciel, ip):
        """
        :param logiciel:
        :param ip:
        :return:

        Incrémente le nombre de connexion pour une installation dans la base de données de l'application web
        """
        if logiciel in self.listeIp.keys():
            for installation in self.listeIp[logiciel]:
                for id in installation.keys():
                    for ipBase in installation[id]:
                        if ip in IPNetwork(ipBase):
                            with self.db.cursor() as cursor:
                                sql = "UPDATE Installation SET nbrConnexion=nbrConnexion + 1 WHERE id=%s"
                                cursor.execute(sql, (id,))
                                self.db.commit()

                            return True

        return False

if __name__ == "__main__":
    bdd = Bdd()
    bdd.updateListeIp()

    for logiciel in bdd.listeIp.keys():
        print(logiciel)

        for installation in bdd.listeIp[logiciel]:
            for id in installation.keys():
                print("===== " + str(id) + " =====")

                for ipBase in installation[id]:
                    print("=== " + ipBase + " ===")

                    for ip in IPNetwork(ipBase):
                        print(ip)
