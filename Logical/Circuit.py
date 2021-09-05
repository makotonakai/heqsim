from Logical.Gate import *
from Logical.State import QuantumState
import numpy as np
import sys
import os

from Device.Cluster import QCluster

class QuantumCircuit:

    def __init__(self, n):
        self.n = n
        self.state = QuantumState(self.n).statevector
        self.cxgraph = {str(idx):[] for idx in range(self.n)}
        self.cluster = QCluster()

    def x(self, idx):
        xmatrix = x_(self.n, idx)
        self.state = np.dot(xmatrix, self.state)

    def y(self, idx):
        ymatrix = y_(self.n, idx)
        self.state = np.dot(ymatrix, self.state)

    def z(self, idx):
        zmatrix = z_(self.n, idx)
        self.state = np.dot(zmatrix, self.state)

    def h(self, idx):
        hmatrix = h_(self.n, idx)
        self.state = np.dot(hmatrix, self.state)

    def cx(self, control_idx, target_idx):
        cxmatrix = cx_(self.n, control_idx, target_idx)
        self.state = np.dot(cxmatrix, self.state)
        self.cxgraph[str(control_idx)].append(str(target_idx))
        self.cxgraph[str(target_idx)].append(str(control_idx))
    
    def contract(self, v, w):
        v = str(v)
        w = str(w)
        newnode = v + w
        
        self.cxgraph[newnode] = self.cxgraph[v]
        del self.cxgraph[v]

        for node in self.cxgraph.keys():
            if v in self.cxgraph[node]:
                for idx in range(len(self.cxgraph[node])):
                    if self.cxgraph[node][idx] == v:
                        self.cxgraph[node][idx] = newnode

        for node in self.cxgraph[w]:
            if node != newnode:
                self.cxgraph[newnode].append(node)
            self.cxgraph[node].remove(w)
            if node != newnode:
                self.cxgraph[node].append(newnode)

        del self.cxgraph[w]
        return newnode

    def get_cluster_config(self):
        return self.cluster.ProcessorList

    # def Karger(self, nodelist):
    #     # while len(self.cxgraph)>2:
    #     #     v = random.choice(list(self.cxgraph.keys()))
    #     #     w = random.choice(self.cxgraph[v])
    #     #     self.contract(v, w)
    #     #     mincut = len(self.cxgraph[list(cxgraph.keys())[0]])
    #     #     self.cuts.append(mincut)
    #     # return self.cuts
    #     while len(node):
    #         v = random.choice(list(self.cxgraph.keys()))
    #         w = random.choice([node for node in self.cxgraph[v] if len(node)==1])
    #         vw = self.contract(v, w)
    #     for key in list(self.cxgraph.keys()):
    #         if len(key) == 4:
    #             self.result_cxgraph[key] = self.cxgraph[key]
    #             del self.cxgraph[key]

        

