#!/usr/bin/python3
#Arquitetura Sistemas Distribuí­dos

import pika
import time
from sys import argv
from random import randint
from distributed import ShouterPlus, FloodingCoordenates, GiftWrapping

<<<<<<< HEAD
class GiftWrapping(BaseAlgorithm):
=======
class ConvexHull:
>>>>>>> 83b32ab25f99900df5562e6e4fe3bd651fb5c4bf
    def __init__(self, my_id, neighbors, channel, n_neighbors):
        self.connection = pika.BlockingConnection()
        self.channel = connection.channel()
        self.channel.queue_declare(queue=my_id, auto_delete=True)
        for n in self.neighbors:
            self.channel.queue_declare(queue=n, auto_delete=True)
        self.shouter = ShouterPlus(self.my_id, self.neighbors, self.channel)
        self.channel.basic_consume(queue=meu_id, on_message_callback=self._callback, auto_ack=True)
        self.n_neighbors = n_neighbors
        self.algorithms = []
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
        if not message_handler(body.decode()):
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
    if(len(argv) < 2):
        print('USO: {} <MEU_ID> <VIZINHOS>'.format(argv[0]))
        exit(1)

    my_id = argv[1]
    neighbors = argv[2:]

    gw = GiftWrapping(my_id, neighbors)
    gw.start()
