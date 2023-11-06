import pandas as pd
import sys

# import instance_collector
import instance_decoder as collector
# import THIRD_instance_collector as collector
import Solver

'''
Run using :
    
    for i in {0..n}; do for strategy in 'MCTS_D' 'MCTS_S' 'BFS' 'BNB' 'BNBL'; do python3 run.py $i $strategy & done done

    
where n is the last index of old_instances i instance collector.
'''


def run_solver(inst, algo, default='-'):
    # print("start " + inst.name)
    solver = Solver.Solver()
    solver.NUMBER_OF_SIMULATIONS = 1000000
    solver.JUMP = solver.NUMBER_OF_SIMULATIONS / min(solver.NUMBER_OF_SIMULATIONS, 100)
    solver.timeout = 420
    solution = None
    if algo == 'MCTS_D':
        solution = solver.det_mcts(inst)
    if algo == 'MCTS_S':
        solution = solver.stoch_mcts(inst)
    if algo == 'BFS':
        solver.type = 'U1S'
        solution = solver.bfs(inst)
    if algo == 'BNB':
        solver.type = 'U1S'
        solution = solver.branch_and_bound(inst, solver.Heuristics_U1, solver.Lower_bound_U1)
    if algo == 'BNBL':
        solver.type = 'U1S'
        solution = solver.branch_and_bound(inst, solver.Heuristics_U1)

    timestamps = solution.timestamps
    states = solution.states
    solver.type = 'U1S'
    solution.set_rewards(solver, inst)
    res = tuple(zip(solution.rewards, timestamps))
    fin_res = solution.rewards[-1] if len(solution.rewards) > 0 else default
    time = timestamps[-1] if not solution.interrupted else default
    return fin_res, time, res, states


def main():
    data_to_append = []
    args = sys.argv[1:]
    inst = collector.instances[int(args[0])]
    algo = str(args[1])
    print("\n" + inst.name + " with " + algo + " starts")
    df = pd.DataFrame(columns=['inst_name', 'num_agents', 'map_size', 'source', 'type', 'horizon', 'algo',
                               'final_result', 'time', 'states', 'result'])
    # collected data:
    # num_agents, map_size, source, type, horizon, final result, time, states, result
    fin_res, t, res, states = run_solver(inst, algo)
    data_to_append.append({'inst_name': str(inst.name), 'num_agents': len(inst.agents), 'map_size': len(inst.map),
                           'source': str(inst.source), 'type': str(inst.type), 'horizon': int(inst.horizon), 'algo': str(algo),
                           'final_result': float(fin_res), 'time': float(t), 'states': int(states), 'result': res})
    print({'inst_name': inst.name, 'num_agents': len(inst.agents), 'map_size': len(inst.map),
           'source': inst.source, 'type': inst.type, 'horizon': inst.horizon, 'algo': algo,
           'final_result': fin_res, 'time': t, 'states': states, })

    # Concatenate the collected data to the DataFrame
    df = pd.concat([df, pd.DataFrame(data_to_append)], ignore_index=True)

    # Print the resulting DataFrame
    print(inst.name + ' without preprocessing is done')
    # df.to_csv(inst.name + "no_preprocessing.csv", index=False)

    df.to_csv('data/small_maps_no_preprocessing_tot.csv', mode='a', index=False, header=False)
    # df = pd.DataFrame(columns=["run", "final result", "time", "result", 'states'])


'''
    data_to_append = []
    preprocess_time = preprocess_names = []
    # Loop over old_instances and num_of_sim
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
