import csv
import time

import pd as pd

import instance_collector
import main
import pandas as pd


def timeout_exec(search, inst, solver, timeout_duration=30, default='-'):
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

    start = time.time()
    it = InterruptableThread()
    it.start()
    it.join(timeout_duration)
    if it.is_alive():
        solver.interrupt()
        del it
        return default, default, default
    else:
        end = time.time()
        res = it.result
        final_res = res[-1] if search == 'MCTS' else res
        del it
        return final_res, end - start, res


def run_mcts(inst, solver, default):
    print("start " + inst.name)
    try:
        paths = solver.mcts(inst)
        p = tuple((solver.evaluate_path(inst, p) for p in paths))
        print("succesfully finished " + inst.name)
        return p
    except main.TimeoutException as timeout_exception:
        # Handle the custom timeout exception
        print("Caught TimeoutException:", str(timeout_exception))
    return default


def run_bfs(inst, solver, default):
    print("start " + inst.name)
    try:
        path = solver.bfs(inst)
        print("succesfully finished " + inst.name)
        return path
    except main.TimeoutException as timeout_exception:
        # Handle the custom timeout exception
        print("Caught TimeoutException:", str(timeout_exception))
    return default


def run_bnb(inst, solver, default):
    print("start " + inst.name)
    try:
        if solver.type == "U1S":
            path = solver.bnb(inst, solver.Heuristics_U1, solver.Lower_bound_U1)
        elif solver.type == "URS":
            path = solver.bnb(inst, solver.Heuristics_UR, solver.Lower_bound_UR)

        print("succesfully finished " + inst.name)
        return path
    except main.TimeoutException as timeout_exception:
        # Handle the custom timeout exception
        print("Caught TimeoutException:", str(timeout_exception))
    return default


df = pd.DataFrame(columns=["run", "final result", "time", "result"])

solver = main.Solver()

# Initialize an empty list to collect data
data_to_append = []
counter = 0
# Loop over instances and num_of_sim
for inst in instance_collector.instances:
    inst.map_reduce()
    for flybys in [True, False]:
        inst.flybys = flybys
        for num_of_sim in [1000]:  # , 1000, 10000]:
            solver.NUMBER_OF_SIMULATIONS = num_of_sim
            for solver_type in ['U1D', 'U1S', 'URD', 'URS']:
                solver.type = solver_type
                for algo in ['MCTS', 'BFS', 'BNB']:
                    fin_res, time, result = timeout_exec(algo, inst, solver)
                    # Append data to the list
                    data_to_append.append({"run": (inst.name, num_of_sim, solver_type, flybys), "final result": fin_res,
                                           "time": time, "result": result})

# Concatenate the collected data to the DataFrame
df = pd.concat([df, pd.DataFrame(data_to_append)], ignore_index=True)

# Print the resulting DataFrame
print(df)
df.to_csv("output.csv", index=False)
