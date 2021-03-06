#!/bin/bash

# --------------------------------------------------------------------------------

# you may run this bash script from terminal as following
# source flashrom.sh [DUT_IP] [COREBOOT_DIR] [COREBOOT_FILE]

# for example
# source flashrom.sh "192.168.123.456" "C:\Users\scottyuxiliu\Downloads" "image.bin"


# --------------------------------------------------------------------------------


DUT_IP=$1 # no whitespace is allowed between the variable name, the equals sign, and the value
DUT_USERNAME="root"
DUT_SSH_KEYFILE="id_rsa"

COREBOOT_DIR=$2
COREBOOT_FILE=$3

echo "create /usr/local/coreboot directory on target system $DUT_IP ..."
python cros_automation.py mkdir -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local/coreboot"

echo "upload $COREBOOT_DIR/$COREBOOT_FILE to target system $DUT_IP ..."
python cros_automation.py upload -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "$COREBOOT_DIR/$COREBOOT_FILE" -o "/usr/local/coreboot/$COREBOOT_FILE"

echo "flash /usr/local/coreboot/$COREBOOT_FILE ..."
python cros_automation.py flashrom -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "/usr/local/coreboot/$COREBOOT_FILE"

echo "reboot test system $DUT_IP ..."
python cros_automation.py reboot -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE