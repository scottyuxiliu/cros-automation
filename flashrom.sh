#!/bin/bash

# --------------------------------------------------------------------------------

# you may run this bash script from terminal as following
# source flashrom.sh [TEST_SYS_IP] [COREBOOT_DIR] [COREBOOT_FILE]

# for example
# source flashrom.sh "192.168.123.456" "C:\Users\scottyuxiliu\Downloads" "image.bin"


# --------------------------------------------------------------------------------


TEST_SYS_IP=$1 # no whitespace is allowed between the variable name, the equals sign, and the value
TEST_SYS_USERNAME="root"
TEST_SYS_KEYFILE="id_rsa"

COREBOOT_DIR=$2
COREBOOT_FILE=$3

echo "create /usr/local/coreboot directory on target system $TEST_SYS_IP ..."
python cros_automation.py mkdir -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "/usr/local/coreboot"

echo "upload $COREBOOT_DIR/$COREBOOT_FILE to target system $TEST_SYS_IP ..."
python cros_automation.py upload -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "$COREBOOT_DIR/$COREBOOT_FILE" -o "/usr/local/coreboot/$COREBOOT_FILE"

echo "flash /usr/local/coreboot/$COREBOOT_FILE ..."
python cros_automation.py flashrom -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "/usr/local/coreboot/$COREBOOT_FILE"

echo "reboot test system $TEST_SYS_IP ..."
python cros_automation.py reboot -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE