
class QuantumProcessor:
    """A class for defining a quantum processor"""

    def __init__(self, qubit_num=1, execution_time=0.1):
        """Define a quantum processor

        Args:
            qubit_num (int, optional): The number of qubits. Defaults to 1.
            execution_time (float, optional): The execution time of each quantum gate. Defaults to 0.1.
        """
        self.id = 0
        self.qubit_num = qubit_num
        self.execution_time = execution_time

    def set_id(self, id_):
        """Set a processor id to this quantum processor

        Args:
            id_ (int): A processor id
        """
        self.id = id_

    def get_id(self):
        """Return the id of this quantum processor

        Returns:
            int: The id of this quantum processor
        """
        return self.id

    def get_info(self):
        """Return an details about properties of this quantum processor

        Returns:
            dict: A dict that contains details of this quantum processor
        """
        info = {
            "id": self.id,
            "qubit_num": self.qubit_num,
            "execution_time": self.execution_time
        }
        return info
