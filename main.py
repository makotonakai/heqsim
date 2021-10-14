from logical.circuit import QuantumCircuit

n = 2
qc = QuantumCircuit(n)

qc.x(0)
qc.x(1)
# for i in range(n):
#     qc.x(i)

qc.execute()

