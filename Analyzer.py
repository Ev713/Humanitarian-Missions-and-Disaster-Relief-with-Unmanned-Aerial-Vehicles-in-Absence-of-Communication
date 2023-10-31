import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


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
        #self.is_real = False
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

    def filter_inst(self, bfs_finished=None, mcts_s_more_than_percentage=None, mcts_d_more_than_percentage=None, mcts_s_before_time=None, mcts_d_before_time=None):
        filtered_instances = []
        for i in list(self.instances.values()):
            if mcts_s_more_than_percentage is not None:
                if i.best_value == -1 or i.MCTS_S.results==-1:
                    continue
                try:
                    if mcts_s_before_time is None:
                        res = i.MCTS_S.fin_res
                    else:
                        id = 0
                        res = i.MCTS_S.results[0][1]
                        while(i.MCTS_S.results[id][1]<mcts_s_before_time and id < len(i.MCTS_S.results)):
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

    def create_runs_NEW(self):
        for i in range(len(self.df)):
            row = self.df.loc[i, :].to_list()
            run = Run()
            run.inst_name = row[0]
            run.num_of_agents = row[1]
            run.map_size = row[2]
            run.source = row[3]
            run.horizon = row[4]
            run.algo = row[5]
            run.fin_res = row[6]
            run.time = float(row[7]) if row[7] != '-' else -1
            run.states = row[8]
            run.results = [tuple(float(t.strip('()')) for t in i.strip('').strip(')').split(', ')) for i in
                                   row[9].strip("()").split(', (')] if len(row[9]) > 2 else []
            self.runs.append(run)

    def create_runs(self):
        for i in range(len(self.df)):
            row = self.df.loc[i, :].to_list()
            run_info = row[0]
            run = Run()
            run.inst_name = run_info.strip("()").split(', ')[0].strip('\'\'')
            run.algo = run_info.strip("()").split(', ')[1].strip('\'\'')
            # run.algo = run_info.strip("()").split(', ')[2].strip('\'\'')
            # run.flybys = bool(run_info.strip("()").split(', ')[3].strip('\'\''))
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
                    else:
                        id.best_value = -1
                case 'BNB':
                    id.BNB = run
                case 'MCTS_S':
                    id.MCTS_S = run
                case 'MCTS_D':
                    id.MCTS_S = run

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
            y.append(len(self.filter_inst(mcts_s_more_than_percentage=percentage/100, mcts_s_before_time=t))/len(self.filter_inst(bfs_finished=True)))
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
    analyzer.create_runs_NEW()
    #analyzer.get_success_rate_per_time(60)
    #analyzer.get_success_rate_per_result(90)

    for run in analyzer.runs:
        rewards = [r[0] for r in run.results if r[1]-run.results[0][1]<300]
        times = [r[1]-run.results[0][1] for r in run.results if r[1]<300]
        states = [r[2] for r in run.results if r[1]-run.results[0][1]<300]
        plt.scatter(times, rewards)
    plt.xlabel('time')
    plt.ylabel('states')
    plt.legend([run.algo for run in analyzer.runs])
    plt.show()
    #plt.savefig()


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
