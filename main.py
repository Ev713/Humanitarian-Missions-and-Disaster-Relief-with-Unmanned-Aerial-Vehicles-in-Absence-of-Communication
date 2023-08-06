import random

import Agent
import Instance
import Instances
import MatricesFunctions
import Node
import State
import Vertex
import StochInstance
from matplotlib import pyplot as plt
import numpy as np

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
import grid2X3 as map
import grid4X4_SIMPLE
import grid5X5_CORNERS_SIMPLE
import grid5X5_SIMPLE
import grid6X6_CORNERS
import grid2X2
import grid5X5
import grid3X3_EMPTY
import grid6X6_EMPTY
import grid10X10
import grid4X4_EMPTY

NUMBER_OF_SIMULATIONS = 10000
JUMP = NUMBER_OF_SIMULATIONS / min(NUMBER_OF_SIMULATIONS, 100)
DISCOUNT = 1

class Solver:
    def __init__(self):
        self.type = None

    def bfs(self, def_inst):
        root = Node.Node(None)
        instance = StochInstance.U1StochInstance(def_inst)
        root.state = instance.initial_state.copy()
        root.deep_expand(instance)
        node = root
        while not node.state.is_terminal() and len(node.children) != 0:
            node = node.highest_value_child()
        return node.get_path()

    def mcts(self, def_inst):
        paths = []
        root = Node.Node(None)
        if self.type == "D":
            root.state = State.DetState(def_inst)
            instance = Instance.DetInstance(def_inst)
        elif self.type == "U1S":
            instance = StochInstance.U1StochInstance(def_inst)
            root.state = instance.initial_state.copy()
        elif self.type == "UR":
            instance = StochInstance.UisRStochInstance(def_inst)
            root.state = instance.initial_state.copy()
        else:
            raise Exception("No recognised type")

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
            discounted_reward = rollout_reward * pow(DISCOUNT, node.depth)
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
            if t % JUMP == 0 or t == NUMBER_OF_SIMULATIONS - 1:
                #print(str(round(t / NUMBER_OF_SIMULATIONS * 100, 2)) + "%")
                node = root
                while not node.state.is_terminal() and len(node.children) != 0:
                    node = node.highest_value_child()
                paths.append(node.get_path())
        # root.get_tree()
        # returning
        return paths

    def evaluate_path(self, def_inst, path, NUM_OF_SIMS=None):
            if self.type=="D":
                instance = Instance.DetInstance(def_inst)
                state = State.DetState(instance)
                state.path = path
                return instance.reward(state, NUM_OF_SIMS)
            if self.type=="U1R":
                instance = StochInstance.U1StochInstance(def_inst)
                state = instance.initial_state.copy()
                for t in range(1, len(list(path.values())[0])):
                    action = {a: path[a][t] for a in path}
                    state = instance.make_action(action, state)
                return instance.reward(state)
            if self.type == "UR":
                instance = StochInstance.UisRStochInstance(def_inst)
                state = instance.initial_state.copy()
                for t in range(1, len(list(path.values())[0])):
                    action = {a: path[a][t] for a in path}
                    state = instance.make_action(action, state)
                return instance.reward(state)


def is_sorted_ascending(lst):
    return all(lst[i] <= lst[i + 1] for i in range(len(lst) - 1))

solver = Solver()
inst = map.instance1
inst.flybys = False
#solver.type = "U1S"
#stoch = solver.mcts(i)

solver.type = "UR"
stoch_ur = solver.mcts(inst)

#bfs = solver.bfs(i)
#print("Best path found with bfs is: ", bfs)
#print("Value of the best path found with bfs is: ", i.evaluate_path_with_matrices(bfs))

#solver.type = "D"
#det = solver.mcts(i)

for j in range(len(stoch_ur)):
    print(stoch_ur[j])
    print(solver.evaluate_path(inst, stoch_ur[j]))
    print("-----------------")

#print("Deterministically calculated value of det:", solver.evaluate_path_by_simulations(i, det[-1], 10000))
#print("Stochastically calculated value of det:", solver.evaluate_path_with_matrices(i, det[-1]))
#print("Deterministically calculated value of stoch:", solver.evaluate_path_by_simulations(i, stoch[-1], 10000))
#print("Stochastically calculated value of stoch:", solver.evaluate_path_with_matrices(i, stoch[-1]))

#print("Best path found with matrices: ", stoch[-1])
#print("Best path found with simulations: ", det[-1])
#y1 = [solver.evaluate_path_with_matrices(i, path) for path in stoch]
#y2 = [solver.evaluate_path_with_matrices(i, path) for path in det]
#y3 = [solver.evaluate_path_by_simulations(i, path, 1000) for path in det]
#y4 = [solver.evaluate_path_by_simulations(i, path, 1000) for path in det]

#x1 = x2 = x3 = x4 = [JUMP * (j + 1) for j in range(len(y1))]

#plt.scatter(x1, y1)
#plt.scatter(x2, y2)
#plt.scatter(x3, y3)
#plt.scatter(x4, y4)
# only Stoch:
#plt.legend(["StochStoch", 'DetStoch'])  # , 'StochDet', 'DetDet'])
plt.show()
# matrix = MatricesFunctions.get_starting_matrix(a1, v1)
# matrix = MatricesFunctions.new_matrix(np.array([[0.1, 0.2, 0.3, 0.4]]), {0: 0.5, 1: 0.3, 2: 0.2}, 1)
# print(matrix)
