#----------------------------------------------------------------------
# User inputs

$DELAY_BETWEEN_LOOP = 60 # delay $DELAY_BETWEEN_LOOP seconds before starting the next iteration

# --------------

$TEST_SYS_IP = "10.4.39.203"
$TEST_SYS_USERNAME = "root"
$TEST_SYS_KEYFILE = "id_rsa"

# --------------
# the downloads directory on host system. when collecting data on the host system, all results are output to this directory by default.
# for example, $DOWNLOADS_PATH = "C:\Users\$($env:UserName)\Downloads"
$DOWNLOADS_PATH = "C:\Users\$($env:UserName)\Downloads"

#----------------------------------------------------------------------

#----------------------------------------------------------------------
# Constants

$VerbosePreference = "Continue"
$DebugPreference = "Continue"

$SCENARIO_CONST = @{
    "aquarium" = @{
        "delay" = 120;
        "id" = "graphics_WebGLAquarium"
    }
    "plt" = @{
        "delay" = 3600;
        "id" = "power_LoadTest.1hour"
    }
}

$DELAY_AFTER_BOOT = 180

$TEST_SYS_AUTOTEST_PATH = "/usr/local/autotest"
$TEST_SYS_ATITOOL_PATH = "/usr/local/atitool"

#----------------------------------------------------------------------

function check_directory_exist {
    <#
    .SYNOPSIS
        this function checks if $directory exists.
        reeturn true if it does, return false if it doesn't.

    .INPUTS
        directory
    #>
    [CmdletBinding()]
    param (
        [Parameter(Mandatory=$true)][string]$directory
    )
    
    Write-Host -NoNewline "check if directory $directory exists ... "

    if(Test-Path $directory) {
        Write-Host "directory found"
        return $true     
    }
    else {
        Write-Host "directory not found"
        return $false
    }
}

function create_directory {
    <#
    .SYNOPSIS
        this function creates a directory given path specified
        by $directory.

    .INPUTS
        directory
    #>
    [CmdletBinding()]
    param (
        [Parameter(Mandatory=$true)][string]$directory
    )
    
    Write-Host -NoNewline "create directory $directory ... "

    try {
        New-Item `
        -ItemType directory `
        -Path $directory | Out-Null

        Write-Host "done"
        
    }
    catch {
        Write-Host "`nan error occurred"
        Write-Host $_
    }

}

function get_current_result_file_index {
    <#
    .SYNOPSIS
        this function checks result files that already
        exist in the result directory, and returns the
        next index/run number that a new result file
        should be named after.

    .EXAMPLE
        example
    #>
    param (
        [Parameter(Mandatory=$true, Position=0)] [string] $result_directory
    )
    
    $offset = 0
    $existing_power_logs = Get-ChildItem -Path $result_directory

    foreach ($existing_power_log in $existing_power_logs) {
        $filename = Split-Path -Path $existing_power_log.FullName -Leaf

        $filename = $filename -replace ".csv",""
        $filename = $filename -replace ".xlsx",""
        $filename = $filename -replace ".etl",""
        $filename = $filename -replace ".html",""

        $instance = ($filename -split '_')[-1]
        $instance = [convert]::ToInt32($instance, 10)

        # Write-Host "filename: $filename, instance: $instance, offset: $offset" -ForegroundColor Yellow

        if ($offset -lt $instance) {
            $offset = $instance
        }
    }

    return $offset
}

function sleep_with_progress_bar($seconds) {
    <#
    .SYNOPSIS
        this function waits for $seconds with
        a progress bar showing the time remaining.

    .INPUTS
        seconds
    #>

    $doneDT = (Get-Date).AddSeconds($seconds)
    while($doneDT -gt (Get-Date)) {
        $secondsLeft = $doneDT.Subtract((Get-Date)).TotalSeconds
        $percent = ($seconds - $secondsLeft) / $seconds * 100
        Write-Progress -Activity "Sleeping" -Status "Sleeping..." -SecondsRemaining $secondsLeft -PercentComplete $percent
        [System.Threading.Thread]::Sleep(500)
    }
    Write-Progress -Activity "Sleeping" -Status "Sleeping..." -SecondsRemaining 0 -Completed
}

function measurement {
    param (
        [Parameter(Mandatory=$true)] [string] $scenario,
        [Parameter(Mandatory=$true)] [string] $result_directory
    )

    if ($SCENARIO_CONST.ContainsKey($scenario)) {
        Write-Verbose "start atitool logging to $TEST_SYS_ATITOOL_PATH/pm_log_$($i+$offset).csv ..."
        python.exe .\cros_automation.py atitool-log -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -t $SCENARIO_CONST.Item($scenario).Item("delay") -o "pm_log_$($i+$offset).csv"

        Write-Verbose "launch $scenario ..."
        python.exe .\cros_automation.py aquarium -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE

        Write-Verbose "wait $($SCENARIO_CONST.Item($scenario).Item('delay')) seconds for $scenario to finish ..."
        sleep_with_progress_bar -seconds $SCENARIO_CONST.Item($scenario).Item("delay")

        Write-Verbose "wait 60 seconds for data logging to finish ..."
        sleep_with_progress_bar -seconds 60

        Write-Verbose "download $scenario result keyval $TEST_SYS_AUTOTEST_PATH/results/default/$($SCENARIO_CONST.Item($scenario).Item('id'))/results/keyval to $result_directory ..."
        python .\cros_automation.py download -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "$TEST_SYS_AUTOTEST_PATH/results/default/$($SCENARIO_CONST.Item($scenario).Item('id'))/results/keyval" -o "$result_directory\keyval_$($i+$offset)"

        Write-Verbose "list items in $TEST_SYS_AUTOTEST_PATH/results/default/$($SCENARIO_CONST.Item($scenario).Item('id'))/results ..."
        python .\cros_automation.py ls -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "$TEST_SYS_AUTOTEST_PATH/results/default/$($SCENARIO_CONST.Item($scenario).Item('id'))/results"

        Write-Verbose "download atitool log $TEST_SYS_ATITOOL_PATH/pm_log_$($i+$offset).csv to $result_directory ..."
        python .\cros_automation.py download -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "$TEST_SYS_ATITOOL_PATH/pm_log_$($i+$offset).csv" -o "$result_directory\pm_log_$($i+$offset).csv"
        
        Write-Verbose "remove atitool log $TEST_SYS_ATITOOL_PATH/pm_log_$($i+$offset).csv on the test system ..."
        python .\cros_automation.py remove -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "$TEST_SYS_ATITOOL_PATH/pm_log_$($i+$offset).csv"
        
        Write-Verbose "list items in $TEST_SYS_ATITOOL_PATH ..."
        python .\cros_automation.py ls -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "$TEST_SYS_ATITOOL_PATH"
    }
    else {
        Write-Verbose "$scenario is not supported. supported scenarios are as follows:"
        foreach ($key in $SCENARIO_CONST.Keys) {
            Write-Verbose "$key"
        }
    }
}

function example {
    param (
        [Parameter(Mandatory=$true)] [string] $loops,
        [Parameter(Mandatory=$true)] [string] $scenario,
        [Parameter(Mandatory=$true)] [string] $result_directory
    )

    Write-Verbose "set up result directory ..."
    $result_directory = "$DOWNLOADS_PATH\$result_directory"
    if( -not ( check_directory_exist -directory $result_directory ) ) {
        create_directory -directory $result_directory
    }
    
    Write-Verbose "get current result file index ..."
    $offset = get_current_result_file_index -result_directory $result_directory

    foreach ($i in 1..$loops) {
        Write-Verbose "reboot test system for $scenario scenario, loop $i ..."
        python.exe .\cros_automation.py reboot -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE

        Write-Verbose "wait $DELAY_AFTER_BOOT seconds before running $scenario ..."
        sleep_with_progress_bar -seconds $DELAY_AFTER_BOOT

        measurement -scenario $scenario -result_directory $result_directory

        if($i -ne $loops) {
            Write-Verbose "wait $DELAY_BETWEEN_LOOP seconds to start loop $($i+1) ..." 
            sleep_with_progress_bar -seconds $DELAY_BETWEEN_LOOP
        }
    }
}

example -loops 1 -scenario "aquarium" -result_directory "r87_13434.223_default_aquarium_vilboz"