from queue import Queue


class Link:
    """A class for a link between two quantum processors"""

    def __init__(self):
        """Create a new link"""
        self.request_link = Queue(maxsize=1)
        self.ack_link = Queue(maxsize=1)
        self.control_message_link = Queue(maxsize=2)
        self.target_message_link = Queue(maxsize=2)

    def send_request(self, request):
        """Send a request to another quantum processor

        Args:
            request (int): The processor id of the sender (quantum processor)
        """
        self.request_link.put(request, block=False)

    def get_request(self):
        """Get a request from another quantum processor

        Returns:
            int: The processor id of the sender
        """
        request = self.request_link.get()
        return request

    def send_ack(self):
        """Send ack to the sender"""
        self.ack_link.put("ack")

    def get_ack(self):
        """Get ack from the receiver

        Returns:
            str: ack
        """
        ack = self.ack_link.get()
        return ack

    def send_control_message(self, message):
        """Send 1st measurement result to the receiver

        Args:
            message (int): The measurement result of the 1st qubit
        """
        self.control_message_link.put(message)

    def get_control_message(self):
        """Get 1st measurement result from the sender

        Returns:
            int: The measurement result of the 1st qubit
        """
        message = self.control_message_link.get()
        return message

    def send_target_message(self, message):
        """Send 2nd measurement result to the sender

        Args:
            message (int): The measurement result of the 2nd qubit
        """
        self.target_message_link.put(message)

    def get_target_message(self):
        """Receive 2nd measurement result from the receiver

        Returns:
            message: The measurement result of the 2nd qubit
        """
        message = self.target_message_link.get()
        return message
