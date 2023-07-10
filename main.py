import random
import  numpy as np
import Agent
import Instance
import Instances
import MatricesFunctions
import Node
import State
import Vertex
from matplotlib import pyplot as plt

import grid

NUMBER_OF_SIMULATIONS = 10000
JUMP = NUMBER_OF_SIMULATIONS/10


def mcts(def_inst, is_det=False):
    values = []
    root = Node.Node(None)
    if is_det:
        root.state = State.DetState(def_inst)
        instance = Instance.DetInstance(def_inst)
    else:
        root.state = State.StochState(def_inst)
        instance = Instance.StochInstance(def_inst)

    node = root
    for t in range(NUMBER_OF_SIMULATIONS):
    #    print(t)
        # selection
        while node.all_children_visited():
            node.times_visited += 1
            if not node.state.is_terminal():
                node = node.highest_uct_child(t)
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
        print("simulation " + str(t))
        # root.get_tree()
        # checking mid-rewards
        if t > 0 and t % JUMP == 0:
            node1 = root
            while not node.state.is_terminal() and len(node1.children) != 0:
                node1 = node1.highest_value_child()
            value = instance.reward(node1.state)
            values.append(value)
    #root.get_tree()
    # returning
    while not node.state.is_terminal():
        if not node.children:
            raise Exception("Note enough simulations.")
        node = node.most_visited_child()
        print(node.state)
    #print(values)
    return values


i = grid.instance1
stoch = mcts(i, False)
det = mcts(i, True)

y1 = stoch
y2 = det

x1 = [JUMP * i for i in range(len(y1))]
x2 = [JUMP * (i+1) for i in range(len(x1))]

plt.scatter(x1, y1)
plt.scatter(x2, y2)
plt.legend(["Stoch", 'Det'])
plt.show()
# matrix = MatricesFunctions.get_starting_matrix(a1, v1)
# matrix = MatricesFunctions.new_matrix(np.array([[0.1, 0.2, 0.3, 0.4]]), {0: 0.5, 1: 0.3, 2: 0.2}, 1)
# print(matrix)
