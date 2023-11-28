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
        self.size = 0

    def ag_is_success(self):
        return self.fin_res == (self.size - 1) / 2 + 1

    def sc_is_success(self):
        return self.fin_res == math.sqrt(self.size - 1) * 2

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
        self.type = map_type
        self.BFS_time = None
        self.best_value = None
        self.BFS = None
        self.BNB = None
        self.MCTS_D = None
        self.MCTS_S = None

    def clone(self):
        cp = Instance_data(self.inst_name, self.flybys, self.type)
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
    def __init__(self, filepath):
        self.file_path = filepath
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
            if map_type is not None and r.type != map_type:
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
    acc = 2
    algos = set()

    allowed_types = (
        'FR',
        'MT',
        'SC',
        'AG01',
        'AG001',
        'AG05'
    )
    filepath = "data/nov_27_2023_30mins_all.csv"
    analyzer = Analyzer(filepath)
    analyzer.create_runs()
    instances = {}
    data_for_graphs = {}
    data_for_tables = {}
    counter = 0

    for run in analyzer.runs:
        algos.add(run.algo)
        max_result = 0
        for r in run.results:
            if r[0] >= max_result:
                max_result = r[0]
            else:
                counter += 1
                break

    for run in analyzer.runs:
        if run.inst_name not in instances:
            instances[run.inst_name] = {}
        instances[run.inst_name][run.algo] = run

    fin_ress = {algo: [] for algo in algos}
    sizes = {algo: [] for algo in algos}
    states = {algo: [] for algo in algos}
    default = 'BFS'
    num_of_types = {type: 0 for type in allowed_types}
    for inst_name in instances:

        instance_runs = instances[inst_name]

        #all_algos = True
        #for algo in algos:
        #    if algo not in instance_runs:
        #        all_algos = False

        #if not all_algos:
        #    continue

        if default not in instance_runs or instance_runs[default].results[-1][0] == 0:
            continue
        #if instance_runs[default].type not in allowed_types:
        #    continue

        #if instance_runs['BFS'].source == 'X' or instance_runs['BFS'].type != 'MT':
        #    continue

        def_result = instance_runs[default].results[-1][0]
        def_time = max([run.results[-1][2] for run in analyzer.runs])  # instance_runs[default].results[-1][2]
        def_states = instance_runs[default].states

        for instance in instances:
            for algo in algos:
                if algo in instances[instance]:
                    num_of_types[instances[instance][algo].type] += 1
                    break

        for algo in algos:
            if algo not in instance_runs:
                continue
            run = instance_runs[algo]
            size = run.size
            fin_res = run.results[-1][0]

            sizes[algo].append(size)
            fin_ress[algo].append(fin_res)
            states[algo].append(run.states)

            for pair in run.results:
                pair[0] = round(pair[0] / def_result, acc)
                pair[1] = round(pair[1] / def_states, acc)
                pair[2] = round(pair[2] / def_time, acc)
            if algo not in data_for_graphs:
                data_for_graphs[algo] = []
            data_for_graphs[algo].append(run)
            if algo not in data_for_tables:
                data_for_tables[algo] = []
            data_for_tables[algo].append(run.states / def_states)

    for t in num_of_types:
        print(t, num_of_types[t])

    relative_to_states = False

    graphs = {algo: [[], []] for algo in data_for_graphs}
    for algo in data_for_graphs:
        runs = data_for_graphs[algo]
        runs_complete_results = []
        for run in runs:
            run_complete_data = {0: 0}
            for t100 in range(1, pow(10, acc) + 1, 1):
                t = t100 / pow(10, acc)
                for r in run.results:
                    if (relative_to_states and r[1] == t) \
                            or (not relative_to_states and r[2] == t):
                        run_complete_data[t] = r[0] # 0 for result 1 for states
                if t not in run_complete_data:
                    prev = round(t - 1 / pow(10, acc), acc)
                    run_complete_data[t] = run_complete_data[prev]
            runs_complete_results.append(run_complete_data)
        for t100 in range(1, pow(10, acc), 1):
            t = t100 / pow(10, acc)
            results = []
            for run in runs_complete_results:
                results.append(run[t])
            avg_result = statistics.mean(results)
            graphs[algo][0].append(t)
            graphs[algo][1].append(avg_result)

    for algo in algos:
        plt.plot(graphs[algo][0], graphs[algo][1], label=algo)

    plt.legend(algos)
    if not relative_to_states:
        plt.xlabel("Time (relative to "+default+" time)")
    else:
        plt.xlabel("States (relative to "+default+" states)")
    plt.ylabel("Result (relative to "+default+" result)")
    plt.title("All maps, new heuristics")
    plt.ylim(bottom=0)

    print("States (relative to BFS states):")
    for algo in data_for_tables:
        print(algo + ": " + str(round(statistics.mean(data_for_tables[algo]), 3)))

    '''print("SC success rates:")
    for algo in data_for_tables:
        runs = []
        for r in analyzer.runs:
            if r.type in ['SC']:
                if r.algo == algo:
                    if r.sc_is_success():
                        runs.append(r)
        print(algo + ": " + str(round(len([r for r in analyzer.runs if r.type in ['AG05', 'AG01',
                                                                                'AG001'] and r.algo == algo and r.ag_is_success()]))))
'''
    # algo = 'BNBL'
    # plt.scatter(sizes[algo], fin_ress[algo])
    # plt.title('BNB')
    # plt.xlabel("Size")
    # plt.ylabel("Reward")

    # , sizes['BNB'], fin_ress['BNB'], sizes['BNBL'], fin_ress['BNBL'],
    #            sizes['MCTS_S'], fin_ress['MCTS_S'], sizes['MCTS_D'], fin_ress['MCTS_D'])

    # plt.savefig("data/Images/server_full_data.png")
    plt.show()


if __name__ == '__main__':
    main()
