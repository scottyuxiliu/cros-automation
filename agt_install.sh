#!/bin/bash

# --------------------------------------------------------------------------------

# you may run this bash script from terminal as following
# source agt_install.sh [TEST_SYS_IP] [AGT_PACKAGE]

# for example
# source agt_install.sh "192.168.123.456" "/media/scottyuxiliu/crosdata/agt.tar.gz"


# --------------------------------------------------------------------------------

TEST_SYS_IP=$1 # no whitespace is allowed between the variable name, the equals sign, and the value
TEST_SYS_USERNAME="root"
TEST_SYS_KEYFILE="id_rsa"
AGT_PACKAGE=$2

echo "remove /usr/local/agt directory on $TEST_SYS_IP if it exists ..."
python cros_automation.py rmdir -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "/usr/local/agt"

echo "create /usr/local/agt directory on $TEST_SYS_IP ..."
python cros_automation.py mkdir -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "/usr/local/agt"

echo "upload $AGT_PACKAGE to $TEST_SYS_IP ..."
python cros_automation.py upload -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i $AGT_PACKAGE -o "/usr/local/agt/agt.tar.gz"

echo "extract /usr/local/agt/agt.tar.gz on $TEST_SYS_IP ..."
python cros_automation.py extract -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "/usr/local/agt/agt.tar.gz"

echo "remove /usr/local/agt/agt.tar.gz on $TEST_SYS_IP ..."
python cros_automation.py rm -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "/usr/local/agt/agt.tar.gz"

echo "ls /usr/local/agt on $TEST_SYS_IP ..."
python cros_automation.py ls -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "/usr/local/agt"
