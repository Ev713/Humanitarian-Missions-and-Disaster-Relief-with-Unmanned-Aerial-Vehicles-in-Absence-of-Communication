import math
import os
from generator import Generator
import os


class InstanceParser:

    def __init__(self, path, type, num_of_agents, horizon, name, factor=4):
        self.source = os.path.basename(path).split('.')[0]
        file = open(path)
        self.lines = [line for line in file]
        file.close()
        self.map = self.extract_map()
        self.FACTOR = factor
        self.reduce_map()
        self.rows = len(self.map)
        self.cols = len(self.map[0])
        self.unpassable = self.get_unpassable()
        self.num_of_agents = num_of_agents
        self.horizon = horizon
        self.type = type

    def gen_instance(self):
        gen = Generator(self.type, self.cols, self.rows,
                        self.num_of_agents, self.horizon, source=self.source, unpassable=self.unpassable)
        return gen.gen_instance()

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
        unpassable = []
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] != '.':
                    unpassable.append(y * self.cols + x + 1)
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
