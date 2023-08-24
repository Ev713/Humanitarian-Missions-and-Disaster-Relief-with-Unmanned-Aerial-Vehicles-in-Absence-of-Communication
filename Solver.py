import random
import time

import DetInstance
import Node
import State
import StochInstance

import check_for_sasha as map

class Solution:
    def __init__(self, paths, timestamps, interrupted):
        self.paths = paths
        self.timestamps = timestamps
        self.rewards = []
        self.interrupted = interrupted

    def set_rewards(self, solver, inst):
        for p in self.paths:
            self.rewards.append(round(solver.evaluate_path(inst, p), 2))

class Solver:
    def __init__(self):
        self.type = None
        self.dup_det = False

        self.NUMBER_OF_SIMULATIONS = 5000
        self.JUMP = self.NUMBER_OF_SIMULATIONS / min(self.NUMBER_OF_SIMULATIONS, 100)
        self.DISCOUNT = 1
        self.timeout = 10

    def Heuristics_U1(self, state, instance):
        if self.type != 'U1S':
            raise Exception("U1S type required!")
        estimate_sum = 0
        for agent in instance.agents:
            current_vertex = state.a_pos[agent.hash()].loc
            winner_list = []
            for v in instance.map:
                if v.hash() == current_vertex or instance.distance[(v.hash(), current_vertex)] > (
                        agent.movement_budget - (instance.horizon - state.time_left)):
                    continue
                winner_list += [state.calculate_vertex_estimate(v, instance)]
            winner_list = sorted(winner_list, reverse=True)

            matrix = state.matrices[agent.hash()]
            ##print(matrix)
            for j in range(matrix.shape[0]):
                for k in range(matrix.shape[1] - 1):
                    for t in range(min(matrix.shape[1] - 1, len(winner_list) - k)):
                        estimate_sum += matrix[j][k] * winner_list[t]
            ##estimate_sum += state.calculate_estimate(winner_list[i])
        return estimate_sum

    def get_greedy_bound_UR(self, movement_budget, current_vertex, state, instance, used_vertex, probs):
        if movement_budget == 0:
            return 0
        if (len(probs) == 0):
            return 0
        winner_list = []
        for v in instance.map:
            if v.hash() == current_vertex or instance.distance[(v.hash(), current_vertex)] > (
                    movement_budget - (instance.horizon - state.time_left)):
                continue
            winner_list += [(state.calculate_vertex_estimate(v, instance), v.hash())]
            used_vertex[v.hash()] = 0
        winner_list = sorted(winner_list, reverse=True)
        i = 0
        while i < len(winner_list) and ([winner_list[i]][1] >= 1 or winner_list[i][0] >= len(probs)):
            i += 1
        if i == len(winner_list):
            return 0
        if (winner_list[i][0] >= len(probs)):
            return 0
        used_vertex[winner_list[i][1]] += probs[0]
        return winner_list[i][0] * probs[0] + self.get_greedy_bound_UR(movement_budget - 1, winner_list[i][1], state,
                                                                       instance, probs[round(winner_list[i][0]):])

    def Lower_bound_UR(self, state, instance):
        if self.type != 'URS':
            raise Exception("URS type required!")
        estimate_sum = 0
        used_vertex = {}
        for agent in instance.agents:
            current_vertex = state.a_pos[agent.hash()].loc
            winner_list = []
            for v in instance.map:
                if v.hash() == current_vertex or instance.distance[(v.hash(), current_vertex)] > (
                        agent.movement_budget - (instance.horizon - state.time_left)):
                    continue
                winner_list += [(state.calculate_vertex_estimate(v, instance), v.hash())]
                used_vertex[v.hash()] = 0
            winner_list = sorted(winner_list, reverse=True)

            matrix = state.matrices[agent.hash()]
            ##print(matrix)
            for j in range(matrix.shape[0]):
                for k in range(matrix.shape[1] - 1):
                    estimate_sum += self.get_greedy_bound_UR(
                        min(matrix.shape[1] - k, agent.movement_budget - (instance.horizon - state.time_left)),
                        current_vertex, state, instance, used_vertex, matrix[j][k:])
            ##estimate_sum += state.calculate_estimate(winner_list[i])
        return estimate_sum

    def get_greedy_bound_U1(self, movement_budget, current_vertex, state, instance, used_vertex, probs):
        if movement_budget == 0:
            return 0
        winner_list = []
        for v in instance.map:
            if v.hash() == current_vertex or instance.distance[(v.hash(), current_vertex)] > (
                    movement_budget - (instance.horizon - state.time_left)):
                continue
            winner_list += [(state.calculate_vertex_estimate(v, instance), v.hash())]
            used_vertex[v.hash()] = 0
        winner_list = sorted(winner_list, reverse=True)
        i = 0
        while i < len(winner_list) and used_vertex[winner_list[i][1]] >= 1:
            i += 1
        if i == len(winner_list):
            return 0
        used_vertex[winner_list[i][1]] += probs[0]
        return winner_list[i][0] * probs[0] + self.get_greedy_bound_U1(movement_budget - 1, winner_list[i][1], state,
                                                                       instance, used_vertex, probs[1:])

    def Lower_bound_U1(self, state, instance):
        if self.type != 'U1S':
            raise Exception("U1S type required!")
        estimate_sum = 0
        used_vertex = {}
        for agent in instance.agents:
            current_vertex = state.a_pos[agent.hash()].loc
            winner_list = []
            for v in instance.map:
                if v.hash() == current_vertex or instance.distance[(v.hash(), current_vertex)] > (
                        agent.movement_budget - (instance.horizon - state.time_left)):
                    continue
                winner_list += [(state.calculate_vertex_estimate(v, instance), v.hash())]
                used_vertex[v.hash()] = 0
            winner_list = sorted(winner_list, reverse=True)
            matrix = state.matrices[agent.hash()]
            ##print(matrix)
            for j in range(matrix.shape[0]):
                for k in range(matrix.shape[1] - 1):
                    estimate_sum += self.get_greedy_bound_U1(
                        min(matrix.shape[1] - k, agent.movement_budget - (instance.horizon - state.time_left)),
                        current_vertex,
                        state, instance, used_vertex, matrix[j][k:])
        return estimate_sum

    def bfs(self, def_inst):
        return self.branch_and_bound(def_inst)

    def branch_and_bound(self, def_inst, upper_bound=None, lower_bound=None):
        start = time.clock_gettime(time.CLOCK_THREAD_CPUTIME_ID)
        if self.type == 'URD' or self.type == 'U1D':
            raise Exception("Unfit type fro bfs")
        root = Node.Node(None)
        best_node = root
        instance = self.make_instance(def_inst)
        instance.calculate_distance_between_vertices()
        root.state = instance.initial_state.copy()
        que = [root]
        visited_states = set()
        num_of_states = 0
        best_value = instance.reward(root.state)
        while que:
            if time.clock_gettime(time.CLOCK_THREAD_CPUTIME_ID) - start > self.timeout:
                return Solution([best_node.get_path()], [round(time.clock_gettime(time.CLOCK_THREAD_CPUTIME_ID) - start, 3)], True)
            node = que.pop()
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

                    if upper_bound is not None:
                        up = upper_bound(c.state, instance)
                        low = lower_bound(best_node.state, instance) if lower_bound is not None else 0
                        if v + up < best_value + low:
                            continue
                    if v > best_value:
                        best_value = v
                        best_node = c
                    que = [c] + que

            if self.dup_det:
                pass  # print("Checked states", len(visited_states))
            else:
                pass  # print("Number of states", num_of_states)
        return Solution([best_node.get_path()], [time.clock_gettime(time.CLOCK_THREAD_CPUTIME_ID) - start], False)

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
        start = time.clock_gettime(time.CLOCK_THREAD_CPUTIME_ID)
        timestamps = []
        paths = []
        root = Node.Node(None)
        best_value = 0
        best_path = None

        instance = self.make_instance(def_inst)

        root.state = instance.initial_state.copy()

        for t in range(self.NUMBER_OF_SIMULATIONS):
            exec_time = time.clock_gettime(time.CLOCK_THREAD_CPUTIME_ID) - start
            if exec_time > self.timeout:
                return Solution(paths, timestamps, True)

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
            path = {a: [] for a in instance.agents_map}
            while not rollout_state.is_terminal():
                action = random.choice(instance.actions(rollout_state))
                for a in path:
                    path[a].append(action[a])
                rollout_state = instance.make_action(action, rollout_state)
            rollout_reward = instance.reward(rollout_state)
            if (self.type == 'U1S' or self.type == 'URS') and rollout_reward > best_value:
                best_value = rollout_reward
                best_path = path
            discounted_reward = rollout_reward * pow(self.DISCOUNT, node.depth)
            # backpropagation
            while True:
                node.value = max(node.value, discounted_reward)
                if node is root:
                    break
                node = node.parent
                discounted_reward /= self.DISCOUNT
            # checking mid-rewards
            if t % self.JUMP == 0 or t == self.NUMBER_OF_SIMULATIONS - 1:
                timestamps.append(round(time.clock_gettime(time.CLOCK_THREAD_CPUTIME_ID) - start, 3))
                if (self.type == 'U1S' or self.type == 'URS') and node.value < best_value:
                    paths.append(best_path)
                else:
                    # print(str(round(t / self.NUMBER_OF_SIMULATIONS * 100, 2)) + "%")
                    node = root
                    while not node.state.is_terminal() and len(node.children) != 0:
                        node = node.highest_value_child()
                    paths.append(node.get_path())
        # root.get_tree()
        # returning
        return Solution(paths, timestamps, False)

    def evaluate_path(self, def_inst, path, NUM_OF_SIMS=100000):
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
        if self.type == "URD":
            instance = DetInstance.DetUisRInstance(def_inst)
            state = instance.initial_state.copy()
            for t in range(1, len(list(path.values())[0])):
                action = {a: path[a][t] for a in path}
                state = instance.make_action(action, state)
            return instance.reward(state, NUM_OF_SIMS)
        else:
            raise Exception("No recognised type!")


def is_sorted_ascending(lst):
    return all(lst[i] <= lst[i + 1] for i in range(len(lst) - 1))


'''
solver = Solver()
inst = map.instance1
inst.flybys = True
# solver.type = "U1S"
# stoch = solver.mcts(i)

solver.dup_det = True



solver.type = "URD"
det = solver.mcts(inst)

path = {0: [State.Position( 1, False ), State.Position( 2, False ), State.Position( 3, False )],#, State.Position( 4, False ), State.Position( 5, False ), State.Position( 6, False )],
        1: [State.Position( 1, False ), State.Position( 2, False ), State.Position( 3, False )]}#, State.Position( 4, False ), State.Position( 5, False ), State.Position( 6, False )]}
print("Value of the best path found with det  is: ", solver.evaluate_path(inst, path))

solver.type = "URS"

print("Value of the best path found with bfs is: ", solver.evaluate_path(inst, path))

'''

'''solver.type = "U1D"

sam = solver.mcts(inst)
print("Best path found with det mcts is: ", sam[-1])
print("Value of the best path found with det mcts is: ", solver.evaluate_path(inst, sam[-1]))

solver.type = "U1D"
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
print(solver.evaluate_path(inst, det_u1[-1]))
'''
'''
# print("Deterministically calculated value of det:", solver.evaluate_path_by_simulations(i, det[-1], 10000))
# print("Stochastically calculated value of det:", solver.evaluate_path_with_matrices(i, det[-1]))
# print("Deterministically calculated value of stoch:", solver.evaluate_path_by_simulations(i, stoch[-1], 10000))
# print("Stochastically calculated value of stoch:", solver.evaluate_path_with_matrices(i, stoch[-1]))

# print("Best path found with matrices: ", stoch[-1])
# print("Best path found with simulations: ", det[-1])
# y1 = [solver.evaluate_path(i, path) for path in stoch]
# y2 = [solver.evaluate_path(i, path) for path in det]
# y3 = [solver.evaluate_path(i, path, 1000) for path in det]
# y4 = [solver.evaluate_path(i, path, 1000) for path in det]

# x1 = x2 = x3 = x4 = [JUMP * (j + 1) for j in range(len(y1))]

# plt.scatter(x1, y1)
# plt.scatter(x2, y2)
# plt.scatter(x3, y3)
# plt.scatter(x4, y4)
# only Stoch:
# plt.legend(["StochStoch", 'DetStoch'])  # , 'StochDet', 'DetDet'])
# plt.show()'''