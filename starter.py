#!/usr/bin/env python3

#
# Starter for the Broadcast Distributed Algorithm implementation using RabbitMQ
# (C)2019 by Luiz Lima Jr.
#

from sys import argv
import pika


def main():
    if len(argv) < 3:
        print(f"USAGE: {argv[0]} <initiator> <I>")
        exit(1)
    routing_key = argv[1]
    info = argv[2]

    connection = pika.BlockingConnection()
    channel = connection.channel()

    channel.queue_declare(queue=routing_key, auto_delete=True)
    channel.basic_publish(
        exchange='',
        routing_key=routing_key,
        body=info)

    print(f"Message {info} sent")

    connection.close()


if __name__ == '__main__':
    main()
