import numpy as np

Imat = np.eye(2)


def x_(nqubits, index):
    """Create an X gate
    Args:
        nqubits (int): The number of qubits on a quantum circuit
        index (int): The index of a qubit that a gate is applied
    Returns:
        np.array : The matrix of an X gate
    """
    matrix = 1
    X = np.array([[0, 1], [1, 0]])
    for i in range(nqubits):
        if i == index:
            matrix = np.kron(matrix, X)
        else:
            matrix = np.kron(matrix, Imat)

    return matrix


def y_(nqubits, index):
    """Create an Y gate
    Args:
        nqubits (int): The number of qubits on a quantum circuit
        index (int): The index of a qubit that a gate is applied
    Returns:
        np.array : The matrix of an Y gate
    """
    matrix = 1
    Y = np.array([[0, -1j], [1j, 0]])
    for i in range(nqubits):
        if i == index:
            matrix = np.kron(matrix, Y)
        else:
            matrix = np.kron(matrix, Imat)

    return matrix


def z_(nqubits, index):
    """Create an Z gate
    Args:
        nqubits (int): The number of qubits on a quantum circuit
        index (int): The index of a qubit that a gate is applied
    Returns:
        np.array : The matrix of an Z gate
    """
    matrix = 1
    Z = np.array([[1, 0], [0, -1]])
    for i in range(nqubits):
        if i == index:
            matrix = np.kron(matrix, Z)
        else:
            matrix = np.kron(matrix, Imat)

    return matrix


def h_(nqubits, index):
    """Create an H gate
    Args:
        nqubits (int): The number of qubits on a quantum circuit
        index (int): The index of a qubit that a gate is applied
    Returns:
        np.array : The matrix of an H gate
    """
    matrix = 1
    H = np.array([[1 / np.sqrt(2), 1 / np.sqrt(2)],
                 [1 / np.sqrt(2), - 1 / np.sqrt(2)]])
    for i in range(nqubits):
        if i == index:
            matrix = np.kron(matrix, H)
        else:
            matrix = np.kron(matrix, Imat)

    return matrix


def cnot_(nqubits, control_index, target_index):
    """Create an CNOT gate
    Args:
        nqubits (int): The number of qubits on a quantum circuit
        control_index (int): The index of a controlled qubit
        target_index (int): The index of a target qubit
    Returns:
        np.array : The matrix of an X gate
    """
    cx = np.zeros((2**nqubits, 2**nqubits))
    control_bin_list = [format(num, 'b').zfill(nqubits) for num in range(2**nqubits)]
    target_bin_list = []
    for control_bin in control_bin_list:
        target_bin = list(control_bin)
        if control_bin[control_index] == '1':
            if target_bin[target_index] == '0':
                target_bin[target_index] = '1'
            else:
                target_bin[target_index] = '0'
        target_bin = "".join(target_bin)
        target_bin_list.append(target_bin)

    for index in range(2**nqubits):
        control_ = int(control_bin_list[index], 2)
        target_ = int(target_bin_list[index], 2)
        cx[control_][target_] = 1

    return cx


def rx_(nqubits, index, theta):
    """Create an RX gate
    Args:
        nqubits (int): The number of qubits on a quantum circuit
        index (int): The index of a qubit that a gate is applied
    Returns:
        np.array : The matrix of an Z gate
    """
    matrix = 1
    rx = np.array([[np.cos(theta / 2), -1j * np.sin(theta / 2)],
                  [-1j * np.sin(theta / 2), np.cos(theta / 2)]])
    for i in range(nqubits):
        if i == index:
            matrix = np.kron(matrix, rx)
        else:
            matrix = np.kron(matrix, Imat)

    return matrix


def ry_(nqubits, index, theta):
    """Create an RY gate
    Args:
        nqubits (int): The number of qubits on a quantum circuit
        index (int): The index of a qubit that a gate is applied
    Returns:
        np.array : The matrix of an Z gate
    """
    matrix = 1
    ry = np.array([[np.cos(theta / 2), -np.sin(theta / 2)],
                  [np.sin(theta / 2), np.cos(theta / 2)]])
    for i in range(nqubits):
        if i == index:
            matrix = np.kron(matrix, ry)
        else:
            matrix = np.kron(matrix, Imat)

    return matrix


def rz_(nqubits, index, theta):
    """Create an RZ gate
    Args:
        nqubits (int): The number of qubits on a quantum circuit
        index (int): The index of a qubit that a gate is applied
    Returns:
        np.array : The matrix of an Z gate
    """
    matrix = 1
    rz = np.array([[np.exp(-1j * theta / 2), 0],
                  [0, np.exp(1j * theta / 2)]])
    for i in range(nqubits):
        if i == index:
            matrix = np.kron(matrix, rz)
        else:
            matrix = np.kron(matrix, Imat)

    return matrix


def phase_(nqubits, index, theta):
    """Create a phase gate
    Args:
        nqubits (int): The number of qubits on a quantum circuit
        index (int): The index of a qubit that a gate is applied
    Returns:
        np.array : The matrix of an Z gate
    """
    matrix = 1
    phase = np.array([[1, 0],
                      [0, np.exp(1j * theta)]])
    for i in range(nqubits):
        if i == index:
            matrix = np.kron(matrix, phase)
        else:
            matrix = np.kron(matrix, Imat)

    return matrix
