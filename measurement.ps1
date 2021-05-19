
# --------------------------------------------------------------------------------

# measurement function and its utilities



# --------------------------------------------------------------------------------
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
        [Parameter(Mandatory=$true)] [bool] $dc_mode,
        [Parameter(Mandatory=$true)] [bool] $debug_mode
    )

    if ($SCENARIO_CONST.ContainsKey($scenario)) {

        if ($dc_mode) {
            if ($debug_mode) {
                Write-Host "INFO`t: (DEBUG MODE) disable ac" -ForegroundColor Green
                python cros_automation.py disable-ac -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE

                Write-Host "INFO`t: (DEBUG MODE) wait 60 seconds for disabling ac to exit" -ForegroundColor Green
                sleep_with_progress_bar -seconds 60
            }
            else {
                Write-Host "INFO`t: disable ac" -ForegroundColor Green
                python cros_automation.py disable-ac -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE

                Write-Host "INFO`t: wait 60 seconds for disabling ac to exit" -ForegroundColor Green
                sleep_with_progress_bar -seconds 60
            }
        }

        # ----------------------------------------------------------------------
        # launch sequence: prepare scenario -> launch scenario -> agt -> pwr

        if ($debug_mode) {
            Write-Host "INFO`t: (DEBUG MODE) prepare $scenario" -ForegroundColor Green
            python cros_automation.py prepare-scenario -s $scenario -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE --debug

            Write-Host "INFO`t: (DEBUG MODE) launch $scenario" -ForegroundColor Green
            python cros_automation.py launch-scenario -s $scenario -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE --debug
        }
        else {
            Write-Host "INFO`t: prepare $scenario" -ForegroundColor Green
            python cros_automation.py prepare-scenario -s $scenario -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE
            
            Write-Host "INFO`t: launch $scenario" -ForegroundColor Green
            python cros_automation.py launch-scenario -s $scenario -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE
            
            if ($SCENARIO_CONST.Item($scenario).Item('delay') -ne 0) {
                Write-Host "INFO`t: wait $($SCENARIO_CONST.Item($scenario).Item('delay')) seconds before starting any data logging" -ForegroundColor Green
                sleep_with_progress_bar -seconds $($SCENARIO_CONST.Item($scenario).Item('delay'))
            }
            
            if ($agt_log) {
                Write-Host "INFO`t: start agt internal logging to $AGT_INTERNAL_PATH/agt_internal_log_$($cur_file_index+$file_index_offset).csv" -ForegroundColor Green
                python cros_automation.py agt-internal-log -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -t $SCENARIO_CONST.Item($scenario).Item("agt_log_time") -o "agt_internal_log_$($cur_file_index+$file_index_offset).csv"
            }

            if ($pwr_log) {
                Write-Host "INFO`t: start pac logging on $HOST_IP" -ForegroundColor Green
                python cros_automation.py pac-log -p $HOST_IP -u $HOST_USERNAME -k $HOST_SSH_KEYFILE -t $SCENARIO_CONST.Item($scenario).Item('pwr_log_time') --password "power"
            }
        }

        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # wait

        if ($debug_mode) {
            Write-Host "INFO`t: (DEBUG MODE) wait 60 seconds for operation to exit" -ForegroundColor Green
            sleep_with_progress_bar -seconds 60
        }
        else {
            $times = @($SCENARIO_CONST.Item($scenario).Item('duration'))
            if ($agt_log) {
                $times += $SCENARIO_CONST.Item($scenario).Item('agt_log_time')
            }
            if ($pwr_log) {
                $times += $SCENARIO_CONST.Item($scenario).Item('pwr_log_time')
            }

            $longest = $times | Measure-Object -Maximum
            $longest = $longest.Maximum

            if ($pwr_log) {
                if ( $agt_log -and ($longest -eq $SCENARIO_CONST.Item($scenario).Item('agt_log_time')) ) {
                    Write-Host "INFO`t: wait $($SCENARIO_CONST.Item($scenario).Item('agt_log_time') - $SCENARIO_CONST.Item($scenario).Item('pwr_log_time')) seconds for agt internal logging to finish" -ForegroundColor Green
                    sleep_with_progress_bar -seconds $($SCENARIO_CONST.Item($scenario).Item('agt_log_time') - $SCENARIO_CONST.Item($scenario).Item('pwr_log_time'))
                }
                elseif ( ($longest -eq $SCENARIO_CONST.Item($scenario).Item('duration')) -and ($SCENARIO_CONST.Item($scenario).Item('duration') -ne $SCENARIO_CONST.Item($scenario).Item('pwr_log_time')) ) {
                    Write-Host "INFO`t: wait $($SCENARIO_CONST.Item($scenario).Item('duration') - $SCENARIO_CONST.Item($scenario).Item('pwr_log_time')) seconds for $scenario to finish" -ForegroundColor Green
                    sleep_with_progress_bar -seconds $($SCENARIO_CONST.Item($scenario).Item('duration') - $SCENARIO_CONST.Item($scenario).Item('pwr_log_time'))
                }
                else {
    
                }
                
            }
            else {
                if ($agt_log) {
                    Write-Host "INFO`t: wait $($SCENARIO_CONST.Item($scenario).Item('agt_log_time')) seconds for agt internal logging to finish" -ForegroundColor Green
                    sleep_with_progress_bar -seconds $($SCENARIO_CONST.Item($scenario).Item('agt_log_time'))
                }
                else {
                    Write-Host "INFO`t: wait $($SCENARIO_CONST.Item($scenario).Item('duration')) seconds for $scenario to finish" -ForegroundColor Green
                    sleep_with_progress_bar -seconds $($SCENARIO_CONST.Item($scenario).Item('duration'))
                }
            }

            
    
            Write-Host "INFO`t: wait 60 seconds for operation to exit" -ForegroundColor Green
            sleep_with_progress_bar -seconds 60
        }

        # ----------------------------------------------------------------------

        # ----------------------------------------------------------------------
        # output result

        if ($debug_mode) {
            Write-Host "INFO`t: (DEBUG MODE) download $scenario keyval $($SCENARIO_CONST.Item($scenario).Item('result'))/keyval to $result_directory" -ForegroundColor Green
            python cros_automation.py download -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "$($SCENARIO_CONST.Item($scenario).Item('result'))/keyval" -o "$result_directory\keyval_$($cur_file_index+$file_index_offset)"

            Write-Host "INFO`t: (DEBUG MODE) remove $scenario keyval $($SCENARIO_CONST.Item($scenario).Item('result'))/keyval" -ForegroundColor Green
            python cros_automation.py rm -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "$($SCENARIO_CONST.Item($scenario).Item('result'))/keyval"

            Write-Host "INFO`t: (DEBUG MODE) download $scenario results-chart.json $($SCENARIO_CONST.Item($scenario).Item('result'))/results-chart.json to $result_directory" -ForegroundColor Green
            python cros_automation.py download -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "$($SCENARIO_CONST.Item($scenario).Item('result'))/results-chart.json" -o "$result_directory\results_chart_$($cur_file_index+$file_index_offset).json"

            Write-Host "INFO`t: (DEBUG MODE) remove $scenario results-chart.json $($SCENARIO_CONST.Item($scenario).Item('result'))/results-chart.json" -ForegroundColor Green
            python cros_automation.py rm -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "$($SCENARIO_CONST.Item($scenario).Item('result'))/results-chart.json"

            Write-Host "INFO`t: (DEBUG MODE) list items in $($SCENARIO_CONST.Item($scenario).Item('result'))" -ForegroundColor Green
            python cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "$($SCENARIO_CONST.Item($scenario).Item('result'))"
        }
        else {
            if ($SCENARIO_CONST.Item($scenario).Item('result') -ne "na") {
                Write-Host "INFO`t: download $scenario keyval $($SCENARIO_CONST.Item($scenario).Item('result'))/keyval to $result_directory" -ForegroundColor Green
                python cros_automation.py download -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "$($SCENARIO_CONST.Item($scenario).Item('result'))/keyval" -o "$result_directory\keyval_$($cur_file_index+$file_index_offset)"
        
                Write-Host "INFO`t: download $scenario results-chart.json $($SCENARIO_CONST.Item($scenario).Item('result'))/results-chart.json to $result_directory" -ForegroundColor Green
                python cros_automation.py download -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "$($SCENARIO_CONST.Item($scenario).Item('result'))/results-chart.json" -o "$result_directory\results_chart_$($cur_file_index+$file_index_offset).json"
        
                Write-Host "INFO`t: list items in $($SCENARIO_CONST.Item($scenario).Item('result'))" -ForegroundColor Green
                python cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "$($SCENARIO_CONST.Item($scenario).Item('result'))"
            }
    
            if ($agt_log) {
                Write-Host "INFO`t: download $AGT_INTERNAL_PATH/agt_internal_log_$($cur_file_index+$file_index_offset).csv to $result_directory" -ForegroundColor Green
                python cros_automation.py download -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "$AGT_INTERNAL_PATH/agt_internal_log_$($cur_file_index+$file_index_offset).csv" -o "$result_directory\agt_internal_log_$($cur_file_index+$file_index_offset).csv"
                
                Write-Host "INFO`t: remove $AGT_INTERNAL_PATH/agt_internal_log_$($cur_file_index+$file_index_offset).csv on the test system" -ForegroundColor Green
                python cros_automation.py rm -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "$AGT_INTERNAL_PATH/agt_internal_log_$($cur_file_index+$file_index_offset).csv"
                
                Write-Host "INFO`t: list items in $AGT_INTERNAL_PATH" -ForegroundColor Green
                python cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d $AGT_INTERNAL_PATH
            }
        }

        # ----------------------------------------------------------------------

        if ($dc_mode) {
            if ($debug_mode) {
                Write-Host "INFO`t: (DEBUG MODE) re-enable ac" -ForegroundColor Green
                python cros_automation.py enable-ac -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE

                Write-Host "INFO`t: (DEBUG MODE) wait 60 seconds for enabling ac to exit" -ForegroundColor Green
                sleep_with_progress_bar -seconds 60
            }
            else {
                Write-Host "INFO`t: re-enable ac" -ForegroundColor Green
                python cros_automation.py enable-ac -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE

                Write-Host "INFO`t: wait 60 seconds for enabling ac to exit" -ForegroundColor Green
                sleep_with_progress_bar -seconds 60
            }
        }

    }
    else {
        Write-Host "ERROR`t: $scenario is not supported. supported scenarios are as follows:" -ForegroundColor Red
        foreach ($key in $SCENARIO_CONST.Keys) {
            Write-Host "ERROR`t: $key" -ForegroundColor Red
        }
    }
}