#!/usr/bin/python3
#Arquitetura Sistemas Distribuí­dos

import pika
import time
from sys import argv
from base import BaseAlgorithm

class GiftWrapping(BaseAlgorithm):
    def initialize(self, my_id, my_coordenates, neighbors, coordenates, channel):
        self.message_format = ["EC"]
        self.coordenates = coordenates
        self.my_coordenates = my_coordenates
        self.my_id = my_id
        self.neighbors = neighbors
        self.state = 'IDLE'
        self.channel = channel
        self.distance = lambda pos_A, pos_B: np.sqrt((pos_A[0] - pos_B[0])**2 + (pos_A[1] - pos_B[1])**2)

    def activate(self):
        self.state = 'ACTIVE'
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
        key_A, key_B = keys[np.where(angles == np.max(angles)[0][0])]
        higher_y = key_A if self.coordenates[key_A][1] > self.coordenates[key_B][1] else key_B
        self.send_message(higher_y, "{}:EC".format(self.my_id))

    def _on_message(self, message):
        source, message = message.split(":")
        print("{} recebi {} de {}".format(self.my_id, message, source))

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
            self.send_message(major_key, "{}:EC".format(self.my_id))
            self.state == 'ACTIVE'

    def calculate_angle(self, node, source):
        adj_A = self.distance(self.my_coordenates, node)
        adj_B = self.distance(self.my_coordenates, source)
        opp = self.distance(node, source)
        return np.arccos((adj_A**2 + adj_B**2 - opp**2)/2*adj_A*adj_B)
