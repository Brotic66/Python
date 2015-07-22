__author__ = 'Brice VICO'

import paramiko

class Remote:
    """
    Cette classe, utilisant Paramiko (https://github.com/paramiko/paramiko), est une classe permettant de stocker
    une connexion, état compris, dans un objet.
    """

    def __init__(self):
        """
        :return:
        """
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()

    def connexion(self, serveur):
        """
        Connexion au serveur

        :param serveur:
        :return:
        """
        self.serveur = serveur
        self.client.connect(serveur, 22, 'brice.vico')

    def getFichiers(self):
        """
        Tente de récupérer le résultat d'une commande.
        Si la connexion à été coupée, alors on se reconnecte.

        :return stdout:
        """
        test = False

        while not test:
            try:
                stdin, stdout, stderr = self.client.exec_command('netstat -n | grep \"tcp\" | grep \"ESTABLISHED\"')
                test = True
            except paramiko.SSHException:
                self.connexion(self.serveur)

        return stdout

    def terminer(self):
        self.client.close()

