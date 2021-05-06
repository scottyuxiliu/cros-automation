#!/bin/bash

# --------------------------------------------------------------------------------

# you may run this bash script from terminal as following
# source agt_internal_install.sh [TEST_SYS_IP] [AGT_INTERNAL_PACKAGE]

# for example
# source agt_internal_install.sh "192.168.123.456" "/media/scottyuxiliu/crosdata/agt_internal.tar.gz"


# --------------------------------------------------------------------------------

TEST_SYS_IP=$1 # no whitespace is allowed between the variable name, the equals sign, and the value
TEST_SYS_USERNAME="root"
TEST_SYS_KEYFILE="id_rsa"
AGT_INTERNAL_PACKAGE=$2

echo "remove /usr/local/agt_internal directory on $TEST_SYS_IP if it exists ..."
python cros_automation.py rmdir -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "/usr/local/agt_internal"

echo "create /usr/local/agt_internal directory on $TEST_SYS_IP ..."
python cros_automation.py mkdir -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "/usr/local/agt_internal"

echo "upload $AGT_INTERNAL_PACKAGE to $TEST_SYS_IP ..."
python cros_automation.py upload -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i $AGT_INTERNAL_PACKAGE -o "/usr/local/agt_internal/agt_internal.tar.gz"

echo "extract /usr/local/agt_internal/agt_internal.tar.gz on $TEST_SYS_IP ..."
python cros_automation.py extract -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "/usr/local/agt_internal/agt_internal.tar.gz"

echo "remove /usr/local/agt_internal/agt_internal.tar.gz on $TEST_SYS_IP ..."
python cros_automation.py rm -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "/usr/local/agt_internal/agt_internal.tar.gz"

echo "ls /usr/local/agt_internal on $TEST_SYS_IP ..."
python cros_automation.py ls -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "/usr/local/agt_internal"
