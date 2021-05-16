$VerbosePreference = "Continue"
$DebugPreference = "Continue"

#----------------------------------------------------------------------
# User inputs

$DUT_IP = ""
$DUT_USERNAME = "root"
$DUT_SSH_KEYFILE = "id_rsa"

$AUTOTEST_BACKUP = ""

#----------------------------------------------------------------------

Write-Verbose "compress /usr/local/autotest directory on $DUT_IP ..."
python .\cros_automation.py compress -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "/usr/local/autotest"

Write-Verbose "download /usr/local/autotest.tar.gz to $AUTOTEST_BACKUP_DIR ..."
python .\cros_automation.py download -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "/usr/local/autotest.tar.gz" -o $AUTOTEST_BACKUP

Write-Verbose "remove /usr/local/autotest.tar.gz on $DUT_IP ..."
python .\cros_automation.py rm -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "/usr/local/autotest.tar.gz"

Write-Verbose "ls /usr/local/autotest on $DUT_IP ..."
python .\cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local/autotest"

Write-Verbose "ls /usr/local/autotest/tests on $DUT_IP ..."
python .\cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local/autotest/tests"