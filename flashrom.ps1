$VerbosePreference = "Continue"
$DebugPreference = "Continue"

#----------------------------------------------------------------------
# User inputs

$TEST_SYS_IP = "192.168.2.172"
$TEST_SYS_USERNAME = "root"
$TEST_SYS_KEYFILE = "id_rsa"

$COREBOOT_DIR = "C:\Users\$($env:UserName)\Downloads"
$COREBOOT_FILE = "image-dirinboz.bin"

#----------------------------------------------------------------------

$src = Join-Path -Path $COREBOOT_DIR -ChildPath $COREBOOT_FILE

Write-Verbose "create /usr/local/coreboot directory on target system $TEST_SYS_IP ..."
python .\cros_automation.py mkdir -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "/usr/local/coreboot"

Write-Verbose "upload $src to target system $TEST_SYS_IP ..."
python .\cros_automation.py upload -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i $src -o "/usr/local/coreboot/$COREBOOT_FILE"

Write-Verbose "flash /usr/local/coreboot/$COREBOOT_FILE ..."
python .\cros_automation.py flashrom -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "/usr/local/coreboot/$COREBOOT_FILE"

Write-Verbose "reboot test system $TEST_SYS_IP ..."
python.exe .\cros_automation.py reboot -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE