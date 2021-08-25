
from PhysicalGate import *
from PhysicalState import *
import numpy as np


class PhysicalCircuit:

    def __init__(self, n):
        self.n = n
        self.state = PhysicalState(self.n).statevector

    def px(self, idx):
        xmatrix = px_(self.n, idx)
        self.state = np.dot(xmatrix, self.state)

    def py(self, idx):
        ymatrix = py_(self.n, idx)
        self.state = np.dot(ymatrix, self.state)

    def pz(self, idx):
        zmatrix = pz_(self.n, idx)
        self.state = np.dot(zmatrix, self.state)

    def ph(self, idx):
        hmatrix = ph_(self.n, idx)
        self.state = np.dot(hmatrix, self.state)

    def pcx(self, control_idx, target_idx):
        cxmatrix = pcx_(self.n, control_idx, target_idx)
        self.state = np.dot(cxmatrix, self.state)

    def measure(self, idx):

        # 確率
        prob = [prob_amp**2 for prob_amp in self.state]

        # 状態と確率
        prob_dict = {}
        for state in range(len(prob)):
            prob_dict[format(state, 'b').zfill(self.n)] = prob[state]

        # 測定確率を計算
        measure_prob = [0, 0]
        for state in list(prob_dict.keys()):
            if state[idx] == "0" and prob_dict[state] > 0:
                measure_prob[0] += 1
            elif state[idx] == "1" and prob_dict[state] > 0:
                measure_prob[1] += 1
        measure_prob = [num/sum(measure_prob) for num in measure_prob]
        measure_result = np.random.choice(range(2), 1, p=measure_prob)[0]
        print(measure_result)

        # 状態ベクトルを更新
        statevector_dict = {}
        for state in range(len(prob)):
            statevector_dict[format(state, 'b').zfill(self.n)] = self.state[state]

        new_statevector_dict = {}
        for state in list(statevector_dict.keys()):
            if state[idx] == measure_result:
                new_statevector_dict[state] = statevector_dict[state]
        print(statevector_dict)


if __name__ == "__main__":

    pc = PhysicalCircuit(2)
    pc.pcx(1,0)
    pc.measure(0)