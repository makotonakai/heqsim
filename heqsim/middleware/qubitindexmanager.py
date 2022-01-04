class QubitIndexManager:
    """A class for the module that manages which qubit is a part of which data qubits / communication qubits / quantum links"""

    def __init__(self, processor_list, network):
        """Create a new qubit index manager

          Args:
              processor_list (list): A list of quantum processors
              network (Network): A network that connects quantum processors
        """
        self.processor_list = processor_list
        self.network = network
        self.qubit_num = 0
        self.dict = {
            "processor": {},
            "communication": {},
            "link": {}
        }

    def get_dict(self):
        """Return the content of this qubit index manager

        Returns:
            [type]: [description]
        """
        return self.dict

    def prepare_all_qubits(self):
        """Calculate the total number of required qubits"""
        for processor in self.processor_list:
            self.qubit_num += processor.qubit_num
        for processor in self.processor_list:
            self.qubit_num += processor.qubit_num
        self.qubit_num += self.network.get_processor_num()
        self.qubit_num += self.network.get_link_num() * 2

    def get_total_qubit_num(self):
        """Return the total number of required qubits

        Returns:
            int: The total number of required qubits
        """
        return self.qubit_num

    def setup(self):
        """Prepare the content of this qubit index manager"""
        self.prepare_all_qubits()
        qubit_index_list = [num for num in range(self.qubit_num)]
        start = 0
        end = 0
        for processor in self.processor_list:
            end += processor.qubit_num
            self.dict["processor"][processor.id] = qubit_index_list[start:end]
            start = end

        for processor in self.processor_list:
            end += 1
            self.dict["communication"][processor.id] = qubit_index_list[start:end]
            start = end

        link_num = self.network.get_link_num()
        for link_id in range(link_num):
            end += 2
            self.dict["link"][link_id] = qubit_index_list[start:end]
            start = end
