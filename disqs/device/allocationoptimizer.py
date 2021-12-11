import random
import math
import copy


class AllocationOptimizer:

    def __init__(self, network, gate_list, iter_num=1000):

        self.network = network
        self.gate_list = gate_list
        self.iter_num = iter_num

        self.processors = list(self.network.graph.nodes)
        self.processor_num = len(self.processors)
        self.qubit_num = [processor.qubit_num for processor in self.processors]

        self.ET = [processor.execution_time for processor in self.processors]
        self.D = self.network.generate_distance_matrix()

    def calc_eng(self, Q):

        gate_cost_list = [0 for processor in self.processors]
        comm_cost_list = [0 for processor in self.processors]
        cost_list = [0 for processor in self.processors]

        for processor_id in range(self.processor_num):
            for gate in self.gate_list:
                if gate.name != "CNOT" and gate.index in Q[processor_id]:
                    gate_cost_list[processor_id] += self.ET[processor_id]

        for processor_id in range(self.processor_num):
            for gate in self.gate_list:
                if gate.name == "CNOT":
                    if gate.index in Q[processor_id] and gate.target_index in Q[processor_id]:
                        comm_cost_list[processor_id] += 0
                    elif gate.index in Q[processor_id]:
                        for the_other_processor_id in range(self.processor_num):
                            if gate.target_index in Q[the_other_processor_id]:
                                comm_cost_list[processor_id] += self.D[processor_id][the_other_processor_id]
                    elif gate.target_index in Q[processor_id]:
                        for the_other_processor_id in range(self.processor_num):
                            if gate.index in Q[the_other_processor_id]:
                                comm_cost_list[processor_id] += self.D[processor_id][the_other_processor_id]

        for processor_id in range(self.processor_num):
            cost_list[processor_id] = gate_cost_list[processor_id] + comm_cost_list[processor_id]

        return max(cost_list)

    def move(self, Q):
        processor1 = random.randint(0, len(Q.keys()) - 1)
        processor2 = random.randint(0, len(Q.keys()) - 1)

        qubit1_index = random.randint(0, len(Q[processor1]) - 1)
        qubit2_index = random.randint(0, len(Q[processor2]) - 1)

        Q[processor1][qubit1_index], Q[processor2][qubit2_index] = Q[processor2][qubit2_index], Q[processor1][qubit1_index]
        return Q

    def accept_prob(self, cur_eng, new_eng, temp):
        if new_eng < cur_eng:
            return 1
        else:
            return math.exp(-(new_eng - cur_eng) / temp)

    def execute(self, Q):

        state = Q
        T = 100

        for iter_ in range(self.iter_num):

            temp = T * (1 - iter_ / self.iter_num)

            state_copy = copy.deepcopy(state)
            new_state = self.move(state_copy)

            cur_eng = self.calc_eng(state)
            new_eng = self.calc_eng(new_state)

            if self.accept_prob(cur_eng, new_eng, temp) >= random.random():
                state = new_state
                print("{}:{}".format(iter_, new_eng))

        return state
