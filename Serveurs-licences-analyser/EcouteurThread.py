__author__ = 'Brice VICO'

from threading import Thread
from collections import defaultdict
from Connexion import Connexion


class EcouteurThread(Thread):
    """
    Cette classe permet d'écouter les connexions entrante et sortante sur un serveur de licences.

    Pourquoi thread ?

        Car si il y à plusieurs serveur, alors on effectue les écoutes en paralléle
    """

    def __init__(self, id, ssh, bdd, lock):
        super().__init__()

        self.id = id
        self.ssh = ssh
        self.d = defaultdict()
        self.bdd = bdd
        self.lock = lock

    def run(self):
        """
        Fonction principale d'analyse.
        Exclusion de 127.0.0.1 et d'une adresse ip distante qui serai égale à celle locale.

        Cette fonction fait appel à un objet BDD afin de pouvoir manipuler les élements de la Base de données.

        :return:
        """

        print("========== Analyse du serveur " + str(self.id) + " en cour... ==========")

        while True:
            out = self.ssh.getFichiers()
            newTab = []
            toSupp = []

            for ligne in out.readlines():
                tokens = ligne.split()
                local = tokens[3].split(':')
                distant = tokens[4].split(':')

                if local[0] != distant[0] and distant[0] != "127.0.0.1":
                    newTab.append(distant[0] + ":" + local[1])

                    if distant[0] + ":" + local[1] not in self.d.keys():
                        self.d[distant[0] + ":" + local[1]] = Connexion(distant[0], local[1])
                        print(
                            "Entrée sur le serveur " + str(self.id) + " : " + str(self.d[distant[0] + ":" + local[1]]))

                        if ':' not in self.d[distant[0] + ":" + local[1]].portName:
                            self.lock.acquire(True)

                            self.bdd.updateListeIp()
                            self.bdd.addNbrConnexion(self.d[distant[0] + ":" + local[1]].portName,
                                                     self.d[distant[0] + ":" + local[1]].ip)
                            self.bdd.addNbrConnexionEnCours(self.d[distant[0] + ":" + local[1]].portName)

                            self.lock.release()

            for key in self.d.keys():
                if key not in newTab:
                    print("Sortie sur le serveur " + str(self.id) + " : " + str(self.d[key]))

                    if ':' not in self.d[key].portName:
                        self.lock.acquire(True)

                        self.bdd.removeNbrConnexionEnCours(self.d[key].portName)

                        self.lock.release()

                    toSupp.append(key)

            for val in toSupp:
                del self.d[val]

                newTab.clear()
                toSupp.clear()

        self.ssh.terminer()
