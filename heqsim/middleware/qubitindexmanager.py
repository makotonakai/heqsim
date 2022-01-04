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
            dict: The dict of all the qubit indices
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

    def add_index(self, kind, id_):
        """Add a new qubit index

        Args:
            kind (str)): "processor", "communication" or "link"
            id_ (int): The id for a particular processor / communication qubit (or quantum device) / communication link
        """
        new_qubit_index = self.qubit_num
        self.dict[kind][id_].append(self.qubit_num)
        self.qubit_num += 1

    def delete_index(self, kind, id_, index):
        """Delete a particular index from the content of this qubit index manager

        Args:
            kind (str): "processor", "communication" or "link"
            id_ (int): The id for a particular processor / communication qubit (or quantum device) / communication link
            index (int): The index of qubit indices of the indices list you choose
                        e.g.  the 2nd element (index) of {"processor": {0:[0, 1, 2]}} is 1
        """
        # Delete 1 qubit from the total qubit number
        self.qubit_num -= 1

        # Get what index you have to delete
        index_to_delete = self.dict[kind][id_][index]

        # "processor", "communciation", or "link"
        for kind_key in list(self.dict.keys()):

            # For all the processor / communication / link ids
            for id_key in list(self.dict[kind_key].keys()):

                # For all the indices in the indices list in the particular processor, communication qubits / communication links
                for qubit_index in self.dict[kind_key][id_key]:

                    # If this index is same as the one you're looking for
                    if qubit_index == index_to_delete:

                        # Get the element index in the particular indices list
                        index_ = self.dict[kind_key][id_key].index(qubit_index)

                        # Get the length of the particular indices list
                        len_index_list = len(self.dict[kind_key][id_key])

                        # Remove the particular index you are looking for
                        self.dict[kind_key][id_key].remove(index_to_delete)

                        # If that is not the last index in the particular index
                        if index_ != len_index_list - 1:

                            # Substract 1 from the next elements in the same list
                            self.dict[kind_key][id_key][index_] -= 1

                    # If this index is larger than the index you have to delete
                    elif qubit_index > index_to_delete:

                        # Substract 1 from this index
                        index_ = self.dict[kind_key][id_key].index(qubit_index)
                        self.dict[kind_key][id_key][index_] -= 1
