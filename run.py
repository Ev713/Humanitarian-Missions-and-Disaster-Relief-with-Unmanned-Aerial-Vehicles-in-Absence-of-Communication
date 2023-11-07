import pandas as pd
import sys

# import instance_collector
import instance_decoder as collector
# import THIRD_instance_collector as collector
import Solver

'''
Run using :
    
for i in {0..n}; do for strategy in 'MCTS_D' 'MCTS_S' 'BFS' 'BNB' 'BNBL'; do for preprocessing in {0..1}; do python3 run.py $i $strategy $preprocessing & done done done

    
where n is the last index of old_instances i instance collector.
'''


def run_solver(inst, algo, default='-'):
    # print("start " + inst.name)
    solver = Solver.Solver()
    solver.NUMBER_OF_SIMULATIONS = 10000000
    solver.JUMP = solver.NUMBER_OF_SIMULATIONS / min(solver.NUMBER_OF_SIMULATIONS, 100)
    solver.timeout = 30
    solution = None
    if algo == 'MCTS_D':
        solution = solver.det_mcts(inst)
    if algo == 'MCTS_S':
        solution = solver.stoch_mcts(inst)
    if algo == 'BFS':
        solver.type = 'U1S'
        solution = solver.bfs(inst)
    if algo == 'BNBL':
        solver.type = 'U1S'
        solution = solver.branch_and_bound(inst, solver.Heuristics_U1, solver.Lower_bound_U1)
    if algo == 'BNB':
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
    name = 'server'
    inst = collector.instances[int(args[0])]
    algo = str(args[1])
    preprocessing = int(args[2])
    print("\n" + inst.name + " with " + algo + " starts")

    if preprocessing == 1:
        # Loop over old_instances and num_of_sim
        import time
        start = time.clock_gettime(time.CLOCK_THREAD_CPUTIME_ID)
        inst.map_reduce()
        finish = time.clock_gettime(time.CLOCK_THREAD_CPUTIME_ID)

        preprocess_time = finish - start

        df2 = pd.DataFrame({"inst_name": inst.name, "preprocess_time": preprocess_time, 'algo': algo})

        df2.to_csv('data/'+name+'_preprocess_time',mode='a', index=False)
        print(inst.name + " " + algo + '_preprocess_time: ' + preprocess_time)

    df = pd.DataFrame(
        columns=[
            'inst_name',
            'num_agents',
            'map_size',
            'source',
            'type',
            'horizon',
            'algo',
            'final_result',
            'time',
            'states',
            'result', ], dtype=object
    )
    # collected data:
    # num_agents, map_size, source, type, horizon, final result, time, states, result
    fin_res, t, res, states = run_solver(inst, algo)
    data_to_append.append({'inst_name': str(inst.name), 'num_agents': len(inst.agents), 'map_size': len(inst.map),
                           'source': str(inst.source), 'type': str(inst.type), 'horizon': int(inst.horizon),
                           'algo': str(algo),
                           'final_result': float(fin_res), 'time': float(t) if t != '-' else '-', 'states': int(states),
                           'result': res})
    print({'inst_name': inst.name, 'num_agents': len(inst.agents), 'map_size': len(inst.map),
           'source': inst.source, 'type': inst.type, 'horizon': inst.horizon, 'algo': algo,
           'final_result': fin_res, 'time': t, 'states': states, })

    df.to_csv('data/'+name+('_with_' if preprocessing == 1 else'_no_')+'preprocessing_tot.csv', mode='a', index=False, header=False)



if __name__ == "__main__":
    main()
