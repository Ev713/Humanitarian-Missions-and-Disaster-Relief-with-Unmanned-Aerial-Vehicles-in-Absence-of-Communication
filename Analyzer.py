import statistics

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math


# (inst.name, solver_type, algo, flybys)

class Run:
    def __init__(self):
        self.inst_name = None
        self.solver_type = None
        self.algo = None
        self.flybys = None
        self.results = None
        self.time = None
        self.fin_res = None
        self.states = 0
        self.map_type = None
        # self.is_real = False
        self.map_size = 0

    def is_timeout(self):
        return self.time == -1

    def inst_name_extract_type(self):
        if self.inst_name[0] == '_':
            ar_id = self.inst_name.find('AR')
            self.map_type = self.inst_name[ar_id - 2] + self.inst_name[ar_id - 1]
            self.is_real = True
        else:
            self.map_type = self.inst_name[-2] + self.inst_name[-1]
            self.is_real = False

    def copy(self):
        cp = Run()
        cp.inst_name = self.inst_name
        cp.time = self.time
        cp.solver_type = self.solver_type
        cp.algo = self.algo
        cp.flybys = self.flybys
        cp.results = self.results
        cp.fin_res = self.fin_res
        cp.map_type = self.map_type
        cp.is_real = self.is_real


class Instance_data:
    def __init__(self, inst_name, flybys, map_type):
        self.inst_name = inst_name
        self.flybys = flybys
        self.map_type = map_type
        self.BFS_time = None
        self.best_value = None
        self.BFS = None
        self.BNB = None
        self.MCTS_D = None
        self.MCTS_S = None

    def clone(self):
        cp = Instance_data(self.inst_name, self.flybys, self.map_type)
        self.BFS_time = None
        self.best_value = None
        self.BFS = None
        self.BNB = None
        self.MCTS = None

    def erase_unnescesarry_MCTS(self):
        new_res = []
        for r in self.MCTS.results:
            if r[1] > self.BFS_time:
                break
            new_res.append(r)
        self.MCTS.results = new_res


class Analyzer:
    def __init__(self):
        self.file_path = "data/NEW_no_preprocessing_tot.csv"
        self.df = pd.read_csv(self.file_path, header=None, on_bad_lines='skip')
        self.runs = []
        self.instances = {}

    def filter_inst(self, bfs_finished=None, mcts_s_more_than_percentage=None, mcts_d_more_than_percentage=None,
                    mcts_s_before_time=None, mcts_d_before_time=None):
        filtered_instances = []
        for i in list(self.instances.values()):
            if mcts_s_more_than_percentage is not None:
                if i.best_value == -1 or i.MCTS_S.results == -1:
                    continue
                try:
                    if mcts_s_before_time is None:
                        res = i.MCTS_S.fin_res
                    else:
                        id = 0
                        res = i.MCTS_S.results[0][1]
                        while (i.MCTS_S.results[id][1] < mcts_s_before_time and id < len(i.MCTS_S.results)):
                            res = i.MCTS_S.results[id][1]
                            id += 1
                except:
                    breakpoint()
                if res < i.best_value * mcts_s_more_than_percentage:
                    continue
            if mcts_d_more_than_percentage is not None:
                if i.best_value == -1:
                    continue
                if mcts_d_before_time is not None:
                    res = i.MCTS_D.fin_res
                else:
                    id = 0
                    res = i.MCTS_D.results[0][1]
                    while (i.MCTS_D.results[id][1] < mcts_d_before_time):
                        res = i.MCTS_D.results[id][1]
                        id += 1
                if res < i.best_value * mcts_d_more_than_percentage:
                    continue
            if bfs_finished == True:
                if i.best_value == -1:
                    continue
            filtered_instances.append(i)
        return filtered_instances

    def filter_runs(self, algo=None, solver_type=None, map_type=None, inst_name=None, finished=None,
                    time_less_than=None, reward_bigger_than=None):
        filtered_runs = []
        for r in self.runs:
            if algo is not None and r.algo != algo:
                continue
            if solver_type is not None and r.solver_type != solver_type:
                continue
            if map_type is not None and r.map_type != map_type:
                continue
            if inst_name is not None and r.inst_name != inst_name:
                continue
            if finished is not None:
                if (finished and r.time != -1) or (not finished and r.time == -1):
                    continue
            if time_less_than is not None and (r.time == -1 or r.time >= time_less_than):
                continue
            if reward_bigger_than is not None and r.fin_res < reward_bigger_than:
                continue
            filtered_runs.append(r)
        return filtered_runs

    def count_percentage(self, arr, sat, sat_param=None):
        num_of_sats = 0
        tot = 0
        for r in arr:
            if sat(r, sat_param):
                num_of_sats += 1
            tot += 1
        p = num_of_sats / tot
        return p

    def create_runs(self):
        for i in range(len(self.df)):
            row = self.df.loc[i, :].to_list()
            run = Run()
            run.inst_name = row[0].strip("\"")
            run.num_of_agents = row[1]
            run.size = row[2]
            run.source = row[3]
            run.type = row[4]
            run.horizon = row[5]
            run.algo = row[6]
            run.fin_res = row[7]
            run.time = row[8] if row[8] != '-' else -1
            run.states = row[9]
            run.results = [[float(number.strip(",)")) for number in pair.split(", ")] for pair in
                           row[10].strip("()").split("), (")]

            self.runs.append(run)

    def normalize(self):
        for i in self.instances.values():
            if i.best_value is not None:
                i.BFS.fin_res /= i.best_value
                i.BFS.time /= i.BFS_time

                i.BNB.fin_res /= i.best_value
                i.BNB.time /= i.BFS_time

                i.erase_unnescesarry_MCTS()
                i.MCTS.fin_res /= i.best_value

                i.MCTS.time /= i.BFS_time
                for t_id in range(len(i.MCTS.results)):
                    t = i.MCTS.results[t_id]
                    new = (t[0] / i.best_value, t[1] / i.BFS_time)

                    i.MCTS.results[t_id] = new

    def get_success_rate_per_time(self, time_range, save=False):
        algos = ['MCTS_S', 'MCTS_D', 'BFS', 'BNB', 'BNBL']
        for algo in algos:
            x = []
            y = []
            for time in range(1, time_range):
                t = time
                y.append(len(self.filter_runs(time_less_than=t, algo=algo)) / len(self.filter_runs(algo=algo)))
                x.append(t)
            plt.scatter(x, y)
        plt.legend(algos)
        plt.xlabel('Runtime limit (s)')
        plt.ylabel('Success rate')
        if save:
            plt.savefig('success_rate_per_time.png')
        plt.show()

    def get_success_rate_per_result(self, percentage, save=False):
        x = []
        y = []
        for time in range(1, 100):
            t = time
            y.append(len(self.filter_inst(mcts_s_more_than_percentage=percentage / 100, mcts_s_before_time=t)) / len(
                self.filter_inst(bfs_finished=True)))
            x.append(t)
        plt.scatter(x, y)
        plt.legend('MCTS')
        plt.xlabel('time')
        plt.ylabel('Success rate')
        if save:
            plt.savefig('success_per_result.png')
        plt.show()


def main():
    analyzer = Analyzer()
    analyzer.create_runs()
    instances = {}
    data_for_graphs = {}
    data_for_tables = {}
    for run in analyzer.runs:
        if not run.inst_name in instances:
            instances[run.inst_name] = {}
        instances[run.inst_name][run.algo] = run
    for instance in list(instances.values()):
        if 'BFS' not in instance:
            continue
        bfs_time = instance['BFS'].results[-1][1]
        bfs_result = instance['BFS'].results[-1][0]
        bfs_states = instance['BFS'].states
        for algo in instance:
            run = instance[algo]
            for pair in run.results:
                pair[0] = round(pair[0] / bfs_result, 2)
                pair[1] = round(pair[1] / bfs_time, 2)
            if not algo in data_for_graphs:
                data_for_graphs[algo] = []
            data_for_graphs[algo].append(run)
            if not algo in  data_for_tables:
                data_for_tables[algo] = []
            data_for_tables[algo].append(run.states/bfs_states)
    graphs = {algo: [[], []] for algo in data_for_graphs}
    for algo in data_for_graphs:
        runs = data_for_graphs[algo]
        for t100 in range(1, 100, 1):
            t = t100 / 100
            results = []
            for run in runs:
                for pair in run.results:
                    if pair[1] == t:
                        results.append(pair[0])
                        break
            avg_result = statistics.mean(results)
            graphs[algo][0].append(t)
            graphs[algo][1].append(avg_result)
    plt.plot(graphs['BFS'][0], graphs['BFS'][1], graphs['BNBL'][0], graphs['BNBL'][1], graphs['BNB'][0],
             graphs['BNB'][1], graphs['MCTS_S'][0], graphs['MCTS_S'][1], graphs['MCTS_D'][0], graphs['MCTS_D'][1], )
    plt.legend(['BFS', 'BNBL', 'BNB', 'MCTS_S', 'MCTS_D'])
    plt.xlabel("Time (relative to BFS time)")
    plt.ylabel("Result (relative to BFS result)")

    print("States (relative to BFS states):")
    for algo in data_for_tables:
        print(algo+": "+str(round(statistics.mean(data_for_tables[algo]), 3)))
    #plt.savefig("COOL.png")
    plt.show()


    # analyzer.get_success_rate_per_time(60)
    # analyzer.get_success_rate_per_result(90)



    types = ['FR', 'MT']
    '''
    for t in types:
        print(t + " BFS success rate: " + str(
            analyzer.count_percentage(filter(list(analyzer.old_instances.values()), inst_is_type, t), inst_has_best_result)))
        print(t + " MCTS success rate: " + str(
            analyzer.count_percentage(filter(list(analyzer.old_instances.values()), inst_is_type, t), inst_has_mcts_result)))
        print()    
    '''

    # analyzer.normalize()

    '''type = 'FR'
    algo = 'MCTS'
    res = {}
    time = {}
    res[type, algo] = []
    time[type, algo] = []

    for i in analyzer.old_instances.values():
        if i.map_type == 'FR' and i.best_value is not None:
            res[type, algo] += [r[0] for r in i.MCTS.results]
            time[type, algo] += [r[1] for r in i.MCTS.results]
    '''


if __name__ == '__main__':
    main()
