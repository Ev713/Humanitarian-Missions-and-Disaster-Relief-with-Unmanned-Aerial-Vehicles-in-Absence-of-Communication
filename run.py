import sys
import pandas as pd

import Solver
import instance_collector


def timeout_exec(search, inst, solver, timeout_duration=10, default='-'):
    """This function will spawn a thread and run the given function
    using the args, kwargs and return the given default value if the
    timeout_duration is exceeded.
    """
    import threading
    import time

    class InterruptableThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = default

        def run(self):
            # try:
            if search == 'MCTS':
                self.result = run_mcts(inst, solver, default)
            if search == 'BFS':
                self.result = run_bfs(inst, solver, default)

            # except Exception as e:
            #    self.result = (-3, -3, e)

    try:
        solver.interrupt_flag = False
        start = time.time()
        it = InterruptableThread()
        it.start()
        it.join(timeout_duration)
        if it.is_alive():
            solver.interrupt()
            res = it.result
            final_res = res[-1] if search == 'MCTS' else res
            del it
            return final_res, default, res
        else:
            end = time.time()
            res = it.result
            final_res = res[-1] if search == 'MCTS' else res
            del it
            return final_res, end - start, res
    except:
        # print()
        return default, default, default


def run_mcts(inst, solver, default):
    # print("start " + inst.name)
    paths = solver.mcts(inst)
    p = tuple((solver.evaluate_path(inst, p) for p in paths))
    if not solver.interrupt_flag:
        pass  # print("succesfully finished " + inst.name)
    else:
        # print("Out of time")
        solver.flag = False
    return p


def run_bfs(inst, solver, default):
    # print("start " + inst.name)
    path = solver.bfs(inst)
    if not solver.interrupt_flag:
        pass  # print("succesfully finished " + inst.name)
    else:
        # print("Out of time")
        solver.flag = False
    return solver.evaluate_path(inst, path)


def run_bnb(inst, solver, default):
    # print("start " + inst.name)
    if solver.type == "U1S":
        path = solver.bnb(inst, solver.Heuristics_U1, solver.Lower_bound_U1)
    elif solver.type == "URS":
        path = solver.bnb(inst, solver.Heuristics_UR, solver.Lower_bound_UR)
    if not solver.interrupt_flag:
        pass  # print("succesfully finished " + inst.name)
    else:
        # print("Out of time")
        solver.flag = False
    return solver.evaluate_path(inst, path)


def main():
    import time

    data_to_append = []
    args = sys.argv[1:]
    inst = instance_collector.instances[0]
    df = pd.DataFrame(columns=["run", "final result", "time", "result"])
    for flybys in [True, False]:
        inst.flybys = flybys
        for solver_type in ['U1D', 'U1S', 'URD', 'URS']:

            for algo in ['MCTS', 'BFS', 'BNB']:
                if algo != 'MCTS' and (solver_type == 'U1D' or solver_type == 'URD'):
                    continue
                for num_of_sim in [5000]:#[100, 500, 1000, 2000, 5000]:
                    solver = Solver.Solver()
                    solver.type = solver_type
                    solver.NUMBER_OF_SIMULATIONS = num_of_sim
                    fin_res, exec_time, result = timeout_exec(algo, inst, solver)
                    if algo != 'MCTS':
                        break
                        # Append data to the list
                    data_to_append.append({"run": (inst.name, num_of_sim, solver_type, algo, flybys), "final result":
                        fin_res, "time": exec_time, "result": result})

    # Concatenate the collected data to the DataFrame
    df = pd.concat([df, pd.DataFrame(data_to_append)], ignore_index=True)

    # Print the resulting DataFrame
    print(df)
    df.to_csv("no_preprocessing.csv", index=False)



    df = pd.DataFrame(columns=["run", "final result", "time", "result"])

    data_to_append = []
    preprocess_time = preprocess_names = []
    # Loop over instances and num_of_sim

    start = time.time()
    inst.map_reduce()
    finish = time.time()
    preprocess_time.append(finish - start)
    preprocess_names.append(inst.name)

    for flybys in [True, False]:
        inst.flybys = flybys
        for solver_type in ['U1D', 'U1S', 'URD', 'URS']:
            for algo in ['MCTS', 'BFS', 'BNB']:
                if algo != 'MCTS' and (solver_type == 'U1D' or solver_type == 'URD'):
                    continue
                for num_of_sim in [5000]:#, 1000, 10000]:
                    solver = Solver.Solver()
                    solver.type = solver_type
                    solver.NUMBER_OF_SIMULATIONS = num_of_sim
                    fin_res, time, result = timeout_exec(algo, inst, solver)
                        # Append data to the list
                    data_to_append.append({"run": (inst.name, num_of_sim, solver_type, algo, flybys), "final result":
                        fin_res, "time": time, "result": result})
                    if algo != 'MCTS':
                        break
    df2 = pd.DataFrame({"prepproces_name": preprocess_names, "preprocess_time": preprocess_time})

    # Concatenate the collected data to the DataFrame
    df = pd.concat([df, pd.DataFrame(data_to_append)], ignore_index=True)

    # Print the resulting DataFrame
    print(df)
    df.to_csv(inst.name + "preprocessing.csv", index=False)
    df2.to_csv(inst.name + "preprocess_time", index=False)


if __name__ == "__main__":
    main()
