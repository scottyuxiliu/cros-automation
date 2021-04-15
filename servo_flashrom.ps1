$VerbosePreference = "Continue"
$DebugPreference = "Continue"

#----------------------------------------------------------------------
# User inputs

$HOST_SYS_IP = ""
$HOST_SYS_USERNAME = ""
$HOST_SYS_KEYFILE = "id_rsa"
$HOST_SYS_SUDO_PASSWORD = ""

$COREBOOT_DIR = ""
$COREBOOT_FILE = ""

#----------------------------------------------------------------------

$src = Join-Path -Path $COREBOOT_DIR -ChildPath $COREBOOT_FILE

Write-Verbose "create /home/ppo/chromiumos/chroot/tmp/Stack directory on $HOST_SYS_IP ..."
python .\cros_automation.py mkdir -p $HOST_SYS_IP -u $HOST_SYS_USERNAME -k $HOST_SYS_KEYFILE -d "/home/ppo/chromiumos/chroot/tmp/Stack"

Write-Verbose "upload $src to $HOST_SYS_IP ..."
python .\cros_automation.py upload -p $HOST_SYS_IP -u $HOST_SYS_USERNAME -k $HOST_SYS_KEYFILE -i $src -o "/home/ppo/chromiumos/chroot/tmp/Stack/$COREBOOT_FILE"

Write-Verbose "use servo on $HOST_SYS_IP to flash /home/ppo/chromiumos/chroot/tmp/Stack/$COREBOOT_FILE ..."
python .\cros_automation.py servo-flashrom -p $HOST_SYS_IP -u $HOST_SYS_USERNAME -k $HOST_SYS_KEYFILE -i "/home/ppo/chromiumos/chroot/tmp/Stack/$COREBOOT_FILE" --sudo $HOST_SYS_SUDO_PASSWORD

Write-Verbose "remove /home/ppo/chromiumos/chroot/tmp/Stack/$COREBOOT_FILE on $HOST_SYS_IP ..."
python .\cros_automation.py rm -p $HOST_SYS_IP -u $HOST_SYS_USERNAME -k $HOST_SYS_KEYFILE -i "/home/ppo/chromiumos/chroot/tmp/Stack/$COREBOOT_FILE"