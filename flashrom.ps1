# --------------------------------------------------------------------------------

# you may run this ps script from powershell as following
# .\flashrom.ps1 [TEST_SYS_IP] [COREBOOT_DIR] [COREBOOT_FILE]

# for example
# .\flashrom.ps1 "192.168.123.456" "C:\Users\scottyuxiliu\Downloads" "image.bin"


# --------------------------------------------------------------------------------


$VerbosePreference = "Continue"
$DebugPreference = "Continue"

$TEST_SYS_IP = $args[0]
$TEST_SYS_USERNAME = "root"
$TEST_SYS_KEYFILE = "id_rsa"

$COREBOOT_DIR = $args[1]
$COREBOOT_FILE = $args[2]

$src = Join-Path -Path $COREBOOT_DIR -ChildPath $COREBOOT_FILE

Write-Verbose "create /usr/local/coreboot directory on target system $TEST_SYS_IP ..."
python .\cros_automation.py mkdir -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "/usr/local/coreboot"

Write-Verbose "upload $src to target system $TEST_SYS_IP ..."
python .\cros_automation.py upload -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i $src -o "/usr/local/coreboot/$COREBOOT_FILE"

Write-Verbose "flash /usr/local/coreboot/$COREBOOT_FILE ..."
python .\cros_automation.py flashrom -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "/usr/local/coreboot/$COREBOOT_FILE"

Write-Verbose "reboot test system $TEST_SYS_IP ..."
python.exe .\cros_automation.py reboot -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE