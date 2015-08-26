#!/bin/sh

set -e

input='README.md'
output='README.md.out'

for p_rate in 0 0.2 0.5 0.9
do
    echo '### Testing with P =' $p_rate
    rm -f "$output"
    ./run-everything.sh "$input" "$output" $p_rate
    if diff -U3 "$input" "$output"
    then
        echo '--- ok'
        echo
    else
        echo '!!! FAILED'
        exit 1
    fi
done

rm -f "$output"
