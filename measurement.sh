#!/bin/bash

# --------------------------------------------------------------------------------

# measurement function and its utilities



# --------------------------------------------------------------------------------

function measurement {
    local scenario=$1
    local result_directory=$2
    local output_file_index=$3
    local agt_log=$4
    local pwr_log=$5
    local dc_mode=$6
    local debug_mode=$7

    if [ "$dc_mode" = true ]
    then
        if [ "$debug_mode" = true ]
        then
            echo -e "${INFO}(DEBUG MODE) disable ac${ENDFORMAT}"
            python cros_automation.py disable-ac -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE --debug

            echo -e "${INFO}(DEBUG MODE) wait 60 seconds for disabling ac to exit${ENDFORMAT}"
            sleep_with_progress_bar 60
        else
            echo -e "${INFO}disable ac${ENDFORMAT}"
            python cros_automation.py disable-ac -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE

            echo -e "${INFO}wait 60 seconds for disabling ac to exit${ENDFORMAT}"
            sleep_with_progress_bar 60
        fi
    fi

    if [ "$debug_mode" = true ]
    then
        echo -e "${INFO}(DEBUG MODE) prepare ${scenario}${ENDFORMAT}"
        python cros_automation.py prepare-scenario -s $scenario -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE --debug

        echo -e "${INFO}(DEBUG MODE) launch ${scenario}${ENDFORMAT}"
        python cros_automation.py launch-scenario -s $scenario -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE --debug
    else
        echo -e "${INFO}prepare ${scenario}${ENDFORMAT}"
        python cros_automation.py prepare-scenario -s $scenario -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE

        echo -e "${INFO}launch ${scenario}${ENDFORMAT}"
        python cros_automation.py launch-scenario -s $scenario -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE

        if [ "$agt_log" = true ]
        then
            echo -e "${INFO}start agt internal logging to $AGT_INTERNAL_PATH/agt_int_$output_file_index.csv${ENDFORMAT}"
            python cros_automation.py agt-internal-log -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -t ${AUTOTEST_DURATION[$scenario]} -o "agt_int_$output_file_index.csv"
        fi
    fi

    # wait 300s before downloading results
    if [ "$debug_mode" = true ]
    then
        echo -e "${INFO}(DEBUG MODE) wait 300 seconds for $scenario to exit${ENDFORMAT}"
        sleep_with_progress_bar 300
    else
        echo -e "${INFO}wait ${AUTOTEST_DURATION[$scenario]} seconds for $scenario to finish${ENDFORMAT}"
        sleep_with_progress_bar ${AUTOTEST_DURATION[$scenario]}

        echo -e "${INFO}wait 300 seconds for data logging to exit${ENDFORMAT}"
        sleep_with_progress_bar 300
    fi

    if [ "$debug_mode" = true ]
    then
        echo -e "${INFO}(DEBUG MODE) download ${AUTOTEST_RESULT_DIR[$scenario]}/keyval to $result_directory${ENDFORMAT}"
        python cros_automation.py download -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "${AUTOTEST_RESULT_DIR[$scenario]}/keyval" -o "$result_directory/keyval_$output_file_index"

        echo -e "${INFO}(DEBUG MODE) download ${AUTOTEST_RESULT_DIR[$scenario]}/results-chart.json to $result_directory${ENDFORMAT}"
        python cros_automation.py download -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "${AUTOTEST_RESULT_DIR[$scenario]}/results-chart.json" -o "$result_directory/results_chart_$output_file_index.json"

        echo -e "${INFO}(DEBUG MODE) rm ${AUTOTEST_RESULT_DIR[$scenario]}/keyval on $DUT_IP${ENDFORMAT}"
        python cros_automation.py rm -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "${AUTOTEST_RESULT_DIR[$scenario]}/keyval"

        echo -e "${INFO}(DEBUG MODE) rm ${AUTOTEST_RESULT_DIR[$scenario]}/results-chart.json on $DUT_IP${ENDFORMAT}"
        python cros_automation.py rm -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "${AUTOTEST_RESULT_DIR[$scenario]}/results-chart.json"

        echo -e "${INFO}(DEBUG MODE) ls ${AUTOTEST_RESULT_DIR[$scenario]} on $DUT_IP${ENDFORMAT}"
        python cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d ${AUTOTEST_RESULT_DIR[$scenario]}
    else
        echo -e "${INFO}download ${AUTOTEST_RESULT_DIR[$scenario]}/keyval to $result_directory${ENDFORMAT}"
        python cros_automation.py download -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "${AUTOTEST_RESULT_DIR[$scenario]}/keyval" -o "$result_directory/keyval_$output_file_index"

        echo -e "${INFO}download ${AUTOTEST_RESULT_DIR[$scenario]}/results-chart.json to $result_directory${ENDFORMAT}"
        python cros_automation.py download -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "${AUTOTEST_RESULT_DIR[$scenario]}/results-chart.json" -o "$result_directory/results_chart_$output_file_index.json"

        if [ "$agt_log" = true ]
        then
            echo -e "${INFO}download $AGT_INTERNAL_PATH/agt_int_$output_file_index.csv to $result_directory${ENDFORMAT}"
            python cros_automation.py download -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "$AGT_INTERNAL_PATH/agt_int_$output_file_index.csv" -o "$result_directory/agt_int_$output_file_index.csv"

            echo -e "${INFO}rm $AGT_INTERNAL_PATH/agt_int_$output_file_index.csv on $DUT_IP${ENDFORMAT}"
            python cros_automation.py rm -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "$AGT_INTERNAL_PATH/agt_int_$output_file_index.csv"

            echo -e "${INFO}ls ${AUTOTEST_RESULT_DIR[$scenario]} on $DUT_IP${ENDFORMAT}"
            python cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d $AGT_INTERNAL_PATH
        fi
    fi


    if [ "$dc_mode" = true ]
    then
        if [ "$debug_mode" = true ]
        then
            echo -e "${INFO}(DEBUG MODE) re-enable ac${ENDFORMAT}"
            python cros_automation.py enable-ac -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE --debug

            echo -e "${INFO}(DEBUG MODE) wait 60 seconds for enabling ac to exit${ENDFORMAT}"
            sleep_with_progress_bar 60
        else
            echo -e "${INFO}re-enable ac${ENDFORMAT}"
            python cros_automation.py enable-ac -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE

            echo -e "${INFO}wait 60 seconds for enabling ac to exit${ENDFORMAT}"
            sleep_with_progress_bar 60
        fi
    fi
}
