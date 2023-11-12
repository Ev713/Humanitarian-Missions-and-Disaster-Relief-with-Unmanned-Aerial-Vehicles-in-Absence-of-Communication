#!/bin/bash

# Define the number of processes and strategies
if [ -n "$1" ]; then
    n=$(($1 - 1))
else
    n=60  # Default value if not provided
fi

strategies=('BFS' 'BNB' 'BNBL')

# Loop through processes and strategies
for i in $(seq 0 $n); do
    for strategy in "${strategies[@]}"; do
        for preprocessing in 0; do
            python3 run.py "$i" "$strategy" "$preprocessing" &
        done
    done
done

# Wait for all background processes to finish
wait
