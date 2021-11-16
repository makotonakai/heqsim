import numpy as np

Imat = np.eye(2)


def px(n, index):
    """Create an X gate
    Args:
        n (int): number of qubits on a quantum circuit
        index (int): the index of a qubit that a gate is applied
    Returns:
        np.array : the matrix of an X gate
    """
    matrix = 1
    X = np.array([[0, 1], [1, 0]])
    for i in range(n):
        if i == index:
            matrix = np.kron(matrix, X)
        else:
            matrix = np.kron(matrix, Imat)

    return matrix


def py(n, index):
    """Create an Y gate
    Args:
        n (int): number of qubits on a quantum circuit
        index (int): the index of a qubit that a gate is applied
    Returns:
        np.array : the matrix of an Y gate
    """
    matrix = 1
    Y = np.array([[0, -1j], [1j, 0]])
    for i in range(n):
        if i == index:
            matrix = np.kron(matrix, Y)
        else:
            matrix = np.kron(matrix, Imat)

    return matrix


def pz(n, index):
    """Create an Z gate
    Args:
        n (int): number of qubits on a quantum circuit
        index (int): the index of a qubit that a gate is applied
    Returns:
        np.array : the matrix of an Z gate
    """
    matrix = 1
    Z = np.array([[1, 0], [0, -1]])
    for i in range(n):
        if i == index:
            matrix = np.kron(matrix, Z)
        else:
            matrix = np.kron(matrix, Imat)

    return matrix


def ph(n, index):
    """Create an H gate
    Args:
        n (int): number of qubits on a quantum circuit
        index (int): the index of a qubit that a gate is applied
    Returns:
        np.array : the matrix of an H gate
    """
    matrix = 1
    H = np.array([[1 / np.sqrt(2), 1 / np.sqrt(2)],
                 [1 / np.sqrt(2), - 1 / np.sqrt(2)]])
    for i in range(n):
        if i == index:
            matrix = np.kron(matrix, H)
        else:
            matrix = np.kron(matrix, Imat)

    return matrix


def pcnot(n, control_index, target_index):
    """Create an CNOT gate
    Args:
        n (int): number of qubits on a quantum circuit
        control_index (int): the index of a controlled qubit
        target_index (int): the index of a target qubit
    Returns:
        np.array : the matrix of an X gate
    """
    cx = np.zeros((2**n, 2**n))
    control_bin_list = [format(num, 'b').zfill(n) for num in range(2**n)]
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

    for index in range(2**n):
        control_ = int(control_bin_list[index], 2)
        target_ = int(target_bin_list[index], 2)
        cx[control_][target_] = 1

    return cx
