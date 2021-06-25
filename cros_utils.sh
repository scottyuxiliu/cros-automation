#!/bin/bash

# --------------------------------------------------------------------------------

# util functions for bash scripts


# --------------------------------------------------------------------------------


function sleep_with_progress_bar {
    local i
    
    for i in `seq 1 $1`
    do
        local bar="##############################"
        local barlength=${#bar}
        local n=$(($i*$barlength/$1)) # arithmetic requires double brackets
        if [ $n -lt 1 ]
        then
            n=1
        fi
        # echo "$barlength"
        printf "\r${INFO}[%-${barlength}s] %ds/%ds ${ENDFORMAT}" ${bar:0:n} $i $1
        sleep 1
    done

    printf "\n"
}