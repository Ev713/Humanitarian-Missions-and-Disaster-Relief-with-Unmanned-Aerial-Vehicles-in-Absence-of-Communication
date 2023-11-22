import math

import numpy as np
import Instance
import numpy


def shift_right(mtrx):
    matrix = mtrx.copy()
    shape = (matrix.shape[0], 1)
    zeros = numpy.zeros(shape)
    matrix = numpy.concatenate((zeros, matrix), axis=1)
    matrix = numpy.delete(matrix, matrix.shape[1] - 1, axis=1)
    return matrix


def shift_down(mtrx, x):
    matrix = mtrx.copy()
    zeros = numpy.zeros((x, matrix.shape[1]))
    matrix = numpy.concatenate((zeros, matrix), axis=0)
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


def add_zeros_to_bottom(mtrx, x):
    matrix = mtrx.copy()
    for _ in range(x):
        shape = (1, matrix.shape[1])
        zeros = np.zeros(shape)
        matrix = np.concatenate((matrix, zeros))
    return matrix


def add_diff_height_mtrxs(mtrx1, mtrx2):
    height_diff = abs(mtrx2.shape[0] - mtrx1.shape[0])
    if mtrx1.shape[0] > mtrx2.shape[0]:
        return np.add(mtrx1, add_zeros_to_bottom(mtrx2, height_diff))
    return np.add(add_zeros_to_bottom(mtrx1, height_diff), mtrx2)


def new_matrix(mtrx, prob, theta):

    m_sum = round(np.sum(mtrx), 5)
    if m_sum != 1:
        raise Exception("Input matrix is invalid, sum is: "+str(m_sum))
    if sum(list(prob.values())) != 1:
        raise Exception("Distribution of a vertex is invalid")

    if 0 not in prob:
        prob[0] = 0

    # Theta represents the probability that the vertex has not been visited by an agent with non-zero utility
    # in which case the vertex is definitely empty; at the start it is always 1.
    # Therefore, at this point the new matrix represents the probability
    # that the agent did not spend any of its utility because another drone has already done it in that vertex.
    # If that matrix is zero, no agent has visited this vertex (or the original matrix was zero).

    updated_matrix = (1 - theta) * mtrx.copy()

    # R-matrix represents the case in which there is reward r in the vertex.
    # The assumptions that we are making is that:
    #   a. The reward in the vertex is indeed r, which happens with probability p.
    #   b. The vertex has not been visited by another agent which happens with probability theta.
    # Under those assumptions, the effect on the matrix would be a shift to right by one that represents that
    # the utility spent by the agent has risen by one (if r is not zero) and a shift down by r which means
    # that reward collected by the agent has risen by r (note that the right-most column doesn't move since if
    # there is no utility left in agent it doesn't collect the reward). Note that if r is zero than r-matrix is just
    # the copy of the original. Also note the sum of values in the r-matrix is the same as in the original matrix
    # and is 1.

    u_left_zero = np.concatenate((np.zeros((mtrx.shape[0], mtrx.shape[1] - 1)),
                                  np.reshape(mtrx[:, - 1], (mtrx.shape[0], 1))), axis=1)
    # Probabilities that the utility left is zero are just the last column.
    # All the other values are filled with zeroes.

    u_spent1 = shift_right(mtrx)

    # The effect of spending one utility unit on the matrix would be a shift to the right which is the same
    # as removing the last column (which is not relevant because in that case we cannot spend utility, and so
    # we look at it as a separate case) and adding a column filled with zeros as the first column. The shape
    # of the matrix doesn't change.

    # The u_left_zero and u_spent1 are used in every iteration therefore we compute now, them outside the loop.

    for r in prob:
        p = prob[r]
        if p == 0:
            continue
        if r == 0:
            r_matrix = mtrx.copy()
        else:
            u_spent1_r_collected = shift_down(u_spent1, r)

            # The effect of collecting a reward that equals to r is just shifting the matrix down by r or adding r empty
            # rows to the upper part of the matrix.

            r_matrix = add_diff_height_mtrxs(u_left_zero, u_spent1_r_collected)

            if round(np.sum(r_matrix), 5) != 1:
                breakpoint()
                raise Exception("bug in computing r-matrix")

            # So, the r-matrix that we get from collecting reward r by using 1 utility unit is the sum
            # of the matrix that represents the possibility that the agent had no utility left and the matrix that
            # represents the possibility that we have actually used utility and collected reward.

        updated_matrix = add_diff_height_mtrxs(updated_matrix, p * theta * r_matrix)
    if round(np.sum(updated_matrix), 5) != 1:
        raise Exception("Bug in updating matrix")
    return updated_matrix


def update_theta(matrix, theta):
    return theta * sum(matrix[:, matrix.shape[1] - 1])


def get_matrices_reward(matrices):
    tot_reward = 0
    for a_hash in matrices:
        m = matrices[a_hash]
        for r in range(m.shape[0]):
            for u in range(m.shape[1]):
                tot_reward += m[r][u] * r
    return tot_reward

