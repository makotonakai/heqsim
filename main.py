from logical.circuit import QuantumCircuit

qc = QuantumCircuit(4)

for i in range(4):
    qc.x(i)

qc.execute()

