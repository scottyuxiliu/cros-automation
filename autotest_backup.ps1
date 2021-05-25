# --------------------------------------------------------------------------------

# you may run this ps script from powershell as following
# .\autotest_backup.ps1 [DUT_IP] [AUTOTEST_BACKUP]

# for example
# .\autotest_backup.ps1 "192.168.123.456" "C:\Users\scottyuxiliu\Downloads\autotest_backup.tar.gz"


# --------------------------------------------------------------------------------

$VerbosePreference = "Continue"
$DebugPreference = "Continue"

$DUT_IP = $args[0]
$DUT_USERNAME = "root"
$DUT_SSH_KEYFILE = "id_rsa"

$AUTOTEST_BACKUP = $args[1]

Write-Host "INFO`t: compress /usr/local/autotest directory on $DUT_IP" -ForegroundColor Green
python .\cros_automation.py compress -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "/usr/local/autotest"

Write-Host "INFO`t: download /usr/local/autotest.tar.gz to $AUTOTEST_BACKUP_DIR" -ForegroundColor Green
python .\cros_automation.py download -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "/usr/local/autotest.tar.gz" -o $AUTOTEST_BACKUP

Write-Host "INFO`t: remove /usr/local/autotest.tar.gz on $DUT_IP" -ForegroundColor Green
python .\cros_automation.py rm -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "/usr/local/autotest.tar.gz"

Write-Host "INFO`t: ls /usr/local/autotest on $DUT_IP" -ForegroundColor Green
python .\cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local/autotest"

Write-Host "INFO`t: ls /usr/local/autotest/tests on $DUT_IP" -ForegroundColor Green
python .\cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local/autotest/tests"