__author__ = 'Brice VICO'

from datetime import datetime

PORTNUMBER = {"30001": "Cadence", "30003" : "Cadence", "54001": "Coventor", "55001": "Coventor",
              "56001": "Coventor", "27001": "Synopsys"}

class Connexion:

    def __init__(self, ip, port):
        """
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
        return "Date : " + self.date.__str__()+ " Adresse ip : " + self.ip + " Logiciel : " + self.portName
