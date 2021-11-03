
class Connection:
    def __init__(self, cluster):
        self.processor_list = cluster
        self.message = None

    def ask_ready(self, id_):
        processor = self.processor_list[id_]
        return processor.get_waiting.remote()

    def send_id(self, id_):
        while True:
            if self.ask_ready(id_):
                processor = self.processor_list[id_]
                processor.put_message.remote(id_)
                break

    def send_ack(self, id_):
        while True:
            processor = self.processor_list[id_]
            processor.put_message.remote("ack")

    def get_message(self):
        return self.message
