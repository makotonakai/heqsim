import time
import ray


@ray.remote
class Link:
    def __init__(self, destination, gate):
        self.destination = destination
        self.gate = gate
        self.setup()

    def setup(self):
        if self.gate.role == "control":
            self.source_id = self.gate.control_id
            self.destination_id = self.gate.target_id
        else:
            self.source_id = self.gate.target_id
            self.destination_id = self.gate.control_id

    def send_request(self):

        request = {
            "id": self.gate.id,
            "source": self.source_id,
            "destination": self.destination_id
        }
        self.destination.put_request.remote(request)
        time.sleep(1)
