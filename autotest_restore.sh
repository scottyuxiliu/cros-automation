#!/bin/bash

# --------------------------------------------------------------------------------

# you may run this bash script from terminal as following
# source autotest_restore.sh [DUT_IP] [AUTOTEST_PACKAGE]

# for example
# source autotest_restore.sh "192.168.123.456" "/media/scottyuxiliu/crosdata/autotest.tar.gz"


# --------------------------------------------------------------------------------

DUT_IP=$1 # no whitespace is allowed between the variable name, the equals sign, and the value
DUT_USERNAME="root"
DUT_SSH_KEYFILE="id_rsa"
AUTOTEST_PACKAGE=$2

echo "remove /usr/local/autotest directory on $DUT_IP ..."
python cros_automation.py rmdir -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local/autotest"

echo "upload $AUTOTEST_PACKAGE to $DUT_IP ..."
python cros_automation.py upload -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i $AUTOTEST_PACKAGE -o "/usr/local/autotest.tar.gz"

echo "extract /usr/local/autotest.tar.gz on $DUT_IP ..."
python cros_automation.py extract -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "/usr/local/autotest.tar.gz"

echo "remove /usr/local/autotest.tar.gz on $DUT_IP ..."
python cros_automation.py rm -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "/usr/local/autotest.tar.gz"

echo "ls /usr/local/autotest on $DUT_IP ..."
python cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local/autotest"

echo "ls /usr/local/autotest/tests on $DUT_IP ..."
python cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local/autotest/tests"