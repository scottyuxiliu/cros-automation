# --------------------------------------------------------------------------------

# you may run this ps script from powershell as following
# .\agt_install.ps1 [DUT_IP] [AGT_PACKAGE]

# for example
# .\agt_install.ps1 "192.168.123.456" "C:\Users\scottyuxiliu\Downloads\agt.tar.gz"


# --------------------------------------------------------------------------------

$VerbosePreference = "Continue"
$DebugPreference = "Continue"


$DUT_IP = $args[0]
$DUT_USERNAME = "root"
$DUT_SSH_KEYFILE = "id_rsa"

$AGT_PACKAGE = $args[1]

Write-Verbose "create /usr/local/agt directory on $DUT_IP ..."
python .\cros_automation.py mkdir -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local/agt"

Write-Verbose "upload $AGT_PACKAGE to $DUT_IP ..."
python .\cros_automation.py upload -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i $AGT_PACKAGE -o "/usr/local/agt/agt.tar.gz"

Write-Verbose "extract /usr/local/agt/agt.tar.gz on $DUT_IP ..."
python .\cros_automation.py extract -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "/usr/local/agt/agt.tar.gz"

Write-Verbose "remove /usr/local/agt/agt.tar.gz on $DUT_IP ..."
python .\cros_automation.py rm -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -i "/usr/local/agt/agt.tar.gz"

Write-Verbose "ls /usr/local/agt on $DUT_IP ..."
python .\cros_automation.py ls -p $DUT_IP -u $DUT_USERNAME -k $DUT_SSH_KEYFILE -d "/usr/local/agt"
