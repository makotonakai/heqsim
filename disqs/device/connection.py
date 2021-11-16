from queue import Queue


class Connection:
    def __init__(self):
        self.request_link = Queue(maxsize=1)
        self.ack_link = Queue(maxsize=1)
        self.message_link = Queue(maxsize=1)

    def send_request(self, request):
        self.request_link.put(request, block=False)

    def get_request(self):
        request = self.request_link.get()
        return request

    def send_ack(self, ack):
        self.ack_link.put(ack)

    def get_ack(self):
        ack = self.ack_link.get()
        return ack

    def send_message(self, message):
        self.message_link.put(message)

    def get_message(self):
        message = self.message_link.get()
        return message
