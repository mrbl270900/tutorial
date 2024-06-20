#!/bin/bash

# Define the number of times to run the scripts
total_runs=145
last_lines_Sim=()

# Loop to run the first Python script
for ((i=1; i<=$total_runs; i++))
do
    #echo "Running CreateXml.py - Iteration $i"
    python CreateXml.py

    #echo "Running Simulation.py - Iteration $i"
    #python Simulation.py NetworkSetup.xml ServerSetup.xml > temp_output.txt
    #last_line=$(tail -n 1 temp_output.txt)
    #echo "$last_line"
    #last_lines_Sim+=("$last_line")
    #rm temp_output.txt
done

#echo "Last lines of sim:"
#printf '%s\n' "${last_lines_Sim[@]}"