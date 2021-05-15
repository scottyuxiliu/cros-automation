#!/bin/bash

# --------------------------------------------------------------------------------

# you may run this bash script from terminal as following
# source agt_internal_log.sh [TEST_SYS_IP] [DURATION] [DIR] [OUTPUT]

# for example
# source agt_internal_log.sh "192.168.123.456" "60" "/home/scottyuxiliu/Downloads/" "agt_internal_log.csv"


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
