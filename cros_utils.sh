#!/bin/bash

# --------------------------------------------------------------------------------

# util functions for bash scripts


# --------------------------------------------------------------------------------


function sleep_with_progress_bar {
    local i
    
    for i in `seq 1 $1`
    do
        bar="################################################################################"
        barlength=${#bar}
        n=$(($i*$barlength/$1))
        printf "\r${INFO}[%-${barlength}s] %ds/%ds ${ENDFORMAT}" ${bar:0:n} $i $1
        sleep 1
    done

    printf "\n"
}