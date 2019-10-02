#!/usr/bin/python3
# Envoltório Convexo
# Nome: Eduardo Borsa, Eduardo Ferreira e Tiago Paiva

import pika
import time
from sys import argv
from random import randint
from distributed import ShouterPlus, FloodingCoordenates

class ConvexHull(object):
    def __init__(self, my_id, n_neighbors, neighbors):
        self.connection = pika.BlockingConnection()
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=my_id, auto_delete=True)
        self.neighbors = neighbors
        self.my_id = my_id
        for n in self.neighbors:
            self.channel.queue_declare(queue=n, auto_delete=True)
        self.shouter = ShouterPlus(self, self.my_id, self.neighbors, self.channel)
        self.algorithms = [self.shouter]
        self.channel.basic_consume(queue=self.my_id, on_message_callback=self._callback, auto_ack=True)
        self.n_neighbors = n_neighbors
        self.coordenate = (randint(0,100), randint(0,100))
        self.messages = []

    def start(self):
        try:
            print("Aguardando mensagens...")
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
            self.connection.close()

    def _callback(self, channel, method, prop, body):
        print("Nova mensagem recebida: {}".format(body.decode()))
        if not self.message_handler(body.decode()):
            self.messages.append(body.decode())

    def message_handler(self, message):
        treated_message = False
        for alg in self.algorithms:
            if alg.new_message(message):
                treated_message = True
                break
        return treated_message

    def review_messages(self):
        for message in self.messages:
            self.message_handler(message)

    def setup_flooding(self, tree_neighbors):
        self.algorithms.append(FloodingCoordenates(self, self.my_id, tree_neighbors, self.channel, self.n_neighbors))
        self.review_messages()

    def setup_convex_hull(self):
        return


if __name__ == "__main__":
    if(len(argv) < 3):
        print('USO: {} <MEU_ID> <N_VIZINHOS> <VIZINHOS>'.format(argv[0]))
        exit(1)

    my_id = argv[1]
    n_neighbors = argv[2]
    neighbors = argv[3:]

    ch = ConvexHull(my_id, n_neighbors, neighbors)
    ch.start()

