#!/bin/bash

# --------------------------------------------------------------------------------

# you may run this bash script from terminal as following
# source autotest_restore.sh [TEST_SYS_IP] [AUTOTEST_PACKAGE]

# for example
# source autotest_restore.sh "192.168.123.456" "/media/scottyuxiliu/crosdata/autotest.tar.gz"


# --------------------------------------------------------------------------------

TEST_SYS_IP=$1 # no whitespace is allowed between the variable name, the equals sign, and the value
TEST_SYS_USERNAME="root"
TEST_SYS_KEYFILE="id_rsa"
AUTOTEST_PACKAGE=$2

echo "remove /usr/local/autotest directory on $TEST_SYS_IP ..."
python cros_automation.py rmdir -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "/usr/local/autotest"

echo "upload $AUTOTEST_PACKAGE to $TEST_SYS_IP ..."
python cros_automation.py upload -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i $AUTOTEST_PACKAGE -o "/usr/local/autotest.tar.gz"

echo "extract /usr/local/autotest.tar.gz on $TEST_SYS_IP ..."
python cros_automation.py extract -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "/usr/local/autotest.tar.gz"

echo "remove /usr/local/autotest.tar.gz on $TEST_SYS_IP ..."
python cros_automation.py rm -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "/usr/local/autotest.tar.gz"

echo "ls /usr/local/autotest on $TEST_SYS_IP ..."
python cros_automation.py ls -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "/usr/local/autotest"

echo "ls /usr/local/autotest/tests on $TEST_SYS_IP ..."
python cros_automation.py ls -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "/usr/local/autotest/tests"