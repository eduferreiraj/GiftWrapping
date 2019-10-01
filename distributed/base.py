class BaseAlgorithm:
    def __init__(self, main_algorithm, *args):
        self.main_algorithm = main_algorithm
        self.message_formats = []
        self.initialize(*args)

    def initialize(self, *args):
        # Initialize the model with the parameters needed to work.
        # Args will be handled by the algorithm.
        # Input: args (tuple)
        # Output: None
        return

    def validate_message(self, message):
        # Validate the message with the self.message_formats list
        # Input: message (str)
        # Output: boolean
        status = False
        for message_format in self.message_formats:
            if message_format in message:
                status = True
        return status

    def new_message(self, message):
        # Function called in the main algorithm. Validate the message and return
        # False if the message doesn't belong here.
        # Input: message (str)
        # Output: boolean
        if not self.validate_message(message):
            return False
        self._on_message(message)
        return True

    def _on_message(self, message):
        # All of the processing in the message by the algorithm occurs here.
        # Input: message (str)
        # Output: None
        return

    def send(self, dest, message):
        # Send a new message to the destination.
        # Input: dest (str), message (str)
        print("Sending {} to {}".format(message, dest))
        self.channel.basic_publish(exchange='', routing_key=dest, body="{}:{}".format(self.my_id, message))


    def finish(self):
        # End the algorithm by removing his instance of the main algorithm.
        self.main_algorithm.algorithms.remove(self)
