#!/bin/bash

# --------------------------------------------------------------------------------

# you may run this bash script from terminal as following
# source cleanup_logfile.sh

# for example
# source cleanup_logfile.sh


# --------------------------------------------------------------------------------

source cros_constants.sh

for i in ${LOGS[@]}
do
    echo -e "${INFO}remove $i${ENDFORMAT}"

    if [ -f $i ] # need to have spaces after "[" and before "]"
    then
        rm $i
    else
        echo -e "${ERROR}no such file: $i${ENDFORMAT}"
    fi

done
