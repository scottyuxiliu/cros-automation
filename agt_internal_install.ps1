# --------------------------------------------------------------------------------

# you may run this ps script from powershell as following
# .\agt_internal_install.ps1 [DUT_IP] [AGT_INTERNAL_PACKAGE]

# for example
# .\agt_internal_install.ps1 192.168.123.456 C:\Users\scottyuxiliu\Downloads\agt_internal.tar.gz


# --------------------------------------------------------------------------------

$VerbosePreference = "Continue"
$DebugPreference = "Continue"


$DUT_IP = $args[0]
$DUT_USERNAME = "root"
$DUT_SSH_KEYFILE = "id_rsa"

$AGT_INTERNAL_PACKAGE = $args[1]

Write-Host "INFO`t: remove /usr/local/agt_internal on $DUT_IP if it exists" -ForegroundColor Green
python cros_automation.py rmdir -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local/agt_internal"

Write-Host "INFO`t: create /usr/local/agt_internal on $DUT_IP" -ForegroundColor Green
python cros_automation.py mkdir -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local/agt_internal"

Write-Host "INFO`t: upload $AGT_INTERNAL_PACKAGE to $DUT_IP" -ForegroundColor Green
python cros_automation.py upload -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i $AGT_INTERNAL_PACKAGE -o "/usr/local/agt_internal/agt_internal.tar.gz"

Write-Host "INFO`t: extract /usr/local/agt_internal/agt_internal.tar.gz on $DUT_IP" -ForegroundColor Green
python cros_automation.py extract -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "/usr/local/agt_internal/agt_internal.tar.gz"

Write-Host "INFO`t: remove /usr/local/agt_internal/agt_internal.tar.gz on $DUT_IP" -ForegroundColor Green
python cros_automation.py rm -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "/usr/local/agt_internal/agt_internal.tar.gz"

Write-Host "INFO`t: ls /usr/local/agt_internal on $DUT_IP" -ForegroundColor Green
python cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local/agt_internal"
