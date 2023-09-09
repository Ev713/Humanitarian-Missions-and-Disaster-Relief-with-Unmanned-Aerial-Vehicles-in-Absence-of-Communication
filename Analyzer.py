import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# (inst.name, solver_type, algo, flybys)

def mcts_is_timeout(run, param=None):
    return run.time == -1


def inst_is_type(inst, t):
    return inst.map_type == t


def time_less_than(run, time):
    return not mcts_is_timeout(run) and run.time < time


def result_greater_than(inst, p):
    return inst.MCTS.fin_res >= p * inst.best_value


def run_is_algo(run, algo):
    return run.algo == algo


def inst_has_best_result(inst, param=None):
    return inst.best_value is not None


def inst_has_mcts_result(inst, param=None):
    return not mcts_is_timeout(inst.MCTS)


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
        self.is_real = False

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
        self.MCTS = None

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
        self.file_path = "small_no_preprocessing_tot.csv"
        self.df = pd.read_csv(self.file_path, header=None, on_bad_lines='skip')
        self.runs = []
        self.instances = {}

    def count_percentage(self, arr, sat, sat_param, filter=None, filter_param=None):
        num_of_sats = 0
        tot = 0
        for r in arr:
            if not filter(r, filter_param):
                continue
            if sat(r, sat_param):
                num_of_sats += 1
            tot += 1
        p = num_of_sats / tot
        return p

    def create_runs(self):
        for i in range(len(self.df)):
            row = self.df.loc[i, :].to_list()
            run_info = row[0]
            run = Run()
            run.inst_name = run_info.strip("()").split(', ')[0].strip('\'\'')
            run.solver_type = run_info.strip("()").split(', ')[1].strip('\'\'')
            run.algo = run_info.strip("()").split(', ')[2].strip('\'\'')
            run.flybys = bool(run_info.strip("()").split(', ')[3].strip('\'\''))
            run.fin_res = row[1]
            run.states = row[4]
            try:
                run.time = float(row[2])
            except:
                run.time = -1
            if run.time == -1:
                try:
                    run.results = [float(c) for c in row[3].replace(")", "").replace("(", "").strip(",").split(", ")]
                except:
                    run.results = -1
            else:
                temp = [i.strip('').strip(')').split(', ') for i in row[3].strip("()").split(', (')]
                try:
                    run.results = [tuple(float(t.strip('()')) for t in i.strip('').strip(')').split(', ')) for i in
                                   row[3].strip("()").split(', (')]
                except:
                    run.results = -1

            run.inst_name_extract_type()
            self.runs.append(run)
            if (run.inst_name, run.flybys, run.map_type) not in self.instances:
                self.instances[(run.inst_name, run.flybys, run.map_type)] = Instance_data(run.inst_name, run.flybys,
                                                                                          run.map_type)

            id = self.instances[(run.inst_name, run.flybys, run.map_type)]
            match run.algo:
                case 'BFS':
                    id.BFS = run
                    if run.time != -1:
                        id.best_value = run.fin_res
                        id.BFS_time = run.time
                case 'BNB':
                    id.BNB = run
                case 'MCTS':
                    id.MCTS = run

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

    def get_success_rate_per_time(self):
        algos = ['MCTS', 'BFS', 'BNB']
        for algo in algos:
            x = []
            y = []
            for time in range(1, 600):
                t = time
                y.append(self.count_percentage(self.runs, time_less_than, t, filter=run_is_algo, filter_param=algo))
                x.append(t)
            plt.scatter(x, y)
        plt.legend(algos)
        plt.xlabel('Runtime limit (s)')
        plt.ylabel('Success rate')
        plt.show()

    def get_success_rate_per_result(self, save=False):
        x = []
        y = []
        for time in range(1, 100):
            t = time / 100
            y.append(self.count_percentage(self.instances.values(), result_greater_than, t, inst_has_best_result))
            x.append(t)
        plt.scatter(x, y)
        plt.legend('MCTS')
        plt.xlabel('Percent of best value')
        plt.ylabel('Success rate')
        if save:
            plt.savefig('success_per_result.png')
        plt.show()


def main():
    analyzer = Analyzer()
    analyzer.create_runs()
    analyzer.get_success_rate_per_result(True)
    types = ['FR', 'MT']
    for t in types:
        print(t + " BFS success rate: " + str(
            analyzer.count_percentage(list(analyzer.instances.values()), inst_has_best_result, None, inst_is_type, t)))
        print(t + " MCTS success rate: " + str(
            analyzer.count_percentage(list(analyzer.instances.values()), inst_has_mcts_result, None, inst_is_type, t)))
        print()
    # analyzer.normalize()

    '''type = 'FR'
    algo = 'MCTS'
    res = {}
    time = {}
    res[type, algo] = []
    time[type, algo] = []

    for i in analyzer.instances.values():
        if i.map_type == 'FR' and i.best_value is not None:
            res[type, algo] += [r[0] for r in i.MCTS.results]
            time[type, algo] += [r[1] for r in i.MCTS.results]
    '''


if __name__ == '__main__':
    main()
