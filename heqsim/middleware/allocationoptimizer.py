import random
import math
import copy


class AllocationOptimizer:
    """A class to optimize index allocation"""

    def __init__(self, network, gate_list, iter_num=1000):
        """Create an index allocation optimizer

        Args:
            network (Network): A network that connects physical quantum processors
            gate_list (list): A list of quantum gates
            iter_num (int, optional): A number of iterations. Defaults to 1000.
        """
        self.network = network
        self.gate_list = gate_list
        self.iter_num = iter_num

        self.processors = list(self.network.graph.nodes)
        self.processor_num = len(self.processors)
        self.qubit_num = [processor.qubit_num for processor in self.processors]

        self.ET = [processor.execution_time for processor in self.processors]
        self.D = self.network.generate_distance_matrix()

    def calc_eng(self, index_dict):
        """Calculate energy in the simulated annealing

        Args:
            index_dict (dict): A dict that maps processor ids to list of indices of allocated qubits in each physical quantum processors

        Returns:
            float: The value of cost function
        """
        gate_cost_list = [0 for processor in self.processors]
        comm_cost_list = [0 for processor in self.processors]
        cost_list = [0 for processor in self.processors]

        for processor_id in range(self.processor_num):
            for gate in self.gate_list:
                if gate.name != "CNOT" and gate.index in index_dict[processor_id]:
                    gate_cost_list[processor_id] += self.ET[processor_id]

        for processor_id in range(self.processor_num):
            for gate in self.gate_list:
                if gate.name == "CNOT":
                    if gate.index in index_dict[processor_id] and gate.target_index in index_dict[processor_id]:
                        comm_cost_list[processor_id] += 0
                    elif gate.index in index_dict[processor_id]:
                        for the_other_processor_id in range(self.processor_num):
                            if gate.target_index in index_dict[the_other_processor_id]:
                                comm_cost_list[processor_id] += self.D[processor_id][the_other_processor_id]
                    elif gate.target_index in index_dict[processor_id]:
                        for the_other_processor_id in range(self.processor_num):
                            if gate.index in index_dict[the_other_processor_id]:
                                comm_cost_list[processor_id] += self.D[processor_id][the_other_processor_id]

        for processor_id in range(self.processor_num):
            cost_list[processor_id] = gate_cost_list[processor_id] + comm_cost_list[processor_id]

        return max(cost_list)

    def move(self, index_dict):
        """Find a neighboring qubit allocation

        Args:
            index_dict (dict): A dict that maps processor ids to list of indices of allocated qubits in each physical quantum processors

        Returns:
            dict: The new result of the qubit allocation
        """
        qubit1_index = random.randint(0, len(index_dict[0]) - 1)
        qubit2_index = random.randint(0, len(index_dict[1]) - 1)

        index_dict[0][qubit1_index], index_dict[1][qubit2_index] = index_dict[1][qubit2_index], index_dict[0][qubit1_index]
        return index_dict

    def accept_prob(self, cur_eng, new_eng, temp):
        """Calculate the accept probability of the current qubit allocation

        Args:
            cur_eng (float): The current energy value
            new_eng (float): The next energy value
            temp (int): The temperature value

        Returns:
            float: The value of this acceptance probability
        """
        if new_eng < cur_eng:
            return 1
        else:
            return math.exp(-(new_eng - cur_eng) / temp)

    def optimize(self, index_dict):
        """Optimize the index allocation process

        Args:
            index_dict (dict): A dict that maps processor ids to list of indices of allocated qubits in each physical quantum processors

        Returns:
            dict: The result of the optimized index allocation
        """
        state = index_dict
        T = 100

        for iter_ in range(self.iter_num):

            temp = T * (1 - iter_ / self.iter_num)

            state_copy = copy.deepcopy(state)
            new_state = self.move(state_copy)

            cur_eng = self.calc_eng(state)
            new_eng = self.calc_eng(new_state)

            if self.accept_prob(cur_eng, new_eng, temp) >= random.random():
                state = new_state

        return state
