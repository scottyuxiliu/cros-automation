function measurement {
    param (
        [Parameter(Mandatory=$true)] [string] $scenario,
        [Parameter(Mandatory=$true)] [string] $result_directory,
        [Parameter(Mandatory=$true)] [int] $cur_file_index,
        [Parameter(Mandatory=$true)] [int] $file_index_offset,
        [Parameter(Mandatory=$true)] [bool] $agt_log,
        [Parameter(Mandatory=$true)] [bool] $pwr_log
    )

    if ($SCENARIO_CONST.ContainsKey($scenario)) {
        # ----------------------------------------------------------------------
        # launch sequence: prepare scenario -> agt -> launch scenario -> pwr

        Write-Verbose "prepare $scenario ..."
        python.exe .\cros_automation.py prepare-scenario -s $scenario -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE

        if ($agt_log) {
            Write-Verbose "start agt internal logging to $TEST_SYS_AGT_PATH/pm_log_$($cur_file_index+$file_index_offset).csv ..."
            python.exe .\cros_automation.py agt-internal-log -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -t $SCENARIO_CONST.Item($scenario).Item("agt_log_time") -o "pm_log_$($cur_file_index+$file_index_offset).csv"
        }

        Write-Verbose "launch $scenario ..."
        python.exe .\cros_automation.py launch-scenario -s $scenario -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE

        if ($pwr_log) {
            get_power_data -url $DAQTOOL_URL -config $DAQ_CONFIG -duration $SCENARIO_CONST.Item($scenario).Item("pwr_log_time") -i $cur_file_index -offset $file_index_offset -result_directory $result_directory -source $DAQTOOL_OUTPUT_DIR
        }

        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # log

        if ($agt_log) {
            Write-Verbose "wait $($SCENARIO_CONST.Item($scenario).Item('agt_log_time')) seconds for $scenario to finish ..."
            sleep_with_progress_bar -seconds $SCENARIO_CONST.Item($scenario).Item("agt_log_time")
        }
        elseif ($pwr_log) {
            Write-Verbose "wait $($SCENARIO_CONST.Item($scenario).Item('pwr_log_time')) seconds for $scenario to finish ..."
            sleep_with_progress_bar -seconds $SCENARIO_CONST.Item($scenario).Item("pwr_log_time")
        }
        else {
            Write-Verbose "wait $($SCENARIO_CONST.Item($scenario).Item('duration')) seconds for $scenario to finish ..."
        }

        Write-Verbose "wait 60 seconds for data logging to finish ..."
        sleep_with_progress_bar -seconds 60

        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # output result

        Write-Verbose "download $scenario result keyval $TEST_SYS_AUTOTEST_PATH/$($SCENARIO_CONST.Item($scenario).Item('result'))/keyval to $result_directory ..."
        python .\cros_automation.py download -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "$TEST_SYS_AUTOTEST_PATH/$($SCENARIO_CONST.Item($scenario).Item('result'))/keyval" -o "$result_directory\keyval_$($cur_file_index+$file_index_offset)"

        Write-Verbose "list items in $TEST_SYS_AUTOTEST_PATH/$($SCENARIO_CONST.Item($scenario).Item('result')) ..."
        python .\cros_automation.py ls -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "$TEST_SYS_AUTOTEST_PATH/$($SCENARIO_CONST.Item($scenario).Item('result'))"

        if ($agt_log) {
            Write-Verbose "download agt internal log $TEST_SYS_AGT_PATH/pm_log_$($cur_file_index+$file_index_offset).csv to $result_directory ..."
            python .\cros_automation.py download -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "$TEST_SYS_AGT_PATH/pm_log_$($cur_file_index+$file_index_offset).csv" -o "$result_directory\pm_log_$($cur_file_index+$file_index_offset).csv"
            
            Write-Verbose "remove agt internal log $TEST_SYS_AGT_PATH/pm_log_$($cur_file_index+$file_index_offset).csv on the test system ..."
            python .\cros_automation.py remove -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "$TEST_SYS_AGT_PATH/pm_log_$($cur_file_index+$file_index_offset).csv"
            
            Write-Verbose "list items in $TEST_SYS_AGT_PATH ..."
            python .\cros_automation.py ls -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "$TEST_SYS_AGT_PATH"
        }

        # ----------------------------------------------------------------------

    }
    else {
        Write-Verbose "$scenario is not supported. supported scenarios are as follows:"
        foreach ($key in $SCENARIO_CONST.Keys) {
            Write-Verbose "$key"
        }
    }
}