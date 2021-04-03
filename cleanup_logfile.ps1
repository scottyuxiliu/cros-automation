$VerbosePreference = "Continue"
$DebugPreference = "Continue"

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
        Write-Host -NoNewline "remove $filepath ... "
        Remove-Item -Path $filepath
        Write-Host "done"
    }
    catch {
        # Write-Verbose "`nan error occurred"
        Write-Host $_
    }
}

$logfiles = @(
    ".\cros_data_logger.log",
    ".\cros_data_parser.log",
    ".\cros_file_handler.log",
    ".\cros_scenario_launcher.log",
    ".\cros_software_controller.log"
)

foreach ($logfile in $logfiles) {
    remove_file -filepath $logfile
}