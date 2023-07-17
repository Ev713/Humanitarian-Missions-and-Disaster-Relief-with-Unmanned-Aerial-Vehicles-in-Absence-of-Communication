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

import grid6X6_CORNERS
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
import grid2X2
import grid5X5 as map

NUMBER_OF_SIMULATIONS = 1000
JUMP = NUMBER_OF_SIMULATIONS / min(NUMBER_OF_SIMULATIONS, 100)


def mcts(def_inst, is_det=False):
    values = []
    root = Node.Node(None)
    if is_det:
        root.state = State.DetState(def_inst)
        instance = Instance.DetInstance(def_inst)
    else:
        instance = Instance.StochInstance(def_inst)
        root.state = instance.initial_state.copy()

    node = root
    for t in range(NUMBER_OF_SIMULATIONS):
        #    print(t)
        # selection
        while node.all_children_visited():
            node.times_visited += 1
            if not node.state.is_terminal():
                node = node.highest_uct_child(t) #, exp_rate=EXPLORATION_RATE)
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

        # backpropagation
        while True:
            node.value += rollout_reward
            if node is root:
                break
            node = node.parent
            rollout_reward *= 0.9

        # showing tree

        # root.get_tree()
        # checking mid-rewards
        if t % JUMP == 0:
            #print("simulation " + str(t))
            node1 = root
            while not node.state.is_terminal() and len(node1.children) != 0:
                node1 = node1.highest_value_child()
            if is_det:
                value = instance.reward(node1.state, NUM_OF_SIMS=1000)
            else:
                value = instance.reward(node1.state)
            values.append(value)
    # root.get_tree()
    # returning
    while not node.state.is_terminal():
        if not node.children:
            raise Exception("Note enough simulations. Increase number of simulations, lower the horizon ot try again.")
        node = node.most_visited_child()
        print(node.state)
        if is_det:
            print(instance.reward(node.state, NUM_OF_SIMS=1000))
        else:
            print(instance.reward(node.state))
    # print(values)
    print("---------------------------------------------------------------------------")
    return values


i = map.instance1
stoch = mcts(i, False)
det = mcts(i, True)

y1 = stoch
y2 = det

x1 = [JUMP * i for i in range(len(y1))]
x2 = [JUMP * (i + 1) for i in range(len(x1))]

plt.scatter(x1, y1)
plt.scatter(x2, y2)
plt.legend(["Stoch", 'Det'])
plt.show()
# matrix = MatricesFunctions.get_starting_matrix(a1, v1)
# matrix = MatricesFunctions.new_matrix(np.array([[0.1, 0.2, 0.3, 0.4]]), {0: 0.5, 1: 0.3, 2: 0.2}, 1)
# print(matrix)
