import random

import Agent
import Instance
import MatricesFunctions
import Node
import State
import Vertex

NUMBER_OF_SIMULATIONS = 500


def mcts(def_inst, is_det=False):
    root = Node.Node(None)
    if is_det:
        root.state = State.DetState(def_inst)
        instance = Instance.DetInstance(def_inst)
    else:
        root.state = State.StochState(def_inst)
        instance = Instance.DetInstance(def_inst)

    node = root
    for t in range(NUMBER_OF_SIMULATIONS):

        # selection
        while node.is_fully_expanded() and not node.state.is_terminal:
            node = node.highest_uct_child(t)

        # expansion
        if not node.state.is_terminal():
            node.expand([instance.make_action(action, node.state) for action in instance.actions(node.state, t)])

        # simulation
        rollout_state = node.state.copy()
        while not rollout_state.is_terminal:
            action = random.choice(instance.actions(node.state))
            rollout_state = instance.make_action(action, rollout_state)
        rollout_reward = instance.reward(rollout_state)

        # backpropagation
        while True:
            node.value += rollout_reward
            node = node.parent
            if node is root:
                break

        # returning
        if is_det:
            while not node.state.is_terminal():
                node = node.highest_value_child()
        print(node.a_locs)


v1 = Vertex.Vertex(1)
v2 = Vertex.Vertex(2)
v3 = Vertex.Vertex(3)
v4 = Vertex.Vertex(4)

v1.neighbours = [v2, v3]
v2.neighbours = [v1, v4]
v3.neighbours = [v1, v4]
v4.neighbours = [v2, v3]

v1.distribution = {0: 1}
v2.distribution = {0: 0.5}
v1.distribution = {1: 0.5}
v1.distribution = {3: 0.5}

a1 = Agent.Agent(1, v1, 3, 3)
a2 = Agent.Agent(2, v1, 3, 3)

map = [v1, v2, v3, v4]
agents = [a1, a2]
i1 = Instance.Instance(map, agents, 3)
mcts(i1, True)
