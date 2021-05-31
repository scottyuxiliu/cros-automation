# --------------------------------------------------------------------------------

# you may run this ps script from powershell as following
# .\agt_internal_log.ps1 [DUT_IP] [DURATION] [DIR] [OUTPUT]

# for example
# .\agt_internal_log.ps1 192.168.123.456 60 C:\Users\scottyuxiliu\Downloads agt_internal_log.csv


# --------------------------------------------------------------------------------

. .\cros_constants.ps1

$DUT_IP = $args[0]
$DUT_USERNAME = "root"
$DUT_SSH_KEYFILE = "id_rsa"

$DURATION = $args[1]
$DIR = $args[2]
$OUTPUT = $args[3]

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
    
    Write-Host "INFO`t: check $directory" -ForegroundColor Green

    if(Test-Path $directory) {
        return $true
    }
    else {
        Write-Host "WARNING`t: no such directory: $directory" -ForegroundColor Yellow
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
    
    Write-Host "WARNING`t: create directory: $directory" -ForegroundColor Yellow

    try {
        New-Item `
        -ItemType directory `
        -Path $directory | Out-Null

    }
    catch {
        Write-Host "ERROR`t: couldn't create directory" -ForegroundColor Red
        Write-Host $_
    }

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


if( -not ( check_directory_exist -directory $DIR ) ) {
    create_directory -directory $DIR
}

Write-Host "INFO`t: start agt internal logging to $AGT_INTERNAL_PATH/$OUTPUT" -ForegroundColor Green
python cros_automation.py agt-internal-log -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -t $DURATION -o $OUTPUT

Write-Host "INFO`t: wait $DURATION seconds for agt internal logging to finish" -ForegroundColor Green
sleep_with_progress_bar -seconds $DURATION

Write-Host "INFO`t: wait 60 seconds for operation to exit" -ForegroundColor Green
sleep_with_progress_bar -seconds 60

Write-Host "INFO`t: download $AGT_INTERNAL_PATH/$OUTPUT to $DIR" -ForegroundColor Green
python cros_automation.py download -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "$AGT_INTERNAL_PATH/$OUTPUT" -o "$DIR\$OUTPUT"

Write-Host "INFO`t: remove $AGT_INTERNAL_PATH/$OUTPUT on $DUT_IP" -ForegroundColor Green
python cros_automation.py rm -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "$AGT_INTERNAL_PATH/$OUTPUT"

Write-Host "INFO`t: ls $AGT_INTERNAL_PATH" -ForegroundColor Green
python cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d $AGT_INTERNAL_PATH