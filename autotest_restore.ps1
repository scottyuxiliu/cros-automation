$VerbosePreference = "Continue"
$DebugPreference = "Continue"

#----------------------------------------------------------------------
# User inputs

$TEST_SYS_IP = "192.168.2.172"
$TEST_SYS_USERNAME = "root"
$TEST_SYS_KEYFILE = "id_rsa"

$AUTOTEST_PACKAGE = "C:\Users\scottyuxiliu\Downloads\autotest.tar.gz"

#----------------------------------------------------------------------

Write-Verbose "create /usr/local/autotest directory on target system $TEST_SYS_IP ..."
python .\cros_automation.py mkdir -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "/usr/local/autotest"

Write-Verbose "upload $AUTOTEST_PACKAGE to target system $TEST_SYS_IP ..."
python .\cros_automation.py upload -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i $AUTOTEST_PACKAGE -o "/usr/local/autotest/autotest.tar.gz"

Write-Verbose "extract /usr/local/autotest/autotest.tar.gz ..."
python .\cros_automation.py extract -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "/usr/local/autotest/autotest.tar.gz" --debug