# First networkx library is imported
# along with matplotlib
from turtle import pd

import networkx as nx
import matplotlib.pyplot as plt


# Defining a Class
import numpy as np


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
    G= nx.Graph()
    for i in range(len(inst.map)):
        for j in range(len(inst.map[i].neighbours)):
            G.add_edge(inst.map[i].name, inst.map[i].neighbours[j].name)
    nx.draw_planar(G, with_labels = True)
    plt.savefig("instance" + str(i) + ".png")
    plt.clf()

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
    colors = [v.get_avg_reward()/average_reward for v in inst.map]

    for t in range(len(inst.map)):
        x += [int(inst.map[t].name[1:]) % m]
        y += [int(inst.map[t].name[1:]) // m]

    fig, ax = plt.subplots()
    ax.scatter(x, y,c = colors, cmap='RdYlGn_r')
    for t in range(len(inst.map)):
        ax.annotate(inst.map[t].name, (x[t], y[t]))

    plt.show()
