#!/usr/bin/python3
#Arquitetura Sistemas Distribuí­dos
# Envoltório Convexo
# Nome: Eduardo Borsa, Eduardo Ferreira e Tiago Paiva

import pika
import time
from sys import argv
from .base import BaseAlgorithm
from .flooding_coordenates import FloodingCoordenates

class ShouterPlus(BaseAlgorithm):
    def __init__(self, main_algorithm, my_id, neighbors, channel):
        self.main_algorithm = main_algorithm
        self.message_formats = ["SIM", "Q"]
        self.my_id = my_id
        self.neighbors = neighbors
        self.state = 'IDLE'
        self.message_counter = 0
        self.tree_nodes = []
        self.channel = channel
        self.dad = None

    def _on_message(self, message):
        if message == "Q":
            self.state = 'STARTER'
            print("Eu sou o STARTER!")
            source = ''
        else:
            source, message = message.split(":")

        if self.state == 'STARTER':
            for n in self.neighbors:
                self.send(n, 'Q')
            self.state = 'ACTIVE'

        elif self.state == 'IDLE':
            self.tree_nodes.append(source)
            self.dad = source
            self.send(source, 'SIM')
            self.message_counter += 1
            for n in self.neighbors:
                if not n == source:
                    self.send(n, 'Q')
            self.state = 'ACTIVE'

        elif self.state == 'ACTIVE':
            self.message_counter += 1
            if message == 'SIM':
                self.tree_nodes.append(source)

        if self.message_counter == len(self.neighbors):
            self.state = 'OK'
            self.finish()

    def finish(self):
        # End the algorithm by removing his instance of the main algorithm.
        self.main_algorithm.algorithms.remove(self)
        self.main_algorithm.setup_flooding(self.tree_nodes)
