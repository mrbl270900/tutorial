#!/bin/bash

# Define the number of times to run the scripts
total_runs=400
log_file="script.log"
last_lines_Sim=()

# Function to read the last line of a log file
read_last_line() {
    tail -n 1 "$1"
}

# Loop to run the first Python script
for ((i=1; i<=$total_runs; i++))
do
    echo "Running CreateXml.py - Iteration $i"
    python CreateXml.py

    echo "Running Simulation.py - Iteration $i"
    output=$(python Simulation.py NetworkSetup.xml ServerSetup.xml)
    last_line=$(echo "$output" | tail -n 1)
    last_lines_Sim+=("$last_line")
done

echo "Last lines of sim:"
printf '%s\n' "${last_lines_Sim[@]}"