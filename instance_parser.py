import Instance


def extract_map(file):
    map = []
    lines = [line for line in file]
    for line_index in range(len(lines)):
        if line_index < 4:
            continue
        row = []
        for x in range(len(lines[line_index])):
            char = lines[line_index][x]
            row.append(char)
        map.append(row)
    return map

def parse(filepath, type):
    file = open(filepath)
    map = extract_map(file)


