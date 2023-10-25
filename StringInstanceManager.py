def toString(Instance):
    file = open(Instance.name+".txt", mode='a')
    file.write(Instance.name)
    file.write(Instance.horizon)
    for a in Instance.agents:
        file.write('A')
        file.write(a.number)
        file.write(a.loc)
        file.write(a.movement_budget)
        file.write(a.utility_budget)
    for v in Instance.map:
        file.write('V')
        file.write(v.number)
        file.write('N')
        for n in v.neighbours:
            file.write(n.number)
        file.write('D')
        for r in range(len(v.distribution)):
            if r not in v.distribution:
                file.write('0')
            else:
                file.write(str(v.distribution[r]))