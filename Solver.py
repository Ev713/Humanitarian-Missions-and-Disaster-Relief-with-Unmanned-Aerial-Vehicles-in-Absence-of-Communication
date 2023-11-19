import math
import random
import time

import numpy
import numpy as np

import DetInstance
import Node
import State
import StochInstance
from numpy import array as matrix

# import check_for_sasha as map
import InstanceManager
import instance_decoder


class Solution:
    def __init__(self, paths, timestamps, states_collector, interrupted, opened_nodes):
        self.paths = paths
        self.timestamps = timestamps
        self.states_collector = states_collector
        self.rewards = []
        self.interrupted = interrupted
        self.states = opened_nodes

    def set_rewards(self, solver, inst):
        instance = solver.make_instance(inst)
        for p in self.paths:
            emp_reward = round(solver.evaluate_path(instance, p, emp=True, NUM_OF_SIMS=50000), 5)
            mat_reward = round(solver.evaluate_path(instance, p), 5)
            print('empirically evaluated reward: ', emp_reward)
            print('reward evaluated with matrices : ', mat_reward)
            print('----------')
            self.rewards.append(round(solver.evaluate_path(instance, p), 2))


class Solver:
    def __init__(self):
        self.dist_calculated = False
        self.all_pair_distances = {}
        self.num_of_states = None
        self.type = None
        self.dup_det = False
        self.prev_time_check = 0

        self.NUMBER_OF_SIMULATIONS = 5000
        self.JUMP = self.NUMBER_OF_SIMULATIONS / min(self.NUMBER_OF_SIMULATIONS, 100)
        self.DISCOUNT = 1
        self.timeout = 60
        self.start = 0

        self.root = None

        # log variables
        self.timestamps = []
        self.paths = []
        self.states_collector = []

        self.best_node = None
        self.best_value = 0
        self.states = 0
        self.map_reduced = False

    def restart(self):
        self.start = time.clock_gettime(time.CLOCK_THREAD_CPUTIME_ID)
        self.prev_time_check = self.start
        self.timestamps = []
        self.paths = []
        self.root = Node.Node(None)
        self.best_node = self.root
        self.best_value = 0
        self.num_of_states = 0
        self.states_collector = []

    def get_time(self):
        return time.clock_gettime(time.CLOCK_THREAD_CPUTIME_ID) - self.start

    def time_for_log(self):
        now = time.clock_gettime(time.CLOCK_THREAD_CPUTIME_ID)
        if self.prev_time_check - self.start == 0 or now - self.prev_time_check > self.timeout / 100:
            # print("time total: ", now-self.start, " time skip:", now-self.prev_time_check)
            self.prev_time_check = now
            self.timestamps.append(now)
            return True
        return False

    def is_timeout(self):
        return self.get_time() > self.timeout

    def get_solution(self, timeout):
        self.paths.append(self.best_node.get_path())
        self.states_collector.append(self.num_of_states)
        return Solution(self.paths, self.timestamps, self.states_collector, timeout, self.num_of_states)

    def base_upper_bound(self, state, instance):
        possible_destinations_expectations = {}
        for agent in instance.agents:
            current_vertex = state.a_pos[agent.hash()].loc
            for v in instance.map:
                if v.hash() == current_vertex or self.all_pair_distances[(v.hash(), current_vertex)] > (
                        agent.movement_budget - (instance.horizon - state.time_left)):
                    continue
                possible_destinations_expectations[v.hash()] = v.expectation()
        max_visits = sum([agent.movement_budget - (instance.horizon - state.time_left) for agent in instance.agents])
        best_vertices = [k[0] for k in sorted(possible_destinations_expectations.items(), key=lambda item: item[1])][
                        0:max_visits - 1:]
        return sum([possible_destinations_expectations[v] for v in best_vertices])

    def calculate_all_pairs_distances_with_Seidel(self, inst):
        self.all_pair_distances = InstanceManager.calculate_all_pairs_distances_with_Seidel(inst)
        self.dist_calculated = True

    def get_greedy_bound_U1(self, movement_budget, current_vertex, state, instance, used_vertex, probs):
        if movement_budget == 0:
            return 0
        winner_list = []
        for v in instance.map:
            if v.hash() == current_vertex or self.all_pair_distances[(v.hash(), current_vertex)] > (
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

    def lower_bound_base_plus_utility(self, state, instance):
        vertexes_with_agents = []
        for agent in instance.agents:
            vertexes_with_agents.append(state.a_pos[agent.hash()].loc)
        reachable_vertexes = []
        for v in instance.map:
            for cur in vertexes_with_agents:
                if (self.all_pair_distances[v.hash(), cur] <= (
                        instance.horizon - state.time_left) and v not in reachable_vertexes):
                    reachable_vertexes.append(v)
        estimated_utility_left = 0
        for agent in instance.agents:
            matrix = state.matrices[agent.hash()]
            for i in range(matrix.shape[0]):
                for j in range(matrix.shape[1]):
                    estimated_utility_left += (matrix.shape[0] - i) * matrix[i][j]
        possible_rewards = []
        for v in reachable_vertexes:
            possible_rewards.append(v.expectation())
        possible_rewards = sorted(possible_rewards)
        return sum(possible_rewards[:min(len(possible_rewards), math.ceil(estimated_utility_left))])

    def upper_bound_base_plus_utility(self, state, instance):
        vertexes_with_agents = []
        for agent in instance.agents:
            vertexes_with_agents.append(state.a_pos[agent.hash()].loc)
        reachable_vertexes = []
        for v in instance.map:
            for cur in vertexes_with_agents:
                if (self.all_pair_distances[v.hash(), cur] <= (
                        instance.horizon - state.time_left) and v not in reachable_vertexes):
                    reachable_vertexes.append(v)
        estimated_utility_left = 0
        for agent in instance.agents:
            matrix = state.matrices[agent.hash()]
            for i in range(matrix.shape[0]):
                for j in range(matrix.shape[1]):
                    estimated_utility_left += (matrix.shape[0] - i) * matrix[i][j]
        possible_rewards = []
        for v in reachable_vertexes:
            possible_rewards.append(v.expectation())
        possible_rewards = sorted(possible_rewards, reverse=True)
        return sum(possible_rewards[:min(len(possible_rewards), math.ceil(estimated_utility_left))])

    def map_reduce(self, inst):
        InstanceManager.map_reduce(inst)
        self.map_reduced = True

    def bfs(self, def_inst):
        return self.branch_and_bound(def_inst)

    def branch_and_bound(self, def_inst, upper_bound=None, lower_bound=None):
        self.restart()
        self.type = 'U1S'
        self.root = Node.Node(None)
        self.best_node = self.root
        instance = self.make_instance(def_inst)
        if upper_bound is not None or lower_bound is not None:
            self.calculate_all_pairs_distances_with_Seidel(instance)
            if not self.dist_calculated:
                print("Calculating distances failed")
                return self.get_solution(True)

        self.root.state = instance.initial_state.copy()
        que = [self.root]
        visited_states = set()
        self.num_of_states = 0
        self.best_value = instance.reward(self.root.state)
        self.prev_time_check = self.start

        while que:
            if self.is_timeout():
                return self.get_solution(True)
            if self.time_for_log():
                self.paths.append(self.best_node.get_path())
                self.states_collector.append(self.num_of_states)
            node = que.pop()
            if not node.state.is_terminal():
                node.expand([instance.make_action(action, node.state) for action in instance.actions(node.state)])
                for c in node.children:
                    if self.is_timeout():
                        return self.get_solution(True)
                    if self.time_for_log():
                        self.paths.append(self.best_node.get_path())
                        self.states_collector.append(self.num_of_states)

                    hash = c.state.hash()
                    if self.dup_det:
                        if hash in visited_states:
                            continue
                        visited_states.add(hash)
                    self.num_of_states += 1
                    v = instance.reward(c.state)

                    if upper_bound is not None:
                        up = upper_bound(c.state, instance)
                        low = 0 if lower_bound is None else lower_bound(self.best_node.state, instance)
                        if v + up < self.best_value + low:
                            continue
                    if v > self.best_value:
                        self.best_value = v
                        self.best_node = c
                    que = [c] + que
        return self.get_solution(False)

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

    def det_mcts(self, inst):
        self.type = 'U1D'
        return self.mcts(inst)

    def stoch_mcts(self, inst):
        self.type = 'U1S'
        return self.mcts(inst)

    def mcts(self, def_inst):
        self.restart()
        instance = self.make_instance(def_inst)
        self.root.state = instance.initial_state.copy()
        best_value = 0
        best_path = None

        for t in range(self.NUMBER_OF_SIMULATIONS):
            if self.is_timeout():
                return self.get_solution(True)
            node = self.root
            # selection
            path = {a: [] for a in instance.agents_map}

            while node.all_children_visited():
                node.times_visited += 1
                if not node.state.is_terminal():
                    node = node.highest_uct_child(t)
                    for a in path:
                        if self.type == 'U1S':
                            action = node.state.a_pos[a]
                        else:
                            first_none = 0
                            while node.state.path[a][first_none] is not None:
                                first_none += 1
                            action = {a: node.state.path[a][first_none-1] for a in path}
                        path[a].append(action)
                else:
                    break

            # expansion
            if not node.children and not node.state.is_terminal():
                node.expand([instance.make_action(action, node.state) for action in instance.actions(node.state)])

            if node.children:
                node.times_visited += 1
                node = node.pick_unvisited_child()
                for a in path:
                    if self.type == 'U1S':
                        action = node.state.a_pos[a]
                    else:
                        first_none = 0
                        while node.state.path[a][first_none] is not None:
                            first_none += 1
                        action = node.state.path[a][first_none - 1]
                    path[a].append(action)
                self.num_of_states += 1

            node.times_visited += 1

            # simulation
            rollout_state = node.state.copy()

            while not rollout_state.is_terminal():
                action = random.choice(instance.actions(rollout_state))
                for a in path:
                    path[a].append(action[a])
                rollout_state = instance.make_action(action, rollout_state)
            rollout_reward = instance.reward(rollout_state)

            # Deterministic approach allows us to memorize the best path
            if self.type == 'U1S' and rollout_reward > best_value:
                best_value = rollout_reward
                best_path = path

            discounted_reward = rollout_reward * pow(self.DISCOUNT, node.depth)

            # backpropagation
            while True:
                if self.type == 'U1D' and (not node.all_children_visited() or node.state.is_terminal()):
                    avg_of_node = (node.value*node.times_visited+discounted_reward)/(node.times_visited+1)
                    node.value = avg_of_node
                    discounted_reward = avg_of_node
                else:
                    if node.value < discounted_reward:
                        node.value = discounted_reward
                    else:
                        break
                if node is self.root:
                    break
                node = node.parent
                discounted_reward /= self.DISCOUNT

            # gathering data
            if self.time_for_log():
                print(instance.name+" logging")
                self.states_collector.append(self.num_of_states)
                # Deterministic approach allows us to takeout the best path without checking
                if self.type == 'U1S':
                    self.paths.append(best_path)
                else:
                    node = self.root
                    while not node.state.is_terminal() and len(node.children) != 0:
                        node = node.highest_value_child()
                    self.paths.append(node.get_path())
                self.states_collector.append(self.num_of_states)
        # root.get_tree()
        # returning
        return self.get_solution(False)

    def evaluate_path(self, def_inst, path, NUM_OF_SIMS=100000, emp=False):
        if path is None:
            return 0
        if emp:
            self.type = "U1D"
            instance = self.make_instance(def_inst)
            state = instance.initial_state.copy()
            for a in path:
                for t in range(len(path[a])):
                    state.path[a][t+1] = path[a][t]
                    state.time_left -= 1
            state.path = path
            return instance.reward(state, NUM_OF_SIMS)
        else:
            self.type = 'U1S'
            instance = self.make_instance(def_inst)
            state = instance.initial_state.copy()
            for t in range(0, len(list(path.values())[0])):
                action = {a: path[a][t] for a in path}
                state = instance.make_action(action, state)
            reward = instance.reward(state)
            return reward


''' def find_bug(self, inst, path, rollout_reward, rolloutstates):
            r = self.evaluate_path(inst, path)
            if r != rollout_reward:
                instance = self.make_instance(inst)
                states = [None]
                states[0] = instance.initial_state.copy()
                for t in range(0, len(list(path.values())[0])):
                    action = {a: path[a][t] for a in path}
                    states.append(instance.make_action(action, states[-1]))
                reward = instance.reward(states[-1])
                for i in range(min(len(states), len(rolloutstates))):
                    for m in range(len(states[i].matrices)):
                        if np.array_equal(states[i].matrices[m], rolloutstates[i].matrices[m]):
                            breakpoint()'''


def is_sorted_ascending(lst):
    return all(lst[i] <= lst[i + 1] for i in range(len(lst) - 1))


def do():
    solver = Solver()
    inst = instance_decoder.instances[10]
    inst.flybys = True
    solver.type = "U1S"
    solver.map_reduce(inst)
    bnb = solver.branch_and_bound(inst, solver.base_upper_bound)
    bnbl = solver.branch_and_bound(inst, solver.base_upper_bound, solver.Lower_bound_U1)
    breakpoint()
    # solver.dup_det = True


# do()

#
# solver.type = "URD"
# det = solver.mcts(inst)

# path = {0: [State.Position( 1, False ), State.Position( 2, False ), State.Position( 3, False )],#, State.Position( 4, False ), State.Position( 5, False ), State.Position( 6, False )],
#        1: [State.Position( 1, False ), State.Position( 2, False ), State.Position( 3, False )]}#, State.Position( 4, False ), State.Position( 5, False ), State.Position( 6, False )]}
# print("Value of the best path found with det  is: ", solver.evaluate_path(inst, path))

# solver.type = "URS"

# print("Value of the best path found with bfs is: ", solver.evaluate_path(inst, path))


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
