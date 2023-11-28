import concurrent.futures
import multiprocessing
import time
from multiprocessing import Process

import pandas as pd

import instance_decoder
import run

algos = [
    'MCTS_E',
    'MCTS_V',
    'MCTS_S',
    'BFS',
    'BNBL',
    'BNB',
    'GBFS'
]
name = 'scratch'
timeout = 300
# with multiprocessing.Pool(num_of_inst * len(algos)) as p:
#        p.map(run.main, [(i_id, algo) for i_id in range(num_of_inst) for algo in algos])
start = time.perf_counter()
decoder = instance_decoder.Decoder()
decoder.decode_reduced()
instances = decoder.instances
preprocessing = 0


# processes = []
# for i_id in range(num_of_inst):
#    for algo in algos:
#        p = Process(target=run.main, args=(i_id, algo))
#        p.start()
#        processes.append(p)

# for p in processes:
#    p.join()
def solve(args):
    return run.run_solver(args[0], args[1], args[2])


with concurrent.futures.ProcessPoolExecutor(max_workers=round(multiprocessing.cpu_count() * 0.8)) as executor:
    results = executor.map(solve, [(inst, algo, timeout) for inst in instances for algo in algos])
    for r in results:
        run.write_data(r, name)

finish = time.perf_counter()
print(f'Finished in {round(finish - start, 2)} second(s)')
