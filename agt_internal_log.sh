#!/bin/bash

# --------------------------------------------------------------------------------

# you may run this bash script from terminal as following
# source agt_internal_log.sh [TEST_SYS_IP] [DURATION] [DIR] [OUTPUT]

# for example
# source agt_internal_log.sh "192.168.123.456" "60" "/home/scottyuxiliu/Downloads/" "agt_internal_log.csv"


# --------------------------------------------------------------------------------

TEST_SYS_IP=$1 # no whitespace is allowed between the variable name, the equals sign, and the value
TEST_SYS_USERNAME="root"
TEST_SYS_KEYFILE="id_rsa"
DURATION=$2
DIR=$3
OUTPUT=$4

echo "start agt internal logging to /usr/local/agt_internal/$OUTPUT ..."
python cros_automation.py agt-internal-log -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -t $DURATION -o $OUTPUT

echo "wait $DURATION seconds for agt internal logging to finish ..."
sleep $DURATION

echo "wait 1 minute for agt internal logging to exit ..."
sleep 1m

echo "download /usr/local/agt_internal/$OUTPUT to $DIR ..."
python cros_automation.py download -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "/usr/local/agt_internal/$OUTPUT" -o "$DIR/$OUTPUT"

echo "remove /usr/local/agt_internal/$OUTPUT on $TEST_SYS_IP ..."
python cros_automation.py rm -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "/usr/local/agt_internal/$OUTPUT"

echo "ls /usr/local/agt_internal on $TEST_SYS_IP ..."
python cros_automation.py ls -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "/usr/local/agt_internal"