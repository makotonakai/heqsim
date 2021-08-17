import numpy as np


I = np.eye(2)
matrix = 1

def x_(n, idx):

    global matrix
    X = np.array([[0,1],[1,0]])
    for i in range(n):
        if i == idx:
            matrix = np.kron(X, matrix)
        else:
            matrix = np.kron(I, matrix)

    return matrix

def y_(n, idx):

    global matrix
    Y = np.array([[0,-1j],[1j,0]])
    for i in range(n):
        if i == idx:
            matrix = np.kron(Y, matrix)
        else:
            matrix = np.kron(I, matrix)

    return matrix

def z_(n, idx):

    global matrix
    Z = np.array([[1,0],[0,-1]])
    for i in range(n):
        if i == idx:
            matrix = np.kron(Z, matrix)
        else:
            matrix = np.kron(I, matrix)

    return matrix

def h_(n, idx):

    global matrix
    H = np.array([[1,1],[1,-1]])/np.sqrt(2)
    for i in range(n):
        if i == idx:
            matrix = np.kron(H, matrix)
        else:
            matrix = np.kron(I, matrix)

    return matrix

def cx_(n, control_idx, target_idx):

    cx = np.zeros((2**n, 2**n))
    control_bin_list = [format(num, 'b').zfill(n) for num in range(2**n)]
    target_bin_list = []
    for control_bin in control_bin_list:
        target_bin = list(control_bin)
        if control_bin[control_idx] == '1':
            if target_bin[target_idx] == '0':
                target_bin[target_idx] = '1'
            else:
                target_bin[target_idx] = '0'
        target_bin = "".join(target_bin)
        target_bin_list.append(target_bin)

    for idx in range(2**n):
        control_ = int(control_bin_list[idx], 2)
        target_ = int(target_bin_list[idx], 2)
        cx[control_][target_] = 1

    return cx

