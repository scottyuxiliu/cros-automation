$VerbosePreference = "Continue"
$DebugPreference = "Continue"

#----------------------------------------------------------------------
# User inputs

$DUT_IP = ""
$DUT_USERNAME = "root"
$DUT_SSH_KEYFILE = "id_rsa"

$AUTOTEST_PACKAGE = ""

#----------------------------------------------------------------------

Write-Verbose "remove /usr/local/autotest directory on $DUT_IP ..."
python .\cros_automation.py rmdir -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local/autotest"

Write-Verbose "upload $AUTOTEST_PACKAGE to $DUT_IP ..."
python .\cros_automation.py upload -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i $AUTOTEST_PACKAGE -o "/usr/local/autotest.tar.gz"

Write-Verbose "extract /usr/local/autotest.tar.gz on $DUT_IP ..."
python .\cros_automation.py extract -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "/usr/local/autotest.tar.gz"

Write-Verbose "remove /usr/local/autotest.tar.gz on $DUT_IP ..."
python .\cros_automation.py rm -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "/usr/local/autotest.tar.gz"

Write-Verbose "ls /usr/local/autotest on $DUT_IP ..."
python .\cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local/autotest"

Write-Verbose "ls /usr/local/autotest/tests on $DUT_IP ..."
python .\cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local/autotest/tests"