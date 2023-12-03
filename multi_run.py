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
    args = [0, 'BFS']
    name = 'scratch'
    timeout = 20
    decoder = instance_decoder.Decoder()
    decoder.decode_reduced(size_higher_bound=30, types_allowed=('FR'))
    inst = decoder.instances[int(args[0])]
    # Inst_visualizer.vis3(inst, name)
    algo = str(args[1])
    print("\n" + inst.name + " with " + algo + " starts")
    run_solver(inst, algo, timeout)


def solve(*args):
    write_data(run_solver(args[0], args[1], args[2]), args[3])


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
    computer = "loc" if multiprocessing.cpu_count() < 10 else "ser"
    name = 'dec_3_' + computer
    timeout = 600
    start = time.perf_counter()
    decoder = instance_decoder.Decoder()
    decoder.decode_reduced()
    instances = decoder.instances
    max_workers = round(multiprocessing.cpu_count() * 0.2)

    # with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    # round(multiprocessing.cpu_count() * 0.8)) as executor:
    #     results = executor.map(solve, [(inst, algo, timeout) for inst in instances for algo in algos])
    #     for r in results:
    #         write_data(r, name)
    print(f"Starting multi-run. \nTimeout: {timeout}\n "
          f"Algorithms: {algos}\n Max workers: {max_workers}\n"
          f"Instances: {len(instances)}")

    processes = []
    for inst in instances:
        for algo in algos:
            p = multiprocessing.Process(target=solve, args=(inst, algo, timeout, name))
            p.start()
            processes.append(p)
            if len(processes) >= max_workers:
                while all([p.is_alive() for p in processes]) or len(processes) >= max_workers :
                    print("Waiting for a process to finish...")
                    time.sleep(10)

                for p in processes:
                    if not p.is_alive():
                        processes.remove(processes[0])
                        print("Process removed. New process may start.")
                print(f"number of processes: {len(processes)}")
    finish = time.perf_counter()
    print(f'Finished in {round(finish - start, 2)} second(s)')


if __name__ == "__main__":
    multi_run()
