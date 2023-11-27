#!/bin/bash

# Define the number of processes and strategies

if [ -n "$1" ] && [ -n "$2" ]; then
    start_index=$1
    end_index=$2
else
    if [ -n "$1" ]; then
        start_index=0
        end_index=$(($1 - 1))
    else
        start_index=0
        end_index=172
    fi
fi

algos=(
 'BFS'
 'BNB'
 'BNBL'
 'MCTS_V'
 'MCTS_E'
 'MCTS_S'
 'GBFS'
 )


# Loop through processes and strategies
for i in $(seq $start_index $end_index); do
    for algo in "${algos[@]}"; do
        python3 run.py "$i" "$algo"  &
    done
done

# Wait for all background processes to finish
wait
