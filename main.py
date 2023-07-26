import random
import numpy as np
import Agent
import Instance
import Instances
import MatricesFunctions
import Node
import State
import Vertex
from matplotlib import pyplot as plt

import grid1X3_SIMPLE
import grid3X3_CORNERS_SIMPLE
import grid3X3_CORNERS
import grid1X3_CORNERS
import grid3X3_SIMPLE
import grid2X1_VERY_SIMPLE
import grid2X1_SIMPLE
import grid2X2_SIMPLE
import grid2X2_CORNERS
import grid2X3_CORNERS
import grid4X4_SIMPLE
import grid5X5_CORNERS_SIMPLE
import grid5X5_SIMPLE
import grid6X6_CORNERS
import grid2X2
import grid5X5
import grid3X3_EMPTY as map
import grid6X6_EMPTY
import grid10X10
import grid4X4_EMPTY

NUMBER_OF_SIMULATIONS = 100000
JUMP = NUMBER_OF_SIMULATIONS / min(NUMBER_OF_SIMULATIONS, 100)
DISCOUNT = 1


def mcts(def_inst, is_det=False):
    paths = []
    root = Node.Node(None)
    if is_det:
        root.state = State.DetState(def_inst)
        instance = Instance.DetInstance(def_inst)
    else:
        instance = Instance.StochInstance(def_inst)
        root.state = instance.initial_state.copy()

    node = root
    for t in range(NUMBER_OF_SIMULATIONS):

        # selection
        while node.all_children_visited():
            node.times_visited += 1
            if not node.state.is_terminal():
                node = node.highest_uct_child(t)  # , exp_rate=EXPLORATION_RATE)
            else:
                break

        # expansion
        if not node.children and not node.state.is_terminal():
            node.expand([instance.make_action(action, node.state) for action in instance.actions(node.state)])

        if node.children:
            node.times_visited += 1
            node = node.pick_unvisited_child()

        node.times_visited += 1

        # simulation
        rollout_state = node.state.copy()
        while not rollout_state.is_terminal():
            action = random.choice(instance.actions(rollout_state))
            rollout_state = instance.make_action(action, rollout_state)
        rollout_reward = instance.reward(rollout_state)
        discounted_reward = rollout_reward * pow(DISCOUNT,  node.depth)
        # backpropagation
        while True:
            node.value = max(node.value, discounted_reward)
            if node is root:
                break
            node = node.parent
            discounted_reward /= DISCOUNT

        # showing tree

        # root.get_tree()
        # checking mid-rewards
        if t % JUMP == 0 or t == NUMBER_OF_SIMULATIONS-1:
            print(str(round(t/NUMBER_OF_SIMULATIONS*100, 2))+"%")
            node = root
            while not node.state.is_terminal() and len(node.children) != 0:
                node = node.highest_value_child()
            paths.append(node.get_path())
    # root.get_tree()
    # returning
    return paths


def is_sorted_ascending(lst):
    return all(lst[i] <= lst[i + 1] for i in range(len(lst) - 1))


i = map.instance1
stoch = mcts(i, False)
det = mcts(i, True)

print("Deterministically calculated value of det:", i.evaluate_path_by_simulations(det[-1], 10000))
print("Stochastically calculated value of det:", i.evaluate_path_with_matrices(det[-1]))
print("Deterministically calculated value of stoch:", i.evaluate_path_by_simulations(stoch[-1], 10000))
print("Stochastically calculated value of stoch:", i.evaluate_path_with_matrices(stoch[-1]))

print("Best path found with matrices: ", stoch[-1])
print("Best path found with simulations: ", det[-1])
y1 = [i.evaluate_path_with_matrices(path) for path in stoch]
y2 = [i.evaluate_path_with_matrices(path) for path in det]
y3 = [i.evaluate_path_by_simulations(path, 1000) for path in det]
y4 = [i.evaluate_path_by_simulations(path, 1000) for path in det]


x1 = x2 = x3 = x4 = [JUMP * (i + 1) for i in range(len(y1))]

plt.scatter(x1, y1)
plt.scatter(x2, y2)
#plt.scatter(x3, y3)
#plt.scatter(x4, y4)
# only Stoch:
plt.legend(["StochStoch", 'DetStoch'])  # , 'StochDet', 'DetDet'])
plt.show()
# matrix = MatricesFunctions.get_starting_matrix(a1, v1)
# matrix = MatricesFunctions.new_matrix(np.array([[0.1, 0.2, 0.3, 0.4]]), {0: 0.5, 1: 0.3, 2: 0.2}, 1)
# print(matrix)
