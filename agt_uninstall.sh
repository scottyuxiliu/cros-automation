#!/bin/bash

# --------------------------------------------------------------------------------

# you may run this bash script from terminal as following
# source agt_uninstall.sh [DUT_IP]

# for example
# source agt_uninstall.sh "192.168.123.456"


# --------------------------------------------------------------------------------

DUT_IP=$1 # no whitespace is allowed between the variable name, the equals sign, and the value
DUT_USERNAME="root"
DUT_SSH_KEYFILE="id_rsa"

echo "remove /usr/local/agt directory on $DUT_IP ..."
python cros_automation.py rmdir -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "/usr/local/agt"

echo "ls /usr/local on $DUT_IP ..."
python cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local"
