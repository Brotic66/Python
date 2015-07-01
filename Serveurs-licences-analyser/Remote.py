__author__ = 'Brice VICO'

import paramiko

class Remote:

    def __init__(self):
        """
        :return:
        """
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()

    def connexion(self, serveur):
        """
        :param serveur:
        :return:
        """
        self.client.connect(serveur, 22, 'brice.vico')

    def getFichiers(self):
        """
        :return stdout:
        """
        stdin, stdout, stderr = self.client.exec_command('netstat -n | grep \"tcp\" | grep \"ESTABLISHED\"')

        return stdout

    def terminer(self):
        self.client.close()

