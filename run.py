import pandas as pd
import sys

import SECOND_instance_collector
import Solver

#for i in {0..39}; do python3 run.py $i & done
def run_solver(inst, algo, default='-'):
    # print("start " + inst.name)
    solver = Solver.Solver()
    solver.NUMBER_OF_SIMULATIONS = 50000
    solver.JUMP = solver.NUMBER_OF_SIMULATIONS / min(solver.NUMBER_OF_SIMULATIONS, 100)
    solver.timeout = 240
    match algo:
        case 'MCTS_D':
            solver.type = 'U1D'
            solution = solver.mcts(inst)
        case 'MCTS_S':
            solver.type = 'U1S'
            solution = solver.mcts(inst)
        case 'BFS':
            solver.type = 'U1S'
            solution = solver.bfs(inst)
        case 'BNB':
            solver.type = 'U1S'
            solution = solver.branch_and_bound(inst, solver.Heuristics_U1, solver.Lower_bound_U1)
        case 'BNBL':
            solver.type = 'U1S'
            solution = solver.branch_and_bound(inst, solver.Heuristics_U1)

    timestamps = solution.timestamps
    states_collector = solution.states_collector
    states = solution.states
    solver.type = 'U1S'
    solution.set_rewards(solver, inst)
    res = tuple(zip(solution.rewards, timestamps, states_collector))
    try:
        fin_res = solution.rewards[-1]
    except IndexError:
        fin_res = default
    try:
        time = timestamps[-1]
    except:
        time=default
    return fin_res, time, res, states


def main():
    import time
    data_to_append = []
    args = sys.argv[1:]
    inst = SECOND_instance_collector.instances[int(args[0])]
    print("\n" + inst.name + " starts")
    df = pd.DataFrame(columns=["run", "final result", "time", "result", 'states'])
    for flybys in [True]:
        inst.flybys = flybys
        for algo in ['MCTS_S','MCTS_D', 'BFS', 'BNB', 'BNBL']:
            fin_res, time, res, states = run_solver(inst, algo)
            data_to_append.append({"run": (inst.name, algo, flybys), "final result":
                fin_res, "time": time, "result": res, 'states': states})
            print({"run": (inst.name, algo, flybys), "final result":
                    fin_res, "time": time})

    # Concatenate the collected data to the DataFrame
    df = pd.concat([df, pd.DataFrame(data_to_append)], ignore_index=True)

    # Print the resulting DataFrame
    print(inst.name + ' without preprocessing is done')
    #df.to_csv(inst.name + "no_preprocessing.csv", index=False)

    df.to_csv('NEW_data/NEW_no_preprocessing_tot.csv', mode='a', index=False, header=False)
    print("first file added")
    #df = pd.DataFrame(columns=["run", "final result", "time", "result", 'states'])
'''
    data_to_append = []
    preprocess_time = preprocess_names = []
    # Loop over instances and num_of_sim
    import time
    start = time.clock_gettime(time.CLOCK_THREAD_CPUTIME_ID)
    inst.map_reduce()
    finish = time.clock_gettime(time.CLOCK_THREAD_CPUTIME_ID)

    preprocess_time.append(finish - start)
    preprocess_names.append(inst.name)

    for flybys in [True, False]:
        inst.flybys = flybys
        for solver_type in ['U1D', 'U1S']:  # , 'URD', 'URS']:
            for algo in ['MCTS', 'BFS', 'BNB', 'BNBH']:
                if algo != 'MCTS' and (solver_type == 'U1D' or solver_type == 'URD'):
                    continue
                fin_res, time, res, states = run_solver(inst, algo, solver_type)
                data_to_append.append({"run": (inst.name, solver_type, algo, flybys), "final result":
                    fin_res, "time": time, "result": res, 'states':states})
                print({"run": (inst.name, solver_type, algo, flybys), "final result":
                    fin_res, "time": time})

    # Concatenate the collected data to the DataFrame
    df = pd.concat([df, pd.DataFrame(data_to_append)], ignore_index=True)
    df.to_csv('small_ye_preprocessing_tot.csv', mode='a', index=False, header=False)

    df2 = pd.DataFrame({"preprocess_name": preprocess_names, "preprocess_time": preprocess_time})
    df.to_csv('preprocess_times.csv', mode='a', index=False, header=False)
    # Print the resulting DataFrame
    print(inst.name + ' with preprocessing is done')
    df.to_csv(inst.name + "preprocessing.csv", index=False)
    df2.to_csv(inst.name + "preprocess_time", index=False)
    print("second and third files added")

    # Pass the list as an argument into
    # the writerow()
'''

if __name__ == "__main__":
    main()