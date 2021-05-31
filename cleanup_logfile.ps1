. .\cros_constants.ps1

$VerbosePreference = "Continue"
$DebugPreference = "Continue"

function check_file_exist {
    <#
    .SYNOPSIS
        This function checks if the file path $file exists.
        Return true if it does, return false if it doesn't.

    .INPUTS
        file
    #>
    [CmdletBinding()]
    param (
        [Parameter(Mandatory=$true)][string]$file
    )

    # Write-Host -NoNewline "check if file $file exists ... "

    if(Test-Path $file) {
        # Write-Host "file found"
        return $true     
    }
    else {
        # Write-Host "file not found"
        return $false
    }
}

function remove_file {
    <#
    .SYNOPSIS
        This function removes file located at $filepath.

    .INPUTS
        filepath
    #>
    [CmdletBinding()]
    param (
        [Parameter(Mandatory=$true)][string]$filepath
    )

    try {
        # Write-Host -NoNewline "remove $filepath ... "
        Remove-Item -Path $filepath
        # Write-Host "done"
    }
    catch {
        # Write-Verbose "`nan error occurred"
        Write-Host $_
    }
}

foreach ($logfile in $LOGS) {
    if (check_file_exist -file $logfile) {
        Write-Host "INFO`t: remove $logfile" -ForegroundColor Green
        remove_file -filepath $logfile
    }
    else {
        Write-Host "ERROR`t: no such file: $logfile" -ForegroundColor Red
    }
}