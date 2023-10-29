import math
import os
from generator import Generator
import os
import StringInstanceManager
import Solver


class InstanceParser:

    def __init__(self, path, type, num_of_agents=None, horizon=None, factor=4):
        self.source = os.path.basename(path).split('.')[0]
        file = open(path)
        self.lines = [line for line in file]
        file.close()
        self.map = self.extract_map()
        self.rows = len(self.map)
        self.cols = len(self.map[0])
        self.reduce_map(factor)
        self.unpassable = []
        self.set_unpassable()
        self.num_of_agents = num_of_agents if num_of_agents is not None else self.get_num_of_agents()
        self.horizon = horizon if horizon is not None else self.rows + self.cols
        self.type = type

    def file_is_too_big(self):
        return self.get_map_size() > 300

    def get_map_size(self):
        size = self.rows * self.cols - len(self.unpassable)
        return size

    def get_num_of_agents(self):
        return max(1, int(self.rows / 5))

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

    def reduce_map(self, factor):
        new_map = []
        new_rows = math.floor(self.rows / factor)
        new_cols = math.floor(self.cols / factor)
        for i in range(new_rows):
            row = []
            for j in range(new_cols):
                c = self.map[math.floor(i * factor)][math.floor(j * factor)]
                row.append(c)
            new_map.append(row)
        self.map = new_map
        self.cols = new_cols
        self.rows = new_rows
        #print("Map size: ", self.get_map_size())
        #print("Reduced map:")
        #print(self.map_to_string())

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

    def set_unpassable(self):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] != '.':
                    self.unpassable.append(y * self.cols + x + 1)


for type in ['FR', 'MT']:
    for filename in os.scandir("DragonAge_maps"):
        if filename.is_file():
            parser = InstanceParser(filename, type)
            if not parser.file_is_too_big():
                print("Map size: ", parser.get_map_size())
                print("Reduced map:")
                print(parser.map_to_string())
                generated_instance = parser.gen_instance()
                StringInstanceManager.to_string(generated_instance, filepath="DragonAge_encoded_instances")
            # recoveredInstance = StringInstanceManager.to_inst("DragonAge_encoded_instances/"+generated_instance.name+'.txt')
            # solver = Solver.Solver()
            # solution = solver.det_mcts(recoveredInstance)
