#----------------------------------------------------------------------
# User inputs

$delay_between_loop = 60 # delay $delay_between_loop seconds before starting the next iteration

# --------------

$test_system_ip_address = "10.4.44.5"
$test_system_username = "root"
$test_system_ssh_private_key_file = "id_rsa"

# --------------
# the downloads directory on host system. when collecting data on the host system, all results are output to this directory by default.
# for example, $downloads_directory = "C:\Users\powerhost\Downloads"
$downloads_directory = "C:\Users\scottyuxiliu\Downloads"

#----------------------------------------------------------------------

$VerbosePreference = "Continue"
$DebugPreference = "Continue"

$duration_aquarium = 120

$delay_after_boot = 180

$test_system_atitool_directory = "/usr/local/atitool"

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
        [Parameter(Mandatory=$true)] [string] $loops,
        [Parameter(Mandatory=$true)] [string] $scenario,
        [Parameter(Mandatory=$true)] [string] $result_directory
    )

    Write-Verbose "set up result directory ..."
    $result_directory = "$downloads_directory\$result_directory"
    if( -not ( check_directory_exist -directory $result_directory ) ) {
        create_directory -directory $result_directory
    }
    
    foreach ($i in 1..$loops) {
        Write-Verbose "get current result file index ..."
        $offset = get_current_result_file_index -result_directory $result_directory

        Write-Verbose "reboot test system for $scenario scenario, loop $i ..."
        python.exe .\cros_automation.py reboot -p $test_system_ip_address -u $test_system_username -k $test_system_ssh_private_key_file

        Write-Verbose "wait $delay_after_boot seconds before running $scenario ..."
        sleep_with_progress_bar -seconds $delay_after_boot

        if ($scenario -eq "aquarium") {
            Write-Verbose "start atitool logging to $test_system_atitool_directory/pm_log_$($i+$offset).csv and launch $scenario ..."
            python.exe .\cros_automation.py atitool -p $test_system_ip_address -u $test_system_username -k $test_system_ssh_private_key_file -t $duration_aquarium -o "pm_log_$($i+$offset).csv"
            python.exe .\cros_automation.py aquarium -p $test_system_ip_address -u $test_system_username -k $test_system_ssh_private_key_file

            Write-Verbose "wait $duration_aquarium seconds for $scenario to finish ..."
            sleep_with_progress_bar -seconds $duration_aquarium

            Write-Verbose "wait 60 seconds for data logging to finish ..."
            sleep_with_progress_bar -seconds 60

            Write-Verbose "download atitool log $test_system_atitool_directory/pm_log_$($i+$offset).csv to $result_directory ..."
            python .\cros_automation.py download -p $test_system_ip_address -u $test_system_username -k $test_system_ssh_private_key_file -i "$test_system_atitool_directory/pm_log_$($i+$offset).csv" -o "$result_directory\pm_log_$($i+$offset).csv"
            
            Write-Verbose "remove atitool log $test_system_atitool_directory/pm_log_$($i+$offset).csv on the test system ..."
            python .\cros_automation.py remove -p $test_system_ip_address -u $test_system_username -k $test_system_ssh_private_key_file -i "$test_system_atitool_directory/pm_log_$($i+$offset).csv"
            
            Write-Verbose "list items in $test_system_atitool_directory ..."
            python .\cros_automation.py ls -p $test_system_ip_address -u $test_system_username -k $test_system_ssh_private_key_file -d "$test_system_atitool_directory"

        }
        else {
            Write-Verbose "$scenario is not supported. supported scenarios are: aquarium"
        }

        if($i -ne $loops) {
            Write-Verbose "wait $delay_between_loop seconds to start loop $($i+1) ..." 
            sleep_with_progress_bar -seconds $delay_between_loop
        }
    }
}

measurement -loops 3 -scenario "aquarium" -result_directory "r87_13434.223_default_aquarium_vilboz"