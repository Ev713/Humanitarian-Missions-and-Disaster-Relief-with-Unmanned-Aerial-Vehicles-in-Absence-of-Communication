import math
import random
import time

import instance_decoder
from Timer import Timer

import EmpInstance
import Node
import VectorInstance

import InstanceManager
from GenQueue import PriorityQueue, RegularQueue, Stack


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
        self.visited_states = {}
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

    def log_if_needed(self, path=None, needed=False):
        now = self.timer.now()
        if needed or self.timer.duration_gt('log', self.timeout / self.num_of_logs, alt_now=now):
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

    def get_reachable_vertices(self, state, agent=None):
        if agent is None:
            agents = self.instance.agents
        else:
            agents = [agent]
        vertexes_with_agents = []
        for agent in agents:
            vertexes_with_agents.append(state.a_pos[agent.hash()].loc)
        reachable_vertexes = []
        for v in self.instance.map:
            for cur in vertexes_with_agents:
                if (self.all_pair_distances[v.hash(), cur] <= (
                        self.instance.horizon - state.time_left) and v not in reachable_vertexes):
                    reachable_vertexes.append(v)
        return reachable_vertexes

    def get_sum_est_utility(self, state):
        estimated_utility_left = 0
        for agent in self.instance.agents:
            matrix = state.matrices[agent.hash()]
            estimated_utility_left += self.get_est_utility(state, agent)
        return estimated_utility_left

    def get_est_utility(self, state, agent):
        estimated_utility_left = 0
        matrix = state.matrices[agent.hash()]
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                estimated_utility_left += (matrix.shape[0] - i) * matrix[i][j]
        return estimated_utility_left

    def get_reachable_exp_rewards(self, state):
        reachable_vertices = self.get_reachable_vertices(state)
        reachable_exps = []
        for v in reachable_vertices:
            reachable_exps.append(v.expectation())
        return reachable_exps

    def get_reachable_bers(self, state):
        reachable_vertices = self.get_reachable_vertices(state)
        reachable_bers = []
        for v in reachable_vertices:
            reachable_bers.append(v.bernoulli())
        return reachable_bers

    def upper_bound_base_plus_utility(self, state):
        reachable_bers = self.get_reachable_bers(state)
        est_utility = self.get_sum_est_utility(state)
        reachable_bers = sorted(reachable_bers, reverse=True)
        return sum(reachable_bers[:min(len(reachable_bers), math.ceil(est_utility))])

    def get_prob_utility_gt0(self, state, agent):
        return 1-sum(state.matrices[agent.hash()][:, - 1])

    def lower_bound_base_plus_utility(self, state):
        probs_u_not_0 = {agent: self.get_prob_utility_gt0(state, agent) for agent in self.instance.agents}
        reachables = {agent: self.get_reachable_vertices(state, agent) for agent in self.instance.agents}
        already_visited = set()
        lowerbound = 0
        agents = sorted(self.instance.agents, key=lambda a: probs_u_not_0[a], reverse=True)
        for agent in agents:
            bernoullis = {v.hash(): v.bernoulli() for v in reachables[agent] if v not in already_visited}
            if len(bernoullis) == 0:
                continue
            v = max([v for v in bernoullis], key=lambda v: bernoullis[v])
            already_visited.add(v)
            lowerbound += bernoullis[v]*probs_u_not_0[agent]
        return lowerbound

    def map_reduce(self):
        InstanceManager.map_reduce(self.instance)
        self.map_reduced = True

    def bfs(self):
        return self.branch_and_bound()

    def branch_and_bound(self, upper_bound=None, lower_bound=None, is_greedy=False, depth_first=False):
        want_print = False
        if upper_bound is not None or lower_bound is not None:
            self.calculate_all_pairs_distances_with_Seidel()
        self.restart()
        if want_print:
            self.timer.start("init")
        if is_greedy:
            que = PriorityQueue(self.root)
        else:
            que = RegularQueue(self.root)
            
        if is_greedy:
            que = PriorityQueue(self.root)
        elif astar:
            que = AstarQueue(self.root)
        elif depth_first:
            que = Stack(self.root)
        else:
            que = RegularQueue(self.root)

        if want_print:
            self.timer.end('init')
        while not que.is_empty():
            if self.is_timeout():
                if want_print:
                    print(str(self.timer))
                self.log_if_needed(needed=True)
                return self.get_results()
            self.log_if_needed()
            node = que.pop()
            if want_print:
                self.timer.end_from_last_end('pop')
            if not node.state.is_terminal():
                node.expand(
                    [self.instance.make_action(action, node.state) for action in self.instance.actions(node.state)])
                self.num_of_states += len(node.children)

                if want_print:
                    self.timer.end_from_last_end('expand')
                for child in node.children:

                    if self.dup_det:
                        if self.is_duplicate(child.state):
                            continue

                    if want_print:
                        self.timer.end_from_last_end("dup det")

                    child.value = self.instance.reward(child.state)

                    if child.value > self.best_value:
                        self.best_node = child
                        self.best_value = child.value

                    if upper_bound is not None:
                        child.high = upper_bound(child.state)
                        if child.high + child.value < self.best_node.value + self.best_node.low:
                            continue

                    if lower_bound is not None:
                        child.low = lower_bound(child.state)
                        if child.value + child.low > best_lower_bound.value + best_lower_bound.low:
                            best_lower_bound = child
                    if want_print:
                        self.timer.end_from_last_end('value games')
                    que.push(child)
                    if want_print:
                        self.timer.end_from_last_end('push')
        self.log_if_needed(needed=True)
        return self.get_results()

    def value_plus_upper_bound(self, state):
        return self.instance.reward(state) + self.upper_bound_base_plus_utility(state)

    def is_duplicate(self, state):
        if state.hash() not in self.visited_states or self.visited_states[state.hash()] > state.time_left:
            self.visited_states[state.hash] = state.time_left
            return False
        return True

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
                self.log_if_needed(best_path, needed=True)
                return self.get_results()
            self.log_if_needed(best_path)
            node = self.root
            # selection

            while node.children:
                node.times_visited += 1
                node = node.highest_uct_child(t)

            # expansion
            if not node.state.is_terminal():
                if len(node.children) > 0:
                    breakpoint()
                children = [self.instance.make_action(action, node.state) for action in
                            self.instance.actions(node.state)]
                random.shuffle(children)
                node.expand(children)
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

        # root.get_tree()
        # returning
        self.log_if_needed(best_path, needed=True)
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


if __name__ == "__main__":
    dec = instance_decoder.Decoder()
    dec.decode_reduced()
    inst = dec.instances[0]
    sol = Solver(inst)
    sol.timeout = 60
    res = sol.greedy_branch_and_bound()
