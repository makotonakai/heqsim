from ray.util.queue import Queue
import asyncio
import ray


class Connection:
    def __init__(self):
        self.message_link = Queue(maxsize=1)
        self.ack_link = Queue(maxsize=1)
        self.qlink = Queue(maxsize=2)

    def has_message(self):
        return not self.message_link.empty

    def send_message(self, message):
        self.message_link.put(message, block=False)

    def get_message(self):
        message = self.message_link.get()
        return message

    def has_ack(self):
        return not self.ack_link.empty

    def send_ack(self, ack):
        self.ack_link.put(ack)

    def get_ack(self):
        ack = self.ack_link.get()
        return ack
