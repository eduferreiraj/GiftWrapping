#!/usr/bin/python3
#Arquitetura Sistemas Distribuí­dos

import pika
import time
from sys import argv
from base import BaseAlgorithm

class FloodingCoordenates(BaseAlgorithm):
    def initialize(self, my_id, neighbors, channel, n_neighbors):
        self.coordenates_counter = 0
        self.coordenates = {}
        self.message_formats = ["-"]
        self.state = "ACTIVE"

    def _on_message(self, message):
        if self.state == "ACTIVE":
            source, message = message.split(":")
            node, coordenate = message.split("-")
            self.message_counter += 1
            self.coordenates[node] = eval(coordenate)
            self.broadcast(source, message)
            if self.message_counter == n_neighbors:
                self.state = "OK"
                self.finish()

    def broadcast(self, source, message):
        for n in self.neighbors:
            if n != source:
                self.send(n, message)
