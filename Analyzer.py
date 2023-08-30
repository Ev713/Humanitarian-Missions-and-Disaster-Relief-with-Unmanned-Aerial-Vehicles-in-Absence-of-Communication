import pandas
import pandas as pd
import matplotlib.pyplot as plt

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
        self.map_type = None
        self.is_real = False

    def inst_name_extract_type(self):
        if self.inst_name[0] == '_':
            ar_id = self.inst_name.find('AR')
            self.map_type = self.inst_name[ar_id-2] + self.inst_name[ar_id-1]
            self.is_real = True
        else:
            self.map_type = self.inst_name[-2] + self.inst_name[-1]
            self.is_real = False
            
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

    def erase_unnescesarry_MCTS(self):
        new_res = []
        for r in self.MCTS.results:
            if r[1] > self.BFS_time:
                break
            new_res.append(r)
        self.MCTS.results = new_res


class Analyzer:
    def __init__(self):
        self.file_path = "~/Humanitarian-Missions-and-Disaster-Relief-with-Unmanned-Aerial-Vehicles-in-Absence-of-Communication/no_preprocessing_tot.csv"
        self.df = pd.read_csv(self.file_path, header=None, on_bad_lines = 'skip')
        self.runs = []
        self.instances = {}

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
                    run.results = [tuple(float(t.strip('()')) for t in i.strip('').strip(')').split(', ')) for i in row[3].strip("()").split(', (')]
                except:
                    run.results = -1

            run.inst_name_extract_type()
            self.runs.append(run)
            if (run.inst_name, run.flybys, run.map_type) not in self.instances:
                self.instances[(run.inst_name, run.flybys, run.map_type)] = Instance_data(run.inst_name, run.flybys, run.map_type)
            
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
         if i.best_value!=None:
            i.BFS.fin_res /= i.best_value
               #i.BFS.results[0][1]/=best_value
               #i.BFS.results[1][1]/=i.BFS_time
            i.BFS.time/=i.BFS_time

            i.BNB.fin_res /= i.best_value
            i.BNB.time/=i.BFS_time
               # i.BNB.results[0][1]/=best_value
               # i.BNB.results[0][0]/=i.BFS_time

            i.erase_unnescesarry_MCTS()
            i.MCTS.fin_res /= i.best_value
            if i.MCTS.fin_res > 1:
                breakpoint
            i.MCTS.time/=i.BFS_time
            for t_id in range(len(i.MCTS.results)):
                t = i.MCTS.results[t_id]
                new =(t[0]/i.best_value, t[1]/i.BFS_time)
                if new[0] > 1:
                    breakpoint()
                i.MCTS.results[t_id] = new

def main():
    analyzer = Analyzer()
    analyzer.create_runs()
    analyzer.normalize()
    
    type = 'FR'
    algo = 'MCTS'
    res = {}
    time = {}
    res[type, algo] = []
    MCTS_time[type, algo] = []
    
    for i in analyzer.instances.values():
        if i.map_type == 'FR' and i.best_value!=None:
            res[type, algo]+=[r[0] for r in i.MCTS.results]
            time[type, algo]+=[r[1] for r in i.MCTS.results]
    
    x = time[type, algo]
    y = res[type, algo]

    plt.scatter(time[type, algo], res[type, algo])

    z = np.polyfit(x, y, 2)
    p = np.poly1d(z)

    #add trendline to plot
    plt.plot(x, p(x))
    plt.show()

if __name__ == '__main__':
    main()
