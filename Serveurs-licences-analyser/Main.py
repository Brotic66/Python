#!/usr/bin/env python3.4
__author__ = 'Brice VICO'

"""
Contient une classe mais aussi une routine de création d'une instance de la classe Main.
"""

from Connexion import Connexion
from collections import defaultdict
from Remote import Remote
from Bdd import Bdd
from EcouteurThread import EcouteurThread
from threading import RLock

class Main:

    def __init__(self):
        """
        Effectue des actions élémentaires de préparation :

            - Connexion aux serveurs de licences
            - connexion à la BDD
            - lancement des threads

        :return:
        """

        self.ssh = []
        self.d = defaultdict(list)

        print("========== Connexions aux serveurs... ==========")

        self.ssh.append(self.creerConnexion("licences.xxx.fr"))
        self.ssh.append(self.creerConnexion("licence2.xxx.fr"))

        print("========== Connexions etablies ==========")

        print("========== Connexion à la BDD... ==========")

        self.bdd = Bdd()

        print("========== Connexion etablie ==========")

        i = 0
        lock = RLock()

        for serveur in self.ssh:
            t = EcouteurThread(i, serveur, self.bdd, lock)
            t.start()
            i += 1

    def creerConnexion(self, serveur):
        """
        Crée une connexion au serveur en SSH via un objet Remote (voir Remote.py)

        :param serveur:
        :return Remote:
        """
        r = Remote()
        r.connexion(serveur)

        return r

if __name__ == '__main__':
    Main()

