import math

import numpy as np
import Instance
import numpy


def shift_right(mtrx, x):
    num_of_columns = mtrx.shape[1]
    if num_of_columns >= x:
        matrix = mtrx.copy()
        for _ in range(x):
            last_column = matrix[:, mtrx.shape[1] - 1]
            matrix[:, mtrx.shape[1] - 2] = np.add(matrix[:, mtrx.shape[1] - 1], matrix[:, mtrx.shape[1] - 2])
            shape = (matrix.shape[0], 1)
            zeros = numpy.zeros(shape)
            matrix = numpy.concatenate((zeros, matrix), axis=1)
            matrix = numpy.delete(matrix, matrix.shape[1] - 1, axis=1)
        return matrix
    else:
        return [[sum(mtrx[r, :])] for r in range(mtrx.shape[0])]


def shift_down(mtrx, x):
    matrix = mtrx.copy()
    last_column = mtrx[:,mtrx.shape[1]-1].copy()
    for _ in range(x):
        last_column = np.append(last_column, 0)
    for _ in range(x):
        matrix = np.concatenate((np.zeros((1, matrix.shape[1])), matrix))
    vs = np.vstack(last_column)
    lc = matrix[:, matrix.shape[1] - 1]
    matrix[:, matrix.shape[1]-1] = last_column
    return matrix


def get_starting_matrix(agent, v):
    max_reward = max([r for r in v.distribution])
    max_utility = agent.utility_budget
    matrix = numpy.zeros((max_reward + 1, max_utility + 1))
    matrix[0][0] = 1
    return matrix


def print_matrix(matrix):
    for j in range(len(matrix)):
        print(matrix[j])
    print()


def get_matrix_value(matrix, reward, used):
    if reward < 0 or used < 0 or reward > len(matrix) - 1 or used > len(matrix[0]) - 1:
        return 0
    else:
        return matrix[reward][used]


def get_stay_matrix(matrix, max_r, max_u, prob, theta):
    stay_matrix = np.zeros((max_r + 1, max_u + 1))
    for reward in range(len(matrix)):
        stay_matrix[reward][max_u] = get_matrix_value(matrix, reward, max_u)
        for used in range(max_u):
            stay_matrix[reward][used] = (theta * prob[0] + 1 - theta) * get_matrix_value(matrix, reward, used)
    return stay_matrix


def get_go_matrix(matrix, max_r, max_u, prob, theta):
    go_matrix = np.zeros((max_r + 1, max_u + 1))
    for reward in range(max_r + 1):
        for used in range(max_u + 1):
            go_matrix[reward][used] = 0
            for r in prob:
                if r != 0:
                    go_matrix[reward][used] = go_matrix[reward][used] + theta * prob[r] * get_matrix_value(matrix,
                                                                                                           reward - r,
                                                                                                           used - 1)
    return go_matrix


def add_zeros_to_bottom(mtrx, x):
    matrix = mtrx.copy()
    for _ in range(x):
        shape = (1, matrix.shape[1])
        zeros = np.zeros(shape)
        matrix = np.concatenate((matrix, zeros))
    return matrix

def add_diff_height_mtrxs(mtrx1, mtrx2):
    height_diff = abs(mtrx2.shape[0]-mtrx1.shape[0])
    if mtrx1.shape[0] > mtrx2.shape[0]:
        return np.add(mtrx1, add_zeros_to_bottom(mtrx2, height_diff))
    return np.add(add_zeros_to_bottom(mtrx1, height_diff), mtrx2)


def new_matrix(mtrx, prob, theta):
    if 0 not in prob:
        prob[0] = 0
    new_matrix = (1-theta) * mtrx.copy()
    for r in prob:
        p = prob[r]
        if r == 0:
            u = 0
        else:
            u = 1  # might change
        p_matrix = theta * p * shift_right(shift_down(mtrx.copy(), r), u)
        new_matrix = add_diff_height_mtrxs(new_matrix, p_matrix)
        if new_matrix is None:
            print()
        #print("r:"+ str(r)+ ", p:"+str(p))
        #print(new_matrix)
    return new_matrix

'''
def update_matrix(matrix, theta, dist):
    if 0 not in dist:
        dist[0] = 0
    max_r = np.shape(matrix)[0] + max([r for r in dist]) - 1
    max_u = np.shape(matrix)[1] - 1
    if type(max_r) != int:
        raise Exception("Reward must be an integer!")
    stay_matrix = get_stay_matrix(matrix, max_r, max_u, dist, theta)
    go_matrix = get_go_matrix(matrix, max_r, max_u, dist, theta)
    # print_matrix(new_matrix)
    new_matrix = np.add(stay_matrix, go_matrix)
    return new_matrix
'''

def update_theta(matrix, theta):
    return theta * sum(matrix[:, matrix.shape[1]-1])


def get_tot_reward(matrices):
    sum = 0
    for a_hash in matrices:
        m = matrices[a_hash]
        u_max = len(m[0]) - 1
        for r in range(len(m)):
            for u in range(u_max + 1):
                sum += get_matrix_value(m, r, u) * r
    return sum


'''
def get_expected_value_of_path(instance, path):
    matrices = []
//    thetas = {}
//    for agent_hash in instance.agents_map:
//        matrices.append(get_starting_matrix(instance.agents[agent_hash], path[0][agent_hash][0]))

//    for vertex in instance.map:
//        thetas[vertex.name] = 1

//    for t in range(min(instance.get_horizon(), len(path))):
//        for agent_index in range(len(instance.agents)):
            # print(matrices[agent_index])
            if path[t][agent_index][1]:
                continue
            vertex = path[t][agent_index][0]
            new_matrix = update_matrix(matrices[agent_index], thetas[vertex.name], vertex.probability)
            new_theta = update_theta(matrices[agent_index], thetas[vertex.name])
            matrices[agent_index] = new_matrix
            thetas[vertex.name] = new_theta
    return get_tot_reward(matrices)'''
