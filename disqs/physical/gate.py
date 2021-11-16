from disqs.physical.basicgate import px, py, pz, ph, pcnot
import numpy as np
import time


def apply_px(state, index):
    state_vector = state.vector
    qubit_num = state.qubit_num
    matrix = px(qubit_num, index)
    state.vector = np.dot(matrix, state_vector)


def apply_py(state, index):
    state_vector = state.vector
    qubit_num = state.qubit_num
    matrix = py(qubit_num, index)
    state.vector = np.dot(matrix, state_vector)


def apply_pz(state, index):
    state_vector = state.vector
    qubit_num = state.qubit_num
    matrix = py(qubit_num, index)
    state.vector = np.dot(matrix, state_vector)


def apply_ph(state, index):
    state_vector = state.vector
    qubit_num = state.qubit_num
    matrix = ph(qubit_num, index)
    state.vector = np.dot(matrix, state_vector)


def apply_pcnot(state, control_index, target_index):
    state_vector = state.vector
    qubit_num = state.qubit_num
    matrix = pcnot(qubit_num, control_index, target_index)
    state.vector = np.dot(matrix, state_vector)


def x(state, index, sleep_time, lock):
    lock.acquire()
    apply_px(state, index)
    lock.release()
    time.sleep(sleep_time)


def y(state, index, sleep_time, lock):
    lock.acquire()
    apply_py(state, index)
    lock.release()
    time.sleep(sleep_time)


def z(state, index, sleep_time, lock):
    lock.acquire()
    apply_pz(state, index)
    lock.release()
    time.sleep(sleep_time)


def h(state, index, sleep_time, lock):
    lock.acquire()
    apply_ph(state, index)
    lock.release()
    time.sleep(sleep_time)


def cnot(state, control_index, target_index, sleep_time, lock):
    lock.acquire()
    apply_pcnot(state, control_index, target_index)
    lock.release()
    time.sleep(sleep_time)


def measure(state, index, sleep_time, lock):
    """Measure a qubit
    Args:
        index (int): the index of a qubit that users measure
    """

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
            measure_prob["0"] += state_dict[key]**2
        else:
            measure_prob["1"] += state_dict[key]**2

    # Perform measurement
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
        prob = new_state_dict[key]**2
        prob_list.append(prob)

    for key in list(new_state_dict.keys()):
        new_state_dict[key] *= np.sqrt(1 / sum(prob_list))

    state.vector = np.array(list(new_state_dict.values()))
    state.qubit_num -= 1
    return measure_result
