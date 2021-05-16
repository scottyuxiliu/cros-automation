function measurement {
    <#
    .SYNOPSIS
        if debug mode is enabled, all logging will be disabled

    .INPUTS
        scenario
    #>

    param (
        [Parameter(Mandatory=$true)] [string] $scenario,
        [Parameter(Mandatory=$true)] [string] $result_directory,
        [Parameter(Mandatory=$true)] [int] $cur_file_index,
        [Parameter(Mandatory=$true)] [int] $file_index_offset,
        [Parameter(Mandatory=$true)] [bool] $agt_log,
        [Parameter(Mandatory=$true)] [bool] $pwr_log,
        [Parameter(Mandatory=$true)] [bool] $debug_mode
    )

    if ($SCENARIO_CONST.ContainsKey($scenario)) {
        # ----------------------------------------------------------------------
        # launch sequence: prepare scenario -> agt -> launch scenario -> pwr

        if ($debug_mode) {
            Write-Verbose "(DEBUG MODE) prepare $scenario ..."
            python.exe .\cros_automation.py prepare-scenario -s $scenario -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE --debug

            Write-Verbose "(DEBUG MODE) launch $scenario ..."
            python.exe .\cros_automation.py launch-scenario -s $scenario -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE --debug
        }
        else {
            Write-Verbose "prepare $scenario ..."
            python.exe .\cros_automation.py prepare-scenario -s $scenario -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE
    
            if ($agt_log) {
                Write-Verbose "start agt internal logging to $AGT_PATH/pm_log_$($cur_file_index+$file_index_offset).csv ..."
                python.exe .\cros_automation.py agt-internal-log -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -t $SCENARIO_CONST.Item($scenario).Item("agt_log_time") -o "pm_log_$($cur_file_index+$file_index_offset).csv"
            }
    
            Write-Verbose "launch $scenario ..."
            python.exe .\cros_automation.py launch-scenario -s $scenario -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE
    
            if ($pwr_log) {
                get_power_data -url $DAQTOOL_URL -config $DAQ_CONFIG -duration $SCENARIO_CONST.Item($scenario).Item("pwr_log_time") -i $cur_file_index -offset $file_index_offset -result_directory $result_directory -source $DAQTOOL_OUTPUT_DIR
            }
        }

        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # log

        if ($debug_mode) {
            Write-Verbose "(DEBUG MODE) wait 60 seconds ..."
            sleep_with_progress_bar -seconds 60
        }
        else {
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
        }

        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # output result

        if ($debug_mode) {
            Write-Verbose "(DEBUG MODE) download $scenario result keyval $($SCENARIO_CONST.Item($scenario).Item('result'))/keyval to $result_directory ..."
            python .\cros_automation.py download -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "$($SCENARIO_CONST.Item($scenario).Item('result'))/keyval" -o "$result_directory\keyval_$($cur_file_index+$file_index_offset)"

            Write-Verbose "(DEBUG MODE) remove $scenario result keyval $($SCENARIO_CONST.Item($scenario).Item('result'))/keyval ..."
            python .\cros_automation.py rm -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "$($SCENARIO_CONST.Item($scenario).Item('result'))/keyval"

            Write-Verbose "(DEBUG MODE) download $scenario result results-chart.json $($SCENARIO_CONST.Item($scenario).Item('result'))/results-chart.json to $result_directory ..."
            python .\cros_automation.py download -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "$($SCENARIO_CONST.Item($scenario).Item('result'))/results-chart.json" -o "$result_directory\results_chart_$($cur_file_index+$file_index_offset).json"

            Write-Verbose "(DEBUG MODE) remove $scenario result results-chart.json $($SCENARIO_CONST.Item($scenario).Item('result'))/results-chart.json ..."
            python .\cros_automation.py rm -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "$($SCENARIO_CONST.Item($scenario).Item('result'))/results-chart.json"

            Write-Verbose "(DEBUG MODE) list items in $($SCENARIO_CONST.Item($scenario).Item('result')) ..."
            python .\cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "$($SCENARIO_CONST.Item($scenario).Item('result'))"
        }
        else {
            if ($SCENARIO_CONST.Item($scenario).Item('result') -ne "na") {
                Write-Verbose "download $scenario result keyval $($SCENARIO_CONST.Item($scenario).Item('result'))/keyval to $result_directory ..."
                python .\cros_automation.py download -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "$($SCENARIO_CONST.Item($scenario).Item('result'))/keyval" -o "$result_directory\keyval_$($cur_file_index+$file_index_offset)"
        
                Write-Verbose "download $scenario result results-chart.json $($SCENARIO_CONST.Item($scenario).Item('result'))/results-chart.json to $result_directory ..."
                python .\cros_automation.py download -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "$($SCENARIO_CONST.Item($scenario).Item('result'))/results-chart.json" -o "$result_directory\results_chart_$($cur_file_index+$file_index_offset).json"
        
                Write-Verbose "list items in $($SCENARIO_CONST.Item($scenario).Item('result')) ..."
                python .\cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "$($SCENARIO_CONST.Item($scenario).Item('result'))"
            }
    
            if ($agt_log) {
                Write-Verbose "download agt internal log $AGT_PATH/pm_log_$($cur_file_index+$file_index_offset).csv to $result_directory ..."
                python .\cros_automation.py download -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "$AGT_PATH/pm_log_$($cur_file_index+$file_index_offset).csv" -o "$result_directory\pm_log_$($cur_file_index+$file_index_offset).csv"
                
                Write-Verbose "remove agt internal log $AGT_PATH/pm_log_$($cur_file_index+$file_index_offset).csv on the test system ..."
                python .\cros_automation.py rm -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "$AGT_PATH/pm_log_$($cur_file_index+$file_index_offset).csv"
                
                Write-Verbose "list items in $AGT_PATH ..."
                python .\cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "$AGT_PATH"
            }
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