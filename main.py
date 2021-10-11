from Logical.Circuit import QuantumCircuit

qc = QuantumCircuit(4)
qc.allocate_index()
cluster = qc.cluster
for processor in cluster.processor_list:
    name = processor.device_name
    print("{}:{}".format(name, cluster.index_dict[name]))