import os
import numpy as np

max_reward = 7


def gen_map(n, m, dense, num_agents, time_horizont):
    f.write("import Instance \nimport MCTS\n")
    total_map = []
    mountns = (np.random.rand(dense) * n * m).round()
    # f.write(mountns)
    map1 = []
    for i in range(n):
        for j in range(m):
            curr_num = i * n + j
            if (curr_num in mountns):
                continue
            map1 += ["vertex" + str(curr_num)]
            f.write("vertex" + str(curr_num) + " = Instance.Vertex(\"v" + str(curr_num) + "\")\n")

            rnd_sz = np.random.randint(1, 10)
            values = {}
            probs = np.random.rand(1, rnd_sz)
            probs[0][0] = 0.5
            probs /= probs.sum()
            for t in range(len(probs[0])):
                #ty = t
                ty = np.random.randint(0, max_reward)
                if(t == 0):
                    values[0] = probs[0][0]
                    continue
                if ty in values.keys():
                    values[ty] += probs[0][t]
                else:
                    values[ty] = probs[0][t]

            f.write("vertex" + str(curr_num) + ".probability = ")
            f.write(str(values) + "\n")

    for i in range(n):
        for j in range(m):
            curr_num = i * n + j
            if (curr_num in mountns):
                continue
            if (curr_num in mountns):
                f.write("vertex" + str(curr_num) + ".neighbours = []\n")
            else:
                f.write("vertex" + str(curr_num) + ".neighbours = [")
                ngbrs = []
                if (i > 0 and ((curr_num - n) not in mountns)):
                    ngbrs += [curr_num - n]
                if (j > 0 and ((curr_num - 1) not in mountns)):
                    ngbrs += [curr_num - 1]
                if (i < n - 1 and ((curr_num + n) not in mountns)):
                    ngbrs += [curr_num + n]
                if (j < m - 1 and ((curr_num + 1) not in mountns)):
                    ngbrs += [curr_num + 1]
                for t in range(len(ngbrs)):
                    if (t < len(ngbrs) - 1):
                        f.write("vertex" + str(ngbrs[t]) + ", ")
                    else:
                        f.write("vertex" + str(ngbrs[t]))
                f.write("]\n")

    agents = []
    for i in range(num_agents):
        f.write("agent" + str(i) + " = Instance.Agent()\n")
        f.write("agent" + str(i) + ".location = vertex" + str(np.random.randint(0, n * m - 1)) + "\n")
        f.write("agent" + str(i) + ".movement_budget = " + str(time_horizont) + "\n")
        f.write("agent" + str(i) + ".utility_budget = " + str(round(np.random.randint(0, n * m))) + "\n")

        agents += ["agent" + str(i)]

    # f.write("map1 = " + *map1 +"\n")
    # f.write("agents = " + *agents+"\n")
    f.write("map1 = [")
    for i in range(len(map1)):
        if (i < len(map1) - 1):
            f.write(map1[i] + ",")
        else:
            f.write(map1[i])
    f.write("]\n")

    f.write("agents = [")
    for i in range(len(agents)):
        if (i < len(agents) - 1):
            f.write(agents[i] + ",")
        else:
            f.write(agents[i])
    f.write("]\n")

    f.write("instance1 = Instance.Instance(map1, agents, "+str(m)+", "+str(n)+")\n")

    #f.write("dumb = MCTS.monte_carlo_tree_search(instance1, 1000, True) \nsmart = MCTS.monte_carlo_tree_search(instance1, 1000, False) \nprint(\"Dumb:\", dumb)\nprint(\"Smart:\", smart)")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    for j in range(10):
        filename = "out"+str(j)+".py"
        for i in range(1):
            f = open(filename, "w")
            gen_map(j+5, j+5, int(j/4), int(j/4)+1, j+5)
            f.close()
        # os.system(filename)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
