#!/bin/bash

# --------------------------------------------------------------------------------

# you may run this bash script from terminal as following
# source agt_internal_log.sh [DUT_IP] [DURATION] [DIR] [OUTPUT]

# for example
# source agt_internal_log.sh 192.168.123.456 60 /home/scottyuxiliu/Downloads/ agt_internal_log.csv


# --------------------------------------------------------------------------------

source cros_constants.sh
source cros_utils.sh

DUT_IP=$1 # no whitespace is allowed between the variable name, the equals sign, and the value
DUT_USERNAME="root"
DUT_SSH_KEYFILE="id_rsa"
DURATION=$2
DIR=$3
OUTPUT=$4

echo -e "${INFO}check ${DIR}${ENDFORMAT}"
if [ -d $DIR ] # need to have spaces after "[" and before "]"
then
    :
else
    echo -e "${ERROR}no such directory: ${DIR}${ENDFORMAT}"
    return # Cause a shell function to exit with the return value n. If n is not supplied, the return value is the exit status of the last command executed in the function.
fi

echo -e "${INFO}start agt internal logging to $AGT_INTERNAL_PATH/${OUTPUT}${ENDFORMAT}"
python cros_automation.py agt-internal-log -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -t $DURATION -o $OUTPUT

echo -e "${INFO}wait $DURATION seconds for agt internal logging to finish${ENDFORMAT}"
sleep_with_progress_bar $DURATION

echo -e "${INFO}wait 60 seconds for operation to exit${ENDFORMAT}"
sleep_with_progress_bar 60

echo -e "${INFO}download $AGT_INTERNAL_PATH/$OUTPUT to ${DIR}${ENDFORMAT}"
python cros_automation.py download -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "$AGT_INTERNAL_PATH/$OUTPUT" -o "$DIR/$OUTPUT"

echo -e "${INFO}remove $AGT_INTERNAL_PATH/$OUTPUT on ${DUT_IP}${ENDFORMAT}"
python cros_automation.py rm -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "$AGT_INTERNAL_PATH/$OUTPUT"

echo -e "${INFO}ls $AGT_INTERNAL_PATH on ${DUT_IP}${ENDFORMAT}"
python cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d $AGT_INTERNAL_PATH