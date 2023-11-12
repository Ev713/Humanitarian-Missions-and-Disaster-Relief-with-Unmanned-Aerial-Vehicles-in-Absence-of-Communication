# First networkx library is imported
# along with matplotlib
from turtle import pd
import math
import networkx as nx
import matplotlib.pyplot as plt

# Defining a Class
import numpy as np

import InstanceManager


class GraphVisualization:

    def __init__(self):
        # visual is a list which stores all
        # the set of edges that constitutes a
        # graph
        self.visual = []

    # addEdge function inputs the vertices of an
    # edge and appends it to the visual list
    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)

    # In visualize function G is an object of
    # class Graph given by networkx G.add_edges_from(visual)
    # creates a graph with a given list
    # nx.draw_networkx(G) - plots the graph
    # plt.show() - displays the graph
    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        plt.show()


def visualize(inst):
    G = nx.Graph()
    for i in range(len(inst.map)):
        for j in range(len(inst.map[i].neighbours)):
            G.add_edge(inst.map[i].number, inst.map[i].neighbours[j].number)
    nx.draw_planar(G, with_labels=True)
    plt.savefig("instance" + str(i) + ".png")
    plt.clf()


def determine_cols(inst):
    for v in inst.map:
        for n in v.neighbours:
            if v.number == n.number + 1 or v.number == n.number - 1:
                continue
            return abs(v.number - n.number)
    return 0


def vis_2(inst):
    '''n = int(inst.map[-1].name[1:])
    m = 1
    i = 1
    while(i * i <= n):
        if(n % i == 0):
            m = i
        i += 1
    i = 0
    length = len(inst.map)
    while inst.map[i+1] in inst.map[i].neighbours and i < length -1:
        i += 1
    m = i

    n /= m
'''
    m = inst.x_size

    x = []
    y = []

    average_reward = np.mean(np.array([v.get_avg_reward() for v in inst.map]))
    colors = [v.get_avg_reward() / average_reward for v in inst.map]

    for t in range(len(inst.map)):
        x += [int(inst.map[t].file_name[1:]) % m]
        y += [int(inst.map[t].file_name[1:]) // m]

    fig, ax = plt.subplots()
    ax.scatter(x, y, c=colors, cmap='RdYlGn_r')
    for t in range(len(inst.map)):
        ax.annotate(inst.map[t].number, (x[t], y[t]))

    plt.show()


def vis3(inst):
    cols = determine_cols(inst)
    rows = math.ceil(inst.map[-1].number / cols)
    color_map = [['#000000' for _ in range(cols)] for _ in range(rows)]
    fig, ax = plt.subplots()
    for v in inst.map:
        x, y = (v.number - 1) % cols, (v.number - 1) // cols
        maximum = max(list([max(list(v.distribution.keys())) for v in inst.map]))
        prob_of_something = 1 - v.distribution[0]
        distr_no_zero = v.distribution if prob_of_something == 0 else {r: v.distribution[r] / prob_of_something for r in
                                                                       v.distribution if r != 0}
        e = (maximum - sum([distr_no_zero[r] * r for r in distr_no_zero])) / maximum
        # color = (prob_of_something, 0, e)
        color = (prob_of_something * (1 - e), 0, prob_of_something * e)

        hex_color = "#{:02X}{:02X}{:02X}".format(int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
        try:
            color_map[y][x] = hex_color
        except:
            breakpoint()
        ax.add_patch(plt.Rectangle((x, y), 1, 1, color=hex_color))
    ax.set_aspect('equal')

    # Set axis limits
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)

    # Remove axis labels and ticks
    ax.set_xticks([])
    ax.set_yticks([])

    # Show the grid
    print(color_map)
    plt.savefig(inst.name+".png")
    plt.show()


vis3(StringInstanceManager.to_inst("DragonAge_encoded_instances/MT/i_133_2_32_MT_orz704d.txt"))
