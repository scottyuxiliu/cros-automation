#!/bin/bash

# --------------------------------------------------------------------------------

# you may run this bash script from terminal as following
# source agt_uninstall.sh [TEST_SYS_IP]

# for example
# source agt_uninstall.sh "192.168.123.456"


# --------------------------------------------------------------------------------

TEST_SYS_IP=$1 # no whitespace is allowed between the variable name, the equals sign, and the value
TEST_SYS_USERNAME="root"
TEST_SYS_KEYFILE="id_rsa"

echo "remove /usr/local/agt directory on $TEST_SYS_IP ..."
python cros_automation.py rmdir -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "/usr/local/agt"

echo "ls /usr/local on $TEST_SYS_IP ..."
python cros_automation.py ls -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "/usr/local"
