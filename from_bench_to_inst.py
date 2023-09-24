import math
import os
import random
import numpy as np
from generator import Generator
import os


class BenchToMapGenerator(Generator):

    def __init__(self, path, type, name):
        source=os.path.basename(path).split('.')[
            0]
        super().__init__(name, type, 100, 100, 2, 10, source=source)
        self.file = open(path)
        self.lines = [line for line in self.file]
        self.rows = int(self.lines[1].split(" ")[1])
        self.cols = int(self.lines[2].split(" ")[1])
        self.map = self.extract_map()
        self.FACTOR = 4
        self.reduce_map()
        self.unpassable = self.get_unpassable()
        self.name = '_' + str(self.rows) + "X" + str(self.cols) + self.type + source + ".py"
        self.file.close()

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
    G = BenchToMapGenerator("maps/den101d.map", type, "den101")
    f = open("ready_maps/" + G.name, "w")
    G.gen_map(f)
    f.close()
