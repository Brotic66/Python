# Script-Python
Recueil de script Python écrit pour de l'administration serveur.

#### AddRulesIptables.python ##
    Script permettant de lier des demandes d'ouverture de ports d'une application web avec le pare-feu (iptables)
    Le principe est que l'on récupère des installations qui ont été validé (demande d'ouverture de ports pour des adresse IPs).
    On va lire uniquement le logiciel (afin de récupérer le port associé à celui-ci) et un objet Doctrine ArrayCollection contenant la liste des adresses IPs pour l'installation.
