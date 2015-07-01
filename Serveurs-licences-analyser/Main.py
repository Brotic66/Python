__author__ = 'Brice VICO'

from Connexion import Connexion
from collections import defaultdict
from Remote import Remote
from Bdd import Bdd
from EcouteurThread import EcouteurThread
from threading import RLock

class Main:

    def __init__(self):
        """
        :return:
        """

        self.ssh = []
        self.d = defaultdict(list)

        print("========== Connexions aux serveurs... ==========")

        self.ssh.append(self.creerConnexion("licences.cnfm.fr"))
        self.ssh.append(self.creerConnexion("licence2.cnfm.fr"))

        print("========== Connexions établies ==========")

        print("========== Connexion à la BDD... ==========")

        self.bdd = Bdd()

        print("========== Connexion établie ==========")

        i = 0
        lock = RLock()

        for serveur in self.ssh:
            t = EcouteurThread(i, serveur, self.bdd, lock)
            t.start()
            i += 1

    def creerConnexion(self, serveur):
        """

        :param serveur:
        :return Remote:
        """
        r = Remote()
        r.connexion(serveur)

        return r

if __name__ == '__main__':
    Main()

