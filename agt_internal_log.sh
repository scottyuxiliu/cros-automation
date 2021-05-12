#!/bin/bash

# --------------------------------------------------------------------------------

# you may run this bash script from terminal as following
# source agt_internal_log.sh [TEST_SYS_IP] [DURATION] [DIR] [OUTPUT]

# for example
# source agt_internal_log.sh "192.168.123.456" "60" "/home/scottyuxiliu/Downloads/" "agt_internal_log.csv"


# --------------------------------------------------------------------------------

source cros_constants.sh

TEST_SYS_IP=$1 # no whitespace is allowed between the variable name, the equals sign, and the value
TEST_SYS_USERNAME="root"
TEST_SYS_KEYFILE="id_rsa"
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
python cros_automation.py agt-internal-log -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -t $DURATION -o $OUTPUT

echo -e "${INFO}wait $DURATION seconds for agt internal logging to finish${ENDFORMAT}"
sleep $DURATION

echo -e "${INFO}wait 1 minute for agt internal logging to exit${ENDFORMAT}"
sleep 1m

echo -e "${INFO}download $AGT_INTERNAL_PATH/$OUTPUT to ${DIR}${ENDFORMAT}"
python cros_automation.py download -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "$AGT_INTERNAL_PATH/$OUTPUT" -o "$DIR/$OUTPUT"

echo -e "${INFO}remove $AGT_INTERNAL_PATH/$OUTPUT on ${TEST_SYS_IP}${ENDFORMAT}"
python cros_automation.py rm -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "$AGT_INTERNAL_PATH/$OUTPUT"

echo -e "${INFO}ls $AGT_INTERNAL_PATH on ${TEST_SYS_IP}${ENDFORMAT}"
python cros_automation.py ls -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d $AGT_INTERNAL_PATH