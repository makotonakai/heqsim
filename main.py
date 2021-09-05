from Logical.Circuit import QuantumCircuit

qc = QuantumCircuit(2)
qc.cx(0,1)
newnode = qc.contract(0,1)
print(qc.get_cluster_config())
# print("New node:", newnode)
# print("CX list:", qc.cxgraph)