#!/bin/bash

# --------------------------------------------------------------------------------

# you may run this bash script from terminal as following
# source agt_internal_install.sh [DUT_IP] [AGT_INTERNAL_PACKAGE]

# for example
# source agt_internal_install.sh 192.168.123.456 /media/scottyuxiliu/crosdata/agt_internal.tar.gz


# --------------------------------------------------------------------------------

source cros_constants.sh

DUT_IP=$1 # no whitespace is allowed between the variable name, the equals sign, and the value
DUT_USERNAME="root"
DUT_SSH_KEYFILE="id_rsa"
AGT_INTERNAL_PACKAGE=$2

echo -e "${INFO}remove /usr/local/agt_internal directory on $DUT_IP if it exists${ENDFORMAT}"
python cros_automation.py rmdir -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local/agt_internal"

echo -e "${INFO}create /usr/local/agt_internal directory on $DUT_IP${ENDFORMAT}"
python cros_automation.py mkdir -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local/agt_internal"

echo -e "${INFO}upload $AGT_INTERNAL_PACKAGE to $DUT_IP${ENDFORMAT}"
python cros_automation.py upload -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i $AGT_INTERNAL_PACKAGE -o "/usr/local/agt_internal/agt_internal.tar.gz"

echo -e "${INFO}extract /usr/local/agt_internal/agt_internal.tar.gz on $DUT_IP${ENDFORMAT}"
python cros_automation.py extract -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "/usr/local/agt_internal/agt_internal.tar.gz"

echo -e "${INFO}remove /usr/local/agt_internal/agt_internal.tar.gz on $DUT_IP${ENDFORMAT}"
python cros_automation.py rm -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "/usr/local/agt_internal/agt_internal.tar.gz"

echo -e "${INFO}ls /usr/local/agt_internal on $DUT_IP${ENDFORMAT}"
python cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local/agt_internal"
