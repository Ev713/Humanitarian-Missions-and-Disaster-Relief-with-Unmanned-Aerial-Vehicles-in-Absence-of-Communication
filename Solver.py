import math
import random

import instance_decoder
from Timer import Timer

import EmpInstance
import Node
import VectorInstance

import InstanceManager
from DataStructures import MaxPriorityQueue


def make_instance(def_inst, method='VEC'):
    if method == 'EMP':
        instance = EmpInstance.EmpInstance(def_inst)
    elif method == 'VEC':
        instance = VectorInstance.VectorInstance(def_inst)
    elif method == 'SEM':
        instance = EmpInstance.SemiEmpInstance(def_inst)
    else:
        raise Exception('Unrecognized type')
    return instance


def is_sorted_ascending(lst):
    return all(lst[i] <= lst[i + 1] for i in range(len(lst) - 1))


class Solver:
    def __init__(self, def_inst):
        self.def_inst = def_inst
        self.dist_calculated = False
        self.all_pair_distances = {}
        self.num_of_states = None
        self.dup_det = False

        self.NUMBER_OF_SIMULATIONS = 999999
        self.DISCOUNT = 1
        self.timeout = 0
        self.num_of_logs = 20
        self.root = None
        self.instance = make_instance(def_inst)

        self.best_node = None
        self.best_value = 0
        self.map_reduced = False

        self.timer = Timer()

    def restart(self):
        self.timer = Timer()
        self.timer.start('run')
        self.timer.start('log')
        self.root = Node.Node(None)
        self.root.state = self.instance.initial_state.copy()
        self.best_node = self.root
        self.best_value = self.instance.reward(self.root.state)
        self.num_of_states = 0

    def get_results(self):
        log = self.timer.logs['run']
        results = []
        for t in log:
            reward = round(self.evaluate_path(log[t][0]), 3)
            # reward_emp = round(self.evaluate_path(log[t][0], method='EMP'), 3)
            # if reward_emp != reward:
            #     breakpoint()
            results.append((reward, log[t][1], round(t, 3)))
        return tuple(results)

    def log_if_needed(self, path=None):

        now = self.timer.now()
        if self.timer.duration_gt('log', self.timeout / self.num_of_logs, alt_now=now):
            self.timer.restart('log', alt_now=now)
            best_is_none = self.best_node is None
            if best_is_none and path is None:
                self.best_node = self.root
                while not self.best_node.state.is_terminal() and len(self.best_node.children) != 0:
                    self.best_node = self.best_node.highest_value_child()
            # print(self.best_value)
            self.timer.log((self.best_node.get_path_actions() if path is None else path, self.num_of_states),
                           thing='run', alt_now=now)
            if best_is_none:
                self.best_node = None
            return True
        return False

    def is_timeout(self):
        return self.timer.duration_gt('run', self.timeout)

    def base_upper_bound(self, state):
        possible_destinations_expectations = {}
        for agent in self.instance.agents:
            current_vertex = state.a_pos[agent.hash()].loc
            for v in self.instance.map:
                if v.hash() == current_vertex or self.all_pair_distances[(v.hash(), current_vertex)] > (
                        agent.movement_budget - (self.instance.horizon - state.time_left)):
                    continue
                possible_destinations_expectations[v.hash()] = v.expectation()
        max_visits = sum([agent.movement_budget - (self.instance.horizon - state.time_left)
                          for agent in self.instance.agents])
        best_vertices = [k[0] for k in sorted(possible_destinations_expectations.items(), key=lambda item: item[1])][
                        0:max_visits - 1:]
        return sum([possible_destinations_expectations[v] for v in best_vertices])

    def calculate_all_pairs_distances_with_Seidel(self):
        self.all_pair_distances = InstanceManager.calculate_all_pairs_distances_with_Seidel(self.instance)
        self.dist_calculated = True

    def get_reachable_vertices(self, state):
        vertexes_with_agents = []
        for agent in self.instance.agents:
            vertexes_with_agents.append(state.a_pos[agent.hash()].loc)
        reachable_vertexes = []
        for v in self.instance.map:
            for cur in vertexes_with_agents:
                if (self.all_pair_distances[v.hash(), cur] <= (
                        self.instance.horizon - state.time_left) and v not in reachable_vertexes):
                    reachable_vertexes.append(v)
        return reachable_vertexes

    def get_possible_rewards_and_est_utilty(self, state):
        reachable_vertices = self.get_reachable_vertices(state)
        estimated_utility_left = 0
        for agent in self.instance.agents:
            matrix = state.matrices[agent.hash()]
            for i in range(matrix.shape[0]):
                for j in range(matrix.shape[1]):
                    estimated_utility_left += (matrix.shape[0] - i) * matrix[i][j]
        possible_rewards = []
        for v in reachable_vertices:
            possible_rewards.append(v.expectation())
        return possible_rewards, estimated_utility_left

    def upper_bound_base_plus_utility(self, state):
        possible_rewards, est_utility = self.get_possible_rewards_and_est_utilty(state)
        possible_rewards = sorted(possible_rewards, reverse=True)
        return sum(possible_rewards[:min(len(possible_rewards), math.ceil(est_utility))])

    def lower_bound_base_plus_utility(self, state):
        possible_rewards, est_utility = self.get_possible_rewards_and_est_utilty(state)
        possible_rewards = sorted(possible_rewards)
        return sum(possible_rewards[:min(len(possible_rewards), math.ceil(est_utility))])

    def map_reduce(self):
        InstanceManager.map_reduce(self.instance)
        self.map_reduced = True

    def bfs(self):
        return self.branch_and_bound()

    def branch_and_bound(self, upper_bound=None, lower_bound=None):
        # self.timer.start('init')
        if upper_bound is not None or lower_bound is not None:
            self.calculate_all_pairs_distances_with_Seidel()
            if not self.dist_calculated:
                print("Calculating distances failed")
                return self.get_results()

        self.restart()
        que = [self.root]
        visited_states = {}

        while que:
            if self.is_timeout():
                return self.get_results()
            self.log_if_needed()
            node = que.pop()
            if not node.state.is_terminal():
                node.expand(
                    [self.instance.make_action(action, node.state) for action in self.instance.actions(node.state)])
                self.num_of_states += len(node.children)
                for child in node.children:
                    # if self.is_timeout():
                    #    return self.get_results()
                    # self.log_if_needed()

                    key = child.state.hash()
                    if self.dup_det:
                        if key in visited_states:
                            if visited_states[key] < child.state.time_left:
                                continue
                        else:
                            visited_states[key] = child.state.time_left

                    v = self.instance.reward(child.state)

                    if v > self.best_value:
                        self.best_value = v
                        self.best_node = child

                    if upper_bound is not None:
                        up = upper_bound(child.state)
                        low = 0 if lower_bound is None else lower_bound(child.state)
                        if v + up < self.best_value + low:
                            continue
                    que.append(child)

        return self.get_results()

    def value_plus_upper_bound(self, state):
        return self.instance.reward(state) + self.upper_bound_base_plus_utility(state)

    def greedy_best_first_search(self, heuristic=value_plus_upper_bound):
        self.restart()
        nodes = MaxPriorityQueue()
        nodes.push(self.root)
        visited_states = set()
        self.calculate_all_pairs_distances_with_Seidel()
        while not nodes.is_empty():

            best_unexpanded_node = nodes.pop()
            best_unexpanded_node.expand([self.instance.make_action(action, best_unexpanded_node.state)
                                         for action in self.instance.actions(best_unexpanded_node.state)])
            for child in best_unexpanded_node.children:

                if self.is_timeout():
                    return self.get_results()
                self.log_if_needed()

                key = child.state.hash()
                if self.dup_det:
                    if key in visited_states:
                        continue
                    visited_states.add(key)
                self.num_of_states += 1
                child.value = heuristic(self, child.state)
                if self.instance.reward(child.state) > self.best_value:
                    self.best_value = child.value
                    self.best_node = child
                if not child.state.is_terminal():
                    nodes.push(child)
        return self.get_results()

    def emp_mcts(self):
        self.instance = make_instance(self.def_inst, method='EMP')
        return self.mcts('EMP')

    def vector_mcts(self):
        return self.mcts('VEC')

    def semi_emp_mcts(self):
        self.instance = make_instance(self.def_inst, method='SEM')
        return self.mcts('SEM')

    def mcts(self, method):
        self.restart()
        best_path = None
        self.best_node = None

        for t in range(self.NUMBER_OF_SIMULATIONS):
            if self.is_timeout():
                return self.get_results()

            node = self.root
            # selection

            while node.children:
                node.times_visited += 1
                node = node.highest_uct_child(t)

            # expansion
            if not node.state.is_terminal():
                if len(node.children) > 0:
                    breakpoint()
                node.expand(
                    random.shuffle([self.instance.make_action(action, node.state) for action in self.instance.actions(node.state)]))
                self.num_of_states += len(node.children)
                node.times_visited += 1
                node = node.children[0]

            # simulation
            node.times_visited += 1
            rollout_state = node.state.copy()
            if method == 'VEC':
                path = node.get_path_actions()

            while not rollout_state.is_terminal():
                action = random.choice(self.instance.actions(rollout_state))
                if method == 'VEC':
                    for a in path:
                        path[a].append(action[a])
                rollout_state = self.instance.make_action(action, rollout_state)
            rollout_reward = self.instance.reward(rollout_state)

            # Deterministic approach allows us to memorize the best path
            if method == 'VEC' and rollout_reward > self.best_value:
                self.best_value = rollout_reward
                best_path = path

            discounted_reward = rollout_reward * pow(self.DISCOUNT, node.depth)

            # backpropagation
            while True:
                if (not node.all_children_visited()) or node.state.is_terminal():
                    avg_of_node = (node.value * (node.times_visited - 1) + discounted_reward) / node.times_visited
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
            self.log_if_needed(best_path)

        # root.get_tree()
        # returning
        return self.get_results()

    def evaluate_path(self, path, method='VEC'):
        self.instance = make_instance(self.def_inst, method)
        if path is None:
            return 0
        state = self.instance.initial_state.copy()
        for t in range(len(list(path.values())[0])):
            action = {a: path[a][t] for a in path}
            state = self.instance.make_action(action, state)
        reward = self.instance.reward(state) if method == 'VEC' \
            else self.instance.average_of_sims(state, 10000)
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

if __name__ == "__main__":
    dec = instance_decoder.Decoder()
    dec.decode_reduced()
    inst = dec.instances[0]
    sol = Solver(inst)
    sol.timeout = 60
    res = sol.emp_mcts()

# solver.type = "URD"
# det = solver.mcts(inst)

# path = {0: [State.Position( 1, False ), State.Position( 2, False ), State.Position( 3, False )],#, State.Position(
# 4, False ), State.Position( 5, False ), State.Position( 6, False )], 1: [State.Position( 1, False ),
# State.Position( 2, False ), State.Position( 3, False )]}#, State.Position( 4, False ), State.Position( 5, False ),
# State.Position( 6, False )]} print("Value of the best path found with det  is: ", solver.evaluate_path(inst, path))

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
