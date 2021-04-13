$VerbosePreference = "Continue"
$DebugPreference = "Continue"

#----------------------------------------------------------------------
# User inputs

$TEST_SYS_IP = ""
$TEST_SYS_USERNAME = "root"
$TEST_SYS_KEYFILE = "id_rsa"

$AUTOTEST_BACKUP = ""

#----------------------------------------------------------------------

Write-Verbose "compress /usr/local/autotest directory on $TEST_SYS_IP ..."
python .\cros_automation.py compress -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "/usr/local/autotest"

Write-Verbose "download /usr/local/autotest.tar.gz to $AUTOTEST_BACKUP_DIR ..."
python .\cros_automation.py download -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "/usr/local/autotest.tar.gz" -o $AUTOTEST_BACKUP

Write-Verbose "remove /usr/local/autotest.tar.gz on $TEST_SYS_IP ..."
python .\cros_automation.py rm -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "/usr/local/autotest.tar.gz"

Write-Verbose "ls /usr/local/autotest on $TEST_SYS_IP ..."
python .\cros_automation.py ls -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "/usr/local/autotest"

Write-Verbose "ls /usr/local/autotest/tests on $TEST_SYS_IP ..."
python .\cros_automation.py ls -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "/usr/local/autotest/tests"