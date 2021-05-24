#!/bin/bash

# --------------------------------------------------------------------------------

# you may run this bash script from terminal as following
# source agt_install.sh [DUT_IP] [AGT_PACKAGE]

# for example
# source agt_install.sh 192.168.123.456 /media/scottyuxiliu/crosdata/agt.tar.gz


# --------------------------------------------------------------------------------

source cros_constants.sh

DUT_IP=$1 # no whitespace is allowed between the variable name, the equals sign, and the value
DUT_USERNAME="root"
DUT_SSH_KEYFILE="id_rsa"
AGT_PACKAGE=$2

echo -e "${INFO}remove $AGT_PATH directory on $DUT_IP if it exists${ENDFORMAT}"
python cros_automation.py rmdir -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d $AGT_PATH

echo -e "${INFO}create $AGT_PATH directory on ${DUT_IP}${ENDFORMAT}"
python cros_automation.py mkdir -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d $AGT_PATH

echo -e "${INFO}upload $AGT_PACKAGE to ${DUT_IP}${ENDFORMAT}"
python cros_automation.py upload -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i $AGT_PACKAGE -o "$AGT_PATH/agt.tar.gz"

echo -e "${INFO}extract $AGT_PATH/agt.tar.gz on ${DUT_IP}${ENDFORMAT}"
python cros_automation.py extract -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "$AGT_PATH/agt.tar.gz"

echo -e "${INFO}remove $AGT_PATH/agt.tar.gz on ${DUT_IP}${ENDFORMAT}"
python cros_automation.py rm -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "$AGT_PATH/agt.tar.gz"

echo -e "${INFO}ls $AGT_PATH on ${DUT_IP}${ENDFORMAT}"
python cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d $AGT_PATH
