#!/bin/bash

# --------------------------------------------------------------------------------

# measurement function


# --------------------------------------------------------------------------------

function measurement {
    local scenario=$1
    local duration=$2
    local result_directory=$3
    local cur_file_index=$4
    local file_index_offset=$5
    local agt_log=$6
    local pwr_log=$7
    local debug_mode=$8

    if [ "$debug_mode" = true ]
    then
        echo -e "${INFO}(DEBUG MODE) prepare ${scenario}${ENDFORMAT}"
        python cros_automation.py prepare-scenario -s $scenario -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE --debug

        echo -e "${INFO}(DEBUG MODE) launch ${scenario}${ENDFORMAT}"
        python cros_automation.py launch-scenario -s $scenario -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE --debug
    else
        echo -e "${INFO}prepare ${scenario}${ENDFORMAT}"
        python cros_automation.py prepare-scenario -s $scenario -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE

        if [ "$agt_log" = true ]
        then
            echo -e "${INFO}start agt internal logging to $AGT_INTERNAL_PATH/agt_internal_log_$($cur_file_index+$file_index_offset).csv${ENDFORMAT}"
            python cros_automation.py agt-internal-log -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -t $DURATION -o $OUTPUT
        else
        fi
    fi
}