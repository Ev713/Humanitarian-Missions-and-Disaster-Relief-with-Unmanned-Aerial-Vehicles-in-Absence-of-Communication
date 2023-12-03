'''
processes = []
    max_workers = 2  # round(multiprocessing.cpu_count() * 0.5)
    counter = 0
    for inst in instances:
        for algo in algos:
            p = multiprocessing.Process(target=solve, args=(inst, algo, timeout, name))
            p.start()
            processes.append(p)
            counter += 1
            while len(processes) >= max_workers:
                processes[0].join()
                processes.remove(processes[0])
'''

MAX_WORKERS=5
COUNTER=0
INSTS=172
for i in $(seq 1 $INSTS);
do
python 3 multirun.py $i;
done