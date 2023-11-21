#!/bin/bash

# Define the number of processes and strategies

if [ -n "$1" ] && [ -n "$2" ]; then
    start_index = $1
    end_index = $2
else
    if[ -n "$1"]; then
        start_index = 0
        end_inedx = $1
    else
        start_index = 0
        end_index = 172
    fi
fi

algos=('BFS' 'BNB' 'BNBL' 'MCTS_V' 'MCTS_E' 'GBFS' )

num_algos=${#algos[@]}
cpu_limit_percent=80
cpu_limit_per_process=$(echo "scale=2; $cpu_limit_percent / ($end_index-$start_index + 1) / $num_algos" | bc)

# Loop through processes and strategies
for i in $(seq 0 $n); do
    for algo in "${algos[@]}"; do
            python3 run.py "$i" "$algo"  &
            pid=$!
            cpulimit --pid=$pid --limit=$cpu_limit_per_process &
    done
done

# Wait for all background processes to finish
wait
