$VerbosePreference = "Continue"
$DebugPreference = "Continue"

#----------------------------------------------------------------------
# User inputs

$TEST_SYS_IP = ""
$TEST_SYS_USERNAME = "root"
$TEST_SYS_KEYFILE = "id_rsa"

$AUTOTEST_PACKAGE = ""

#----------------------------------------------------------------------

Write-Verbose "remove /usr/local/autotest directory on $TEST_SYS_IP ..."
python .\cros_automation.py rmdir -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "/usr/local/autotest"

Write-Verbose "upload $AUTOTEST_PACKAGE to $TEST_SYS_IP ..."
python .\cros_automation.py upload -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i $AUTOTEST_PACKAGE -o "/usr/local/autotest.tar.gz"

Write-Verbose "extract /usr/local/autotest.tar.gz on $TEST_SYS_IP ..."
python .\cros_automation.py extract -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "/usr/local/autotest.tar.gz"

Write-Verbose "remove /usr/local/autotest.tar.gz on $TEST_SYS_IP ..."
python .\cros_automation.py rm -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "/usr/local/autotest.tar.gz"

Write-Verbose "ls /usr/local/autotest on $TEST_SYS_IP ..."
python .\cros_automation.py ls -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "/usr/local/autotest"

Write-Verbose "ls /usr/local/autotest/tests on $TEST_SYS_IP ..."
python .\cros_automation.py ls -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "/usr/local/autotest/tests"