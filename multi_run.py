import concurrent.futures
import multiprocessing
import sys
import time
from multiprocessing import Process

import pandas as pd

import Solver
import instance_decoder


def write_data(r, name, ):
    fin_res, t, res, states, inst, algo = r[0], r[1], r[2], r[3], r[4], r[5]
    df = pd.DataFrame({'inst_name': [str(inst.name)], 'num_agents': [len(inst.agents)], 'map_size': [len(inst.map)],
                       'source': [str(inst.source)], 'type': [str(inst.type)], 'horizon': [int(inst.horizon)],
                       'algo': [str(algo)],
                       'final_result': [float(fin_res)], 'time': [float(t)] if t != '-' else '-', 'states': int(states),
                       'result': [str(res)]})
    print({'inst_name': inst.name, 'num_agents': len(inst.agents), 'map_size': len(inst.map),
           'source': inst.source, 'type': inst.type, 'horizon': inst.horizon, 'algo': algo,
           'final_result': fin_res, 'time': t, 'states': states, })

    df.to_csv('data/' + name + '.csv', mode='a', index=False,
              header=False)


def run_solver(inst, algo, timeout=1800, default='-', dup_det=True):
    print("start " + inst.name, algo)
    solver = Solver.Solver(inst)
    solver.dup_det = dup_det
    solver.timeout = timeout
    results = None
    if algo == 'MCTS_E':
        results = solver.emp_mcts()
    if algo == 'MCTS_V':
        results = solver.vector_mcts()
    if algo == 'MCTS_S':
        results = solver.semi_emp_mcts()
    if algo == 'BFS':
        solver.type = 'U1S'
        results = solver.bfs()
    if algo == 'BNBL':
        solver.type = 'U1S'
        results = solver.branch_and_bound(solver.upper_bound_base_plus_utility,
                                          solver.lower_bound_base_plus_utility)
    if algo == 'BNB':
        solver.type = 'U1S'
        results = solver.branch_and_bound(solver.upper_bound_base_plus_utility)
    if algo == 'GBFS':
        solver.type = 'U1S'
        results = solver.greedy_best_first_search()
    fin_res = results[-1][0] if len(results) > 0 else default
    fin_time = results[-1][-1] if len(results) > 0 and results[-1][-1] < timeout else default
    fin_states = results[-1][1] if len(results) > 0 else default
    return fin_res, fin_time, results, fin_states, inst, algo


def single_run():
    args = [0, 'GBFS']
    name = 'scratch'
    timeout = 99999
    decoder = instance_decoder.Decoder()
    decoder.decode_reduced(size_higher_bound=30)
    inst = decoder.instances[int(args[0])]
    # Inst_visualizer.vis3(inst, name)
    algo = str(args[1])
    print("\n" + inst.name + " with " + algo + " starts")

    r = run_solver(inst, algo, timeout)
    write_data(r, name)


def solve(args):
    return run_solver(args[0], args[1], args[2])


def multi_run():
    algos = [
        'MCTS_E',
        'MCTS_V',
        'MCTS_S',
        'BFS',
        'BNBL',
        'BNB',
        'GBFS'
    ]
    name = 'nov_29'
    timeout = 300
    start = time.perf_counter()
    decoder = instance_decoder.Decoder()
    decoder.decode_reduced()
    instances = decoder.instances

    with concurrent.futures.ProcessPoolExecutor(max_workers=round(multiprocessing.cpu_count() * 0.8)) as executor:
        results = executor.map(solve, [(inst, algo, timeout) for inst in instances for algo in algos])
        for r in results:
            write_data(r, name)

    finish = time.perf_counter()
    print(f'Finished in {round(finish - start, 2)} second(s)')


if __name__ == "__main__":
    multi_run()
