__author__ = 'Brice VICO'

from datetime import datetime

"""
Contient une classe et un tableau permettant de lier un port à son logiciel
"""

PORTNUMBER = {"30001": "Cadence", "30003": "Cadence", "30005": "Cadence", "54001": "Coventor", "55001": "Coventor",
              "56001": "Coventor", "27001": "Synopsys"}

class Connexion:
    """
    Classe permettant de présenter une connexion aux serveurs comme un objet.
    """

    def __init__(self, ip, port):
        """
        Cette fonction, constructeur de la classe, va lié le port au logiciel si celui-ci est connus.

        :param ip:
        :param port
        :return:
        """
        self.ip = ip
        self.date = datetime.now()
        self.port = port

        if self.port in PORTNUMBER.keys():
            self.portName = PORTNUMBER[self.port]
        else:
            self.portName = "Inconnu:" + self.port

    def __str__(self):
        """
        :return:
        """
        return "Date : " + self.date.__str__()+ " Adresse ip : " + self.ip + " Logiciel : " + self.portName
