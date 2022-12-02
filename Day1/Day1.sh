#!/bin/bash
# Script to solve Day 1 of Advent of Code 2022
# Usage: bash Day1.sh input_file

# Variables to store highest three sums
let max=next_to_max=nn_to_max=0
# Parse input
while read -r line; do
# If line is not empty
if [ -z "$line" ]
then
    # Store highest three sums in order
    if (( sum > max ))
    then
        let max=$sum
    else
        if (( sum > next_to_max ))
        then
            let next_to_max=$sum
        else
            if (( sum > nn_to_max ))
            then
                let nn_to_max=$sum
            fi
        fi
    fi
    # Reset sum
    let sum=0
else
    # Add next count to sum
    let sum="$((sum+$line))"
fi
done < $1
#### Part 1 ####
echo "Part 1:" $max
#### Part 2 ####
# Sum of three highest
echo "Part 2:" "$((max+next_to_max+nn_to_max))"
