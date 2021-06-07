# --------------------------------------------------------------------------------

# you may run this ps script from powershell as following
# .\autotest_restore.ps1 [DUT_IP] [AUTOTEST_PACKAGE]

# for example
# .\autotest_restore.ps1 192.168.123.456 C:\Users\scottyuxiliu\Downloads\autotest.tar.gz


# --------------------------------------------------------------------------------

$VerbosePreference = "Continue"
$DebugPreference = "Continue"

$DUT_IP = $args[0]
$DUT_USERNAME = "root"
$DUT_SSH_KEYFILE = "id_rsa"

$AUTOTEST_PACKAGE = $args[1]

Write-Host "INFO`t: remove /usr/local/autotest directory on $DUT_IP" -ForegroundColor Green
python .\cros_automation.py rmdir -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local/autotest"

Write-Host "INFO`t: upload $AUTOTEST_PACKAGE to $DUT_IP" -ForegroundColor Green
python .\cros_automation.py upload -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i $AUTOTEST_PACKAGE -o "/usr/local/autotest.tar.gz"

Write-Host "INFO`t: extract /usr/local/autotest.tar.gz on $DUT_IP" -ForegroundColor Green
python .\cros_automation.py extract -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "/usr/local/autotest.tar.gz"

Write-Host "INFO`t: remove /usr/local/autotest.tar.gz on $DUT_IP" -ForegroundColor Green
python .\cros_automation.py rm -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "/usr/local/autotest.tar.gz"

Write-Host "INFO`t: ls /usr/local/autotest on $DUT_IP" -ForegroundColor Green
python .\cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local/autotest"

Write-Host "INFO`t: ls /usr/local/autotest/tests on $DUT_IP" -ForegroundColor Green
python .\cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local/autotest/tests"