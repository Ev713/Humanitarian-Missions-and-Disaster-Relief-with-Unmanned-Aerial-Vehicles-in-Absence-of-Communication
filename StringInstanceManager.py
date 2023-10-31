import itertools

import Vertex
import Instance
import Agent


def to_string(inst, filepath=''):
    file = open(filepath +'/'+ inst.name + ".txt", mode='w')
    file.write(str(inst.name) + '\n')
    file.write(str(inst.horizon) + '\n')
    file.write(inst.source + '\n')
    for a in inst.agents:
        file.write('A' + '\n')
        file.write(str(a.number) + '\n')
        file.write(str(a.loc.number) + '\n')
        file.write(str(a.movement_budget) + '\n')
        file.write(str(a.utility_budget) + '\n')
    for v in inst.map:
        file.write('V' + '\n')
        file.write(str(v.number) + '\n')
        file.write('N' + '\n')
        for n in v.neighbours:
            file.write(str(n.hash()) + '\n')
        file.write('D' + '\n')
        for r in range(max(list(v.distribution.keys()))+1):
            if r not in v.distribution:
                file.write('0' + '\n')
            else:
                file.write(str(v.distribution[r]) + '\n')

def to_inst(filepath):
    file = open(filepath, mode='r')
    line_it = iter(file)
    name = next(line_it).strip()
    horizon = int(next(line_it).strip())
    source = next(line_it).strip()
    agents = []
    agents_locations = {}
    map = []
    map_map = {}
    neighbours_hashes = {}
    EOF = False
    while next(line_it).strip() == 'A':
        agent = Agent.Agent(None, None, None, None)
        agent.number = int(next(line_it).strip())
        agents_locations[agent.number] = int(next(line_it).strip())
        agent.movement_budget = int(next(line_it).strip())
        agent.utility_budget = int(next(line_it).strip())
        agents.append(agent)
    while True:
        vertex = Vertex.Vertex(int(next(line_it).strip()))
        neighbours_hashes[vertex] = []
        if not next(line_it).strip() == 'N':
            raise Exception('Instance encoded incorrectly!')
        while True:
            n = next(line_it).strip()
            if n == 'D':
                break
            neighbours_hashes[vertex].append(int(n))
        for r in itertools.count(start=0):
            next_line = next(line_it, 'EOF').strip()
            if next_line == 'V':
                break
            if next_line == 'EOF':
                EOF = True
                break
            vertex.distribution[r] = float(next_line)
        map.append(vertex)
        map_map[vertex.hash()] = vertex
        if EOF:
            for v in map:
                v.neighbours = [map_map[n_hash] for n_hash in neighbours_hashes[v]]
            for a in agents:
                a.loc = map_map[agents_locations[a.number]]
            return Instance.Instance(name, map, agents, horizon, source)
