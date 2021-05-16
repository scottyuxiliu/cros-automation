# --------------------------------------------------------------------------------

# you may run this ps script from powershell as following
# .\flashrom.ps1 [DUT_IP] [COREBOOT_DIR] [COREBOOT_FILE]

# for example
# .\flashrom.ps1 "192.168.123.456" "C:\Users\scottyuxiliu\Downloads" "image.bin"


# --------------------------------------------------------------------------------


$VerbosePreference = "Continue"
$DebugPreference = "Continue"

$DUT_IP = $args[0]
$DUT_USERNAME = "root"
$DUT_SSH_KEYFILE = "id_rsa"

$COREBOOT_DIR = $args[1]
$COREBOOT_FILE = $args[2]

$src = Join-Path -Path $COREBOOT_DIR -ChildPath $COREBOOT_FILE

Write-Verbose "create /usr/local/coreboot directory on target system $DUT_IP ..."
python .\cros_automation.py mkdir -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local/coreboot"

Write-Verbose "upload $src to target system $DUT_IP ..."
python .\cros_automation.py upload -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i $src -o "/usr/local/coreboot/$COREBOOT_FILE"

Write-Verbose "flash /usr/local/coreboot/$COREBOOT_FILE ..."
python .\cros_automation.py flashrom -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "/usr/local/coreboot/$COREBOOT_FILE"

Write-Verbose "reboot test system $DUT_IP ..."
python.exe .\cros_automation.py reboot -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE