#!/usr/bin/env python3

"""
|==========================|
| Les noeuds 'ordinateur'. |
|==========================|

* Dans un graphe qui represente un reseau internet, les noeuds
modelises ici sont les noeuds qui sont capable d'effectuer un calcul.
"""

import time

from raisin.tools import identity
from ..vertex import Vertex


class Computer(Vertex):
    """
    |===============================|
    | Un ordinateur dans un reseau. |
    |===============================|

    * C'est une entitee capable d'executer des taches.
    """
    def __init__(self, mac, *, n=None):
        super().__init__(n=n, name=f"computer_{mac}")
        self.mac = mac
        self.flags["edgecolor"] = "black"
        if mac == identity["mac"]:
            self.flags["facecolor"] = "#ff0000" # Rouge.
        else:
            self.flags["facecolor"] = "#77c100" # Vert.

        self.creation_date = time.time()

        # Historique.
        self.history = {} # A chaque attribu, sa date de mise a jour.
        self.history["creation_date"] = 1/time.time() # Stratageme pour garder la plus vielle valeur.

    def get_attr(self):
        """
        |===================================|
        | Recupere les arguments suffisants |
        | a la reconstitution de self.      |
        |===================================|

        Returns
        -------
        :return: Les clefs et les valeurs a passer a l'initialisateur
            de facon a instancier un nouvel objet de contenu identique a self.
        :rtype: dict
        """
        return {
            "initializer": {
                "mac": self.mac,
                "n": self.n},
            "internal": {"history": self.history}}

class MySelf(Computer):
    pass
