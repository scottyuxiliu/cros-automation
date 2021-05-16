#!/bin/bash

# --------------------------------------------------------------------------------

# measurement function


# --------------------------------------------------------------------------------

function measurement {
    local scenario=$1
    local duration=$2
    local result_directory=$3
    local output_file=$4
    local agt_log=$5
    local pwr_log=$6
    local debug_mode=$7

    if [ "$debug_mode" = true ]
    then
        echo -e "${INFO}(DEBUG MODE) prepare ${scenario}${ENDFORMAT}"
        python cros_automation.py prepare-scenario -s $scenario -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE --debug

        echo -e "${INFO}(DEBUG MODE) launch ${scenario}${ENDFORMAT}"
        python cros_automation.py launch-scenario -s $scenario -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE --debug
    else
        echo -e "${INFO}prepare ${scenario}${ENDFORMAT}"
        python cros_automation.py prepare-scenario -s $scenario -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE

        if [ "$agt_log" = true ]
        then
            echo -e "${INFO}start agt internal logging to $AGT_INTERNAL_PATH/${output_file}${ENDFORMAT}"
            python cros_automation.py agt-internal-log -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -t $duration -o $output_file
        else
            :
        fi

        echo -e "${INFO}launch ${scenario}${ENDFORMAT}"
        python cros_automation.py launch-scenario -s $scenario -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE
    fi

    if [ "$debug_mode" = true ]
    then
        echo -e "${INFO}(DEBUG MODE) wait 60 seconds for $scenario to exit${ENDFORMAT}"
        sleep 60s
    else
        echo -e "${INFO}wait $duration seconds${ENDFORMAT}"
        sleep $duration

        echo -e "${INFO}wait 60 seconds for data logging to finish${ENDFORMAT}"
        sleep 60s
    fi

    
}