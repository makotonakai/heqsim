from heqsim.hardware.basicgate import x_, y_, z_, h_, cnot_, rx_, ry_, rz_, phase_
import numpy as np
import time


def apply_x(state, index):
    """Apply an X state to a given quantum state

    Args:
        state (QuantumState): A quantum state
        index (int): The index of the qubit that an X gate is applied to
    """
    state_vector = state.vector
    qubit_num = state.qubit_num
    matrix = x_(qubit_num, index)
    state.vector = np.dot(matrix, state_vector)


def apply_y(state, index):
    """Apply a Y state to a given quantum state

    Args:
        state (QuantumState): A quantum state
        index (int): The index of the qubit that an Y gate is applied to
    """
    state_vector = state.vector
    qubit_num = state.qubit_num
    matrix = y_(qubit_num, index)
    state.vector = np.dot(matrix, state_vector)


def apply_z(state, index):
    """Apply a Z state to a given quantum state

    Args:
        state (QuantumState): A quantum state
        index (int): The index of the qubit that a Z gate is applied to
    """
    state_vector = state.vector
    qubit_num = state.qubit_num
    matrix = z_(qubit_num, index)
    state.vector = np.dot(matrix, state_vector)


def apply_h(state, index):
    """Apply an H state to a given quantum state

    Args:
        state (QuantumState): A quantum state
        index (int): The index of the qubit that an H gate is applied to
    """
    state_vector = state.vector
    qubit_num = state.qubit_num
    matrix = h_(qubit_num, index)
    state.vector = np.dot(matrix, state_vector)


def apply_cnot(state, control_index, target_index):
    """Apply an CNOT state to a given quantum state on a local quantum processor

    Args:
        state (QuantumState): A quantum state
        index (int): The index of the qubit that a CNOT gate is applied to
    """
    state_vector = state.vector
    qubit_num = state.qubit_num
    matrix = cnot_(qubit_num, control_index, target_index)
    state.vector = np.dot(matrix, state_vector)


def apply_rx(state, index, theta):
    """Apply an Rx state to a given quantum state

    Args:
        state (QuantumState): A quantum state
        index (int): The index of the qubit that an Rx gate is applied to
        theta (float): The rotation angle of this Rx gate
    """
    state_vector = state.vector
    qubit_num = state.qubit_num
    matrix = rx_(qubit_num, index, theta)
    state.vector = np.dot(matrix, state_vector)


def apply_ry(state, index, theta):
    """Apply an Ry state to a given quantum state

    Args:
        state (QuantumState): A quantum state
        index (int): The index of the qubit that an Ry gate is applied to
        theta (float): The rotation angle of this Ry gate
    """
    state_vector = state.vector
    qubit_num = state.qubit_num
    matrix = ry_(qubit_num, index, theta)
    state.vector = np.dot(matrix, state_vector)


def apply_rz(state, index, theta):
    """Apply an Rz state to a given quantum state

    Args:
        state (QuantumState): A quantum state
        index (int): The index of the qubit that an Rz gate is applied to
        theta (float): The rotation angle of this Rz gate
    """
    state_vector = state.vector
    qubit_num = state.qubit_num
    matrix = rz_(qubit_num, index, theta)
    state.vector = np.dot(matrix, state_vector)


def apply_phase(state, index, theta):
    """Apply a phase state to a given quantum state

    Args:
        state (QuantumState): A quantum state
        index (int): The index of the qubit that a phase gate is applied to
    """
    state_vector = state.vector
    qubit_num = state.qubit_num
    matrix = phase_(qubit_num, index, theta)
    state.vector = np.dot(matrix, state_vector)


def x(state, index, execution_time, lock):
    """Execute an X gate

    Args:
        state (QuantumState): A quantum state
        index (int): The index of the qubit that a phase gate is applied to
        execution_time (float): The execution time of  this X gate
        lock (threading.Lock): A lock to take before executing this X gate
    """
    if lock is not None:
        lock.acquire()
    apply_x(state, index)
    if lock is not None:
        lock.release()
    time.sleep(execution_time)


def y(state, index, execution_time, lock):
    """Execute an Y gate

    Args:
        state (QuantumState): A quantum state
        index (int): The index of The qubit that a phase gate is applied to
        execution_time (float): The execution time of this Y gate
        lock (threading.Lock): A lock to take before executing this Y gate
    """
    if lock is not None:
        lock.acquire()
    apply_y(state, index)
    if lock is not None:
        lock.release()
    time.sleep(execution_time)


def z(state, index, execution_time, lock):
    """Execute an Z gate

    Args:
        state (QuantumState): A quantum state
        index (int): The index of the qubit that a phase gate is applied to
        execution_time (float): The execution time of  this Z gate
        lock (threading.Lock): A lock to take before executing this Z gate
    """
    if lock is not None:
        lock.acquire()
    apply_z(state, index)
    if lock is not None:
        lock.release()
    time.sleep(execution_time)


def h(state, index, execution_time, lock):
    """Execute an H gate

    Args:
        state (QuantumState): A quantum state
        index (int): The index of the qubit that a phase gate is applied to
        execution_time (float): The execution time of  this H gate
        lock (threading.Lock): A lock to take before executing this H gate
    """
    if lock is not None:
        lock.acquire()
    apply_h(state, index)
    if lock is not None:
        lock.release()
    time.sleep(execution_time)


def cnot(state, control_index, target_index, execution_time, lock):
    """Execute an CNOT gate on a quantum processor

    Args:
        state (QuantumState): A quantum state
        control_index (int): The index of the control qubit
        target_index (int): The index of the target qubit
        execution_time (float): The execution time of this CNOT gate
        lock (threading.Lock): A lock to take before executing this CNOT gate
    """
    if lock is not None:
        lock.acquire()
    apply_cnot(state, control_index, target_index)
    if lock is not None:
        lock.release()
    time.sleep(execution_time)


def swap(state, control_index, target_index, execution_time, lock):
    """Execute an CNOT gate on a quantum processor

    Args:
        state (QuantumState): A quantum state
        control_index (int): The index of the control qubit
        target_index (int): The index of the target qubit
        execution_time (float): The execution time of this CNOT gate
        lock (threading.Lock): A lock to take before executing this CNOT gate
    """
    if lock is not None:
        lock.acquire()
    apply_cnot(state, control_index, target_index)
    apply_cnot(state, target_index, control_index)
    apply_cnot(state, control_index, target_index)
    if lock is not None:
        lock.release()
    time.sleep(execution_time)


def rx(state, index, theta, execution_time, lock):
    """Execute an Rx gate

    Args:
        state (QuantumState): A quantum state
        index (int): The index of the qubit that a phase gate is applied to
        theta (float): The rotation angle of this Rx gate
        execution_time (float): The execution time of this Rx gate
        lock (threading.Lock): A lock to take before executing this Rx gate
    """
    if lock is not None:
        lock.acquire()
    apply_rx(state, index, theta)
    if lock is not None:
        lock.release()
    time.sleep(execution_time)


def ry(state, index, theta, execution_time, lock):
    """Execute an Ry gate

    Args:
        state (QuantumState): A quantum state
        index (int): The index of the qubit that a phase gate is applied to
        theta (float): The rotation angle of this Ry gate
        execution_time (float): The execution time of this Ry gate
        lock (threading.Lock): A lock to take before executing this Ry gate
    """
    if lock is not None:
        lock.acquire()
    apply_ry(state, index, theta)
    if lock is not None:
        lock.release()
    time.sleep(execution_time)


def rz(state, index, theta, execution_time, lock):
    """Execute an Rz gate

    Args:
        state (QuantumState): A quantum state
        index (int): The index of the qubit that a phase gate is applied to
        theta (float): The rotation angle of this Rz gate
        execution_time (float): The execution time of this Rz gate
        lock (threading.Lock): A lock to take before executing this Rz gate
    """
    if lock is not None:
        lock.acquire()
    apply_rz(state, index, theta)
    if lock is not None:
        lock.release()
    time.sleep(execution_time)


def phase(state, index, theta, execution_time, lock):
    """Execute an phase gate

    Args:
        state (QuantumState): A quantum state
        index (int): The index of the qubit that a phase gate is applied to
        theta (float): The rotation angle of this phase gate
        execution_time (float): The execution time of this phase gate
        lock (threading.Lock): A lock to take before executing this phase gate
    """
    if lock is not None:
        lock.acquire()
    apply_phase(state, index, theta)
    if lock is not None:
        lock.release()
    time.sleep(execution_time)


def measure(state, index, execution_time, lock):
    """Measure a qubit
    Args:
        index (int): The index of a qubit that users measure
        lock (threading.Lock): A lock to take before executing this phase gate
    """

    if lock is not None:
        lock.acquire()

    # Measurement probability of the measured qubit
    measure_prob = {"0": 0, "1": 0}

    # Pairs of state & its probability amplitude
    state_dict = {}
    for num in range(len(state.vector)):
        comp_basis = bin(num)[2:].zfill(state.qubit_num)
        state_dict[comp_basis] = state.vector[num]

    # Calculate measurement probability of the measured qubit
    for key in list(state_dict.keys()):
        if key[index] == "0":
            measure_prob["0"] += abs(state_dict[key])**2
        else:
            measure_prob["1"] += abs(state_dict[key])**2

    # # Perform measurement
    measure_result = np.random.choice(2, 1, p=list(measure_prob.values()))[0]

    # Pairs of each of the updated states & its probability amplitude
    new_state_dict = {}
    for num in range(len(state.vector)):
        comp_basis = bin(num)[2:].zfill(state.qubit_num)
        if comp_basis[index] == str(measure_result):
            comp_basis_list = list(comp_basis)
            del comp_basis_list[index]
            new_comp_basis = "".join(comp_basis_list)
            new_state_dict[new_comp_basis] = state.vector[num]

    # Update each of the probability amplitudes
    prob_list = []
    for key in list(new_state_dict.keys()):
        prob = abs(new_state_dict[key])**2
        prob_list.append(prob)
    for key in list(new_state_dict.keys()):
        new_state_dict[key] *= np.sqrt(1 / sum(prob_list))

    state.vector = np.array(list(new_state_dict.values()))
    state.qubit_num -= 1

    if lock is not None:
        lock.release()

    time.sleep(execution_time)

    return measure_result
