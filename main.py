from logical.circuit import QuantumCircuit

n = 4
qc = QuantumCircuit(n)
indices = qc.get_indices()
print(indices)

