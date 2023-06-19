import numpy as np
from decimal import *
import Instance
import numpy


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
        return Decimal(matrix[reward][used])


def get_stay_matrix(matrix, max_r, max_u, prob, theta):
    stay_matrix = np.zeros((max_r + 1, max_u + 1))
    for reward in range(len(matrix)):
        stay_matrix[reward][max_u] = Decimal(get_matrix_value(matrix, reward, max_u))
        for used in range(max_u):
            stay_matrix[reward][used] = (Decimal(theta) * Decimal(prob[0]) + 1 - Decimal(theta)) * Decimal(
                get_matrix_value(matrix, reward, used))
    return stay_matrix


def get_go_matrix(matrix, max_r, max_u, prob, theta):
    go_matrix = np.zeros((max_r + 1, max_u + 1))
    for reward in range(max_r + 1):
        for used in range(max_u + 1):
            go_matrix[reward][used] = Decimal(0)
            for r in prob:
                if r != 0:
                    go_matrix[reward][used] = Decimal(go_matrix[reward][used]) + Decimal(theta) * Decimal(
                        prob[r]) * Decimal(get_matrix_value(matrix, reward - r, used - 1))
    return go_matrix


def update_matrix(matrix, theta, prob):
    if 0 not in prob:
        prob[0] = 0
    max_r = np.shape(matrix)[0] + max([r for r in prob]) - 1
    max_u = np.shape(matrix)[1] - 1
    stay_matrix = get_stay_matrix(matrix, max_r, max_u, prob, theta)
    go_matrix = get_go_matrix(matrix, max_r, max_u, prob, theta)
    # print_matrix(new_matrix)
    return np.add(stay_matrix, go_matrix)


def update_theta(matrix, theta):
    prb = Decimal(0)
    max_u = np.shape(matrix)[1] - 1
    max_r = np.shape(matrix)[0] - 1
    for reward in range(max_r):
        for used in range(max_u):
            prb += Decimal(get_matrix_value(matrix, reward, used))
    return Decimal(theta * (1 - prb))


def get_tot_reward(matrices):
    sum = Decimal(0)
    for m in matrices:
        u_max = len(m[0]) - 1
        for r in range(len(m)):
            for u in range(u_max + 1):
                sum += Decimal(get_matrix_value(m, r, u) * r)
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
