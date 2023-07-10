import random
import time
from decimal import *
import default_instance

import Inst_visualizer
import Instance
import matplotlib
from matplotlib import pyplot as plt


def check_valuing_diff(i):
    for _ in range(60):
        path = i.return_random_path()
        for hor in range(1, len(path)):
            path_shorter = [path[i] for i in range(hor)]
            dumb_value = i.value(path_shorter, True, 10000)
            smart_value = i.value(path_shorter, False)
            print(smart_value - dumb_value)
        print("********************")


def get_avg_lists_of_lists(lst_of_lsts):
    avg_lst = []
    for i in range(len(lst_of_lsts[0])):
        avg_lst.append((sum([lst[i] for lst in lst_of_lsts])) / len(lst_of_lsts))
    return avg_lst


def check_visualiser(instances):
    for i in range(len(instances)):
        Inst_visualizer.vis_2(instances[i])


def full_scan():
    for i in range(len(instances)):
        print("Instance: " + str(i))
        dumb = get_avg_lists_of_lists([MCTS.monte_carlo_tree_search(instances[i], NUM_OF_SIMS, True, JUMP)
                                       for _ in range(AVERAGE_OF)])
        print("Finished counting dum-dums!")
        smart = get_avg_lists_of_lists([MCTS.monte_carlo_tree_search(instances[i], NUM_OF_SIMS, False, JUMP)
                                        for _ in range(AVERAGE_OF)])
        print("Finished counting smarts!")

        x1 = [i + 20 * JUMP for i in range(len(dumb) - 20)]
        y1 = [dumb[i + 20] for i in range(len(dumb) - 20)]
        x2 = [i + 20 * JUMP for i in range(len(smart) - 20)]
        y2 = [smart[i + 20] for i in range(len(dumb) - 20)]
        plt.scatter(x1, y1)
        plt.scatter(x2, y2)
        plt.legend(["dumb", 'smart'])
        plt.savefig("goodies/instance" + str(i) + ".jpg")
        plt.show()


i15 = default_instance.instance15
NUM_OF_SIMS = 200
JUMP = 1
AVERAGE_OF = 200
full_scan()