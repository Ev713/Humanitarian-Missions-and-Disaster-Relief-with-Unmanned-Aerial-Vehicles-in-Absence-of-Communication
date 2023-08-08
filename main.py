import random

import Agent
import Instance
import DetInstance
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
import grid2X3
import grid4X4_SIMPLE as map
import grid5X5_CORNERS_SIMPLE
import grid5X5_SIMPLE
import grid6X6_CORNERS
import grid2X2
import grid5X5
import grid3X3_EMPTY
import grid6X6_EMPTY
import grid10X10
import grid4X4_EMPTY

NUMBER_OF_SIMULATIONS = 1000
JUMP = NUMBER_OF_SIMULATIONS / min(NUMBER_OF_SIMULATIONS, 100)
DISCOUNT = 1


def zero(state):
    return 0


class Solver:
    def __init__(self):
        self.type = None
        self.dup_det = False

    def bfs(self, def_inst):
        return self.bnb(def_inst, zero)

    def bnb(self, def_inst, heur):
        root = Node.Node(None)
        best_node = root
        instance = self.make_instance(def_inst)
        root.state = instance.initial_state.copy()
        que = [root]
        visited_states = set()
        num_of_states = 0
        while que:
            node = que.pop()

            best_value = instance.reward(node.state)
            if not node.state.is_terminal():
                node.expand([instance.make_action(action, node.state) for action in instance.actions(node.state)])
                for c in node.children:
                    num_of_states += 1
                    hash = c.state.hash()
                    if self.dup_det:
                        if hash in visited_states:
                            continue
                        visited_states.add(hash)
                    v = instance.reward(c.state)
                    if v+heur(c.state) < best_value:
                        continue
                    if v > best_value:
                        best_value = v
                        best_node = c
                    que.insert(0, c)
                    
        if self.dup_det:
            print("Checked states", len(visited_states))
        else:
            print("Number of states", num_of_states)
        return best_node.get_path()

    def make_instance(self, def_inst):
        if self.type == "U1D":
            instance = DetInstance.DetU1Instance(def_inst)
        elif self.type == "URD":
            instance = DetInstance.DetUisRInstance(def_inst)
        elif self.type == "U1S":
            instance = StochInstance.U1StochInstance(def_inst)
        elif self.type == "URS":
            instance = StochInstance.UisRStochInstance(def_inst)
        else:
            raise Exception("No recognised type!")
        return instance

    def mcts(self, def_inst):
        paths = []
        instance = None
        root = Node.Node(None)

        instance = self.make_instance(def_inst)

        root.state = instance.initial_state.copy()

        for t in range(NUMBER_OF_SIMULATIONS):

            node = root
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
                # print(str(round(t / NUMBER_OF_SIMULATIONS * 100, 2)) + "%")
                node = root
                while not node.state.is_terminal() and len(node.children) != 0:
                    node = node.highest_value_child()
                paths.append(node.get_path())
        # root.get_tree()
        # returning
        return paths

    def evaluate_path(self, def_inst, path, NUM_OF_SIMS=None):
        if self.type == "U1D":
            instance = DetInstance.DetU1Instance(def_inst)
            state = State.DetState(instance)
            state.path = path
            return instance.reward(state, NUM_OF_SIMS)
        if self.type == "U1S":
            instance = StochInstance.U1StochInstance(def_inst)
            state = instance.initial_state.copy()
            for t in range(1, len(list(path.values())[0])):
                action = {a: path[a][t] for a in path}
                state = instance.make_action(action, state)
            return instance.reward(state)
        if self.type == "URS":
            instance = StochInstance.UisRStochInstance(def_inst)
            state = instance.initial_state.copy()
            for t in range(1, len(list(path.values())[0])):
                action = {a: path[a][t] for a in path}
                state = instance.make_action(action, state)
            return instance.reward(state)
        else:
            raise Exception("No recognised type!")


def is_sorted_ascending(lst):
    return all(lst[i] <= lst[i + 1] for i in range(len(lst) - 1))


solver = Solver()
inst = map.instance1
inst.flybys = False
# solver.type = "U1S"
# stoch = solver.mcts(i)

solver.dup_det = True

solver.type = "URS"
bfs = solver.bfs(inst)
print("Best path found with bfs is: ", bfs)
print("Value of the best path found with bfs is: ", solver.evaluate_path(inst, bfs))

'''solver.type = "U1D"
det_u1 = solver.mcts(inst)
solver.type = "U1S"
stoch_u1 = solver.mcts(inst)
solver.type = "URS"
stoch_ur = solver.mcts(inst)
solver.type = "URD"
det_ur = solver.mcts(inst)

solver.type = "URS"
print("-------URS-------")
print(stoch_ur[-1])
print(solver.evaluate_path(inst, stoch_ur[-1]))
print("-------URD-------")
print(det_ur[-1])

print(solver.evaluate_path(inst, det_ur[-1]))
solver.type = "U1S"
print("-------U1S-------")
print(stoch_u1[-1])
print(solver.evaluate_path(inst, stoch_u1[-1]))
print("-------U1D-------")
print(det_u1[-1])
print(solver.evaluate_path(inst, det_u1[-1]))'''

# print("Deterministically calculated value of det:", solver.evaluate_path_by_simulations(i, det[-1], 10000))
# print("Stochastically calculated value of det:", solver.evaluate_path_with_matrices(i, det[-1]))
# print("Deterministically calculated value of stoch:", solver.evaluate_path_by_simulations(i, stoch[-1], 10000))
# print("Stochastically calculated value of stoch:", solver.evaluate_path_with_matrices(i, stoch[-1]))

# print("Best path found with matrices: ", stoch[-1])
# print("Best path found with simulations: ", det[-1])
# y1 = [solver.evaluate_path_with_matrices(i, path) for path in stoch]
# y2 = [solver.evaluate_path_with_matrices(i, path) for path in det]
# y3 = [solver.evaluate_path_by_simulations(i, path, 1000) for path in det]
# y4 = [solver.evaluate_path_by_simulations(i, path, 1000) for path in det]

# x1 = x2 = x3 = x4 = [JUMP * (j + 1) for j in range(len(y1))]

# plt.scatter(x1, y1)
# plt.scatter(x2, y2)
# plt.scatter(x3, y3)
# plt.scatter(x4, y4)
# only Stoch:
# plt.legend(["StochStoch", 'DetStoch'])  # , 'StochDet', 'DetDet'])
plt.show()
# matrix = MatricesFunctions.get_starting_matrix(a1, v1)
# matrix = MatricesFunctions.new_matrix(np.array([[0.1, 0.2, 0.3, 0.4]]), {0: 0.5, 1: 0.3, 2: 0.2}, 1)
# print(matrix)
