#!/usr/bin/python3
#Arquitetura Sistemas Distribuí­dos

import pika
import time
from sys import argv
from .base import BaseAlgorithm

class FloodingCoordenates(BaseAlgorithm):
    def __init__(self, main_algorithm, my_id, neighbors, channel, n_neighbors):
        self.main_algorithm = main_algorithm
        self.coordenates = {}
        self.message_formats = ["-"]
        self.message_counter = 0
        self.state = "ACTIVE"
        self.neighbors = neighbors
        self.channel = channel
        self.n_neighbors = n_neighbors
        self.my_id = my_id

    def _on_message(self, message):
        if self.state == "ACTIVE":
            source, message = message.split(":")
            node, coordenate = message.split("-")
            self.message_counter += 1
            self.coordenates[node] = eval(coordenate)
            self.broadcast(source, message)
            if self.message_counter == self.n_neighbors:
                print("Finished broadcasting")
                self.state = "OK"
                self.finish()

    def broadcast(self, source, message):
        for n in self.neighbors:
            if n != source:
                self.send(n, message)

    def finish(self):
        self.main_algorithm.algorithms.remove(self)
        self.main_algorithm.setup_convex_hull(self.coordenates)
