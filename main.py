from Logical.Circuit import QuantumCircuit

qc = QuantumCircuit(6)
index_list = qc.allocate_index()
print(index_list)