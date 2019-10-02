#!/usr/bin/python3
#Arquitetura Sistemas Distribuí­dos
# Envoltório Convexo
# Nome: Eduardo Borsa, Eduardo Ferreira e Tiago Paiva

import pika
import time
from sys import argv
from .base import BaseAlgorithm
import numpy as np

class GiftWrapping(BaseAlgorithm):
    def __init__(self, main_algorithm, my_id, my_coordenates, coordenates, channel):
        self.message_formats = ["EC"]
        self.coordenates = coordenates
        self.my_coordenates = my_coordenates
        self.my_id = my_id
        self.state = 'IDLE'
        self.channel = channel
        self.distance = lambda pos_A, pos_B: np.sqrt((pos_A[0] - pos_B[0])**2 + (pos_A[1] - pos_B[1])**2)
        self.convex_hull = False
        self.main_algorithm = main_algorithm


    def activate(self):
        self.state = 'ACTIVE'
        self.convex_hull = True
        options = [item for item in self.coordenates.items()]
        keys = []
        angles = []
        for key_A, coord_A in options:
            for key_B, coord_B in options:
                if key_A == key_B:
                    continue
                keys.append((key_A, key_B))
                angles.append(self.calculate_angle(coord_A, coord_B))

            options.remove((key_A, coord_A))
        key_A, key_B = keys[np.where(angles == np.max(angles))[0][0]]
        higher_y = key_A if self.coordenates[key_A][1] > self.coordenates[key_B][1] else key_B
        self.send(higher_y, "EC")

    def _on_message(self, message):
        source, message = message.split(":")

        if self.state == 'IDLE':
            major_key = None
            major_angle = 0.0
            for key, coord in self.coordenates.items():
                if key == source:
                    continue
                angle = self.calculate_angle(coord, self.coordenates[source])
                if angle > major_angle:
                    major_angle = angle
                    major_key = key
            self.send(major_key, "EC")
            self.convex_hull = True
            self.state == 'ACTIVE'

    def calculate_angle(self, node, source):
        adj_A = self.distance(self.my_coordenates, node)
        adj_B = self.distance(self.my_coordenates, source)
        opp = self.distance(node, source)
        cos = (adj_A**2 + adj_B**2 - opp**2)/(2*adj_A*adj_B)
        return np.arccos(cos)
