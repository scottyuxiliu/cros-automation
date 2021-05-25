#!/bin/bash

# --------------------------------------------------------------------------------

# you may run this bash script from terminal as following
# source autotest_backup.sh [DUT_IP] [AUTOTEST_PACKAGE]

# for example
# source autotest_backup.sh 192.168.123.456 /media/scottyuxiliu/crosdata/autotest.tar.gz


# --------------------------------------------------------------------------------

source cros_constants.sh

DUT_IP=$1 # no whitespace is allowed between the variable name, the equals sign, and the value
DUT_USERNAME="root"
DUT_SSH_KEYFILE="id_rsa"
AUTOTEST_PACKAGE=$2

echo -e "${INFO}compress /usr/local/autotest on ${DUT_IP}${ENDFORMAT}"
python cros_automation.py compress -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "/usr/local/autotest"

echo -e "${INFO}download /usr/local/autotest.tar.gz to ${AUTOTEST_PACKAGE}${ENDFORMAT}"
python cros_automation.py download -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "/usr/local/autotest.tar.gz" -o $AUTOTEST_PACKAGE

echo -e "${INFO}remove /usr/local/autotest.tar.gz on ${DUT_IP}${ENDFORMAT}"
python cros_automation.py rm -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "/usr/local/autotest.tar.gz"

echo -e "${INFO}ls /usr/local/autotest on ${DUT_IP}${ENDFORMAT}"
python cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local/autotest"

echo -e "${INFO}ls /usr/local/autotest/tests on ${DUT_IP}${ENDFORMAT}"
python cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local/autotest/tests"