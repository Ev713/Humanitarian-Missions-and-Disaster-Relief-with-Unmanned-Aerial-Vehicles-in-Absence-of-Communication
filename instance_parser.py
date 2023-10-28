import math
import os
import random
import numpy as np
from generator import Generator
import os


class InstanceParser():

    def __init__(self, path, type, num_of_agents, horizon, name, factor=4):
        source = os.path.basename(path).split('.')[0]
        file = open(path)
        self.lines = [line for line in file]
        file.close()
        self.map = self.extract_map()
        self.FACTOR = factor
        self.reduce_map()
        rows = len(self.map)
        cols = len(self.map[0])
        unpassable = self.get_unpassable()
        self.gen = Generator(type, cols, rows, num_of_agents, horizon, source=source, unpassable=unpassable)

    def get_inst(self):
        return self.gen.gen_instance()

    def map_to_string(self):
        string = ''
        for row in self.map:
            for char in row:
                if char == '.':
                    string += ' '
                else:
                    string += '■'
            string += '■\n'
        return string

    def generate_init_loc(self, agent_hash):
        while True:
            l = random.randint(1, self.rows * self.cols)
            if l not in self.unpassable:
                return l

    def reduce_map(self):
        factor = self.FACTOR
        new_map = []
        new_rows = math.floor(self.rows / factor)
        new_cols = math.floor(self.cols / factor)
        for i in range(new_rows):
            row = []
            for j in range(new_cols):
                c = self.map[math.floor(i * factor)][math.floor(j * factor)]
                row.append(c)
            new_map.append(row)
        print("Reduced map:")
        self.map = new_map
        self.cols = new_cols
        self.rows = new_rows

        print(self.map_to_string())

    def extract_map(self):
        map = []
        for line_index in range(len(self.lines)):
            if line_index < 4:
                continue
            row = []
            for x in range(len(self.lines[line_index])):
                char = self.lines[line_index][x]
                row.append(char)
            map.append(row)
        return map

    def get_unpassable(self):
        if not hasattr(self, 'map'):
            self.map = self.extract_map()
        unpassable = []
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] != '.':
                    unpassable.append(self.xy_to_num(x, y))
        return unpassable


for type in ['FR', 'MT']:
    G = InstanceParser("maps/den101d.map", type, "den101")
    f = open("ready_maps/" + G.name, "w")
    g = open("THIRD_instance_collector.py", "a")
    g.write("from ready_maps import " + G.name + "\n")
    g.write("instances.append(" + G.name + ".instance1)\n")
    g.close()

    G.gen_map(f)
    f.close()
