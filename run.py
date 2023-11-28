import pandas as pd
import sys

# import instance_collector
# import Inst_visualizer
import instance_decoder
# import THIRD_instance_collector as collector
import Solver

'''
Run using :
    
for i in {0..n}; do for strategy in 'MCTS_D' 'MCTS_S' 'BFS' 'BNB' 'BNBL'; do for preprocessing in {0..1}; do python3 run.py $i $strategy $preprocessing & done done done

    
where n is the last index of old_instances i instance collector.
'''


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
    solver = Solver.Solver()
    solver.dup_det = dup_det
    solver.NUMBER_OF_SIMULATIONS = 9999999
    solver.JUMP = solver.NUMBER_OF_SIMULATIONS / min(solver.NUMBER_OF_SIMULATIONS, 20)
    solver.timeout = timeout
    solution = None
    if algo == 'MCTS_E':
        solution = solver.emp_mcts(inst)
    if algo == 'MCTS_V':
        solution = solver.vector_mcts(inst)
    if algo == 'MCTS_S':
        solution = solver.semi_emp_mcts(inst)
    if algo == 'BFS':
        solver.type = 'U1S'
        solution = solver.bfs(inst)
    if algo == 'BNBL':
        solver.type = 'U1S'
        solution = solver.branch_and_bound(inst, solver.upper_bound_base_plus_utility,
                                           solver.lower_bound_base_plus_utility)
    if algo == 'BNB':
        solver.type = 'U1S'
        solution = solver.branch_and_bound(inst, solver.upper_bound_base_plus_utility)
    if algo == 'GBFS':
        solver.type = 'U1S'
        solution = solver.greedy_best_first_search(inst)
    timestamps = solution.timestamps
    states = solution.states
    solver.type = 'U1S'
    solution.set_rewards(solver, inst)
    res = tuple(zip(solution.rewards, solution.states_collector, timestamps, ))
    fin_res = solution.rewards[-1] if len(solution.rewards) > 0 else default
    time = timestamps[-1] if not solution.interrupted else default
    return fin_res, time, res, states, inst, algo


def main():
    args = sys.argv[1:]
    # args = [0, 'MCTS_V']
    name = 'nov_27_2023_30mins_all'
    # name = 'scratch'
    decoder = instance_decoder.Decoder()
    decoder.decode_reduced()
    inst = decoder.instances[int(args[0])]
    # Inst_visualizer.vis3(inst, name)
    algo = str(args[1])
    # preprocessing = int(args[2])
    preprocessing = 0
    print("\n" + inst.name + " with " + algo + " starts")

    r = run_solver(inst, algo)
    write_data(r, name)


if __name__ == "__main__":
    main()
