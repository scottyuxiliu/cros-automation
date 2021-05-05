# --------------------------------------------------------------------------------

# you may run this ps script from powershell as following
# .\agt_install.ps1 [TEST_SYS_IP] [AGT_PACKAGE]

# for example
# .\agt_install.ps1 "192.168.123.456" "C:\Users\scottyuxiliu\Downloads\agt.tar.gz"


# --------------------------------------------------------------------------------

$VerbosePreference = "Continue"
$DebugPreference = "Continue"


$TEST_SYS_IP = $args[0]
$TEST_SYS_USERNAME = "root"
$TEST_SYS_KEYFILE = "id_rsa"

$AGT_PACKAGE = $args[1]

Write-Verbose "create /usr/local/agt directory on $TEST_SYS_IP ..."
python .\cros_automation.py mkdir -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "/usr/local/agt"

Write-Verbose "upload $AGT_PACKAGE to $TEST_SYS_IP ..."
python .\cros_automation.py upload -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i $AGT_PACKAGE -o "/usr/local/agt/agt.tar.gz"

Write-Verbose "extract /usr/local/agt/agt.tar.gz on $TEST_SYS_IP ..."
python .\cros_automation.py extract -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "/usr/local/agt/agt.tar.gz"

Write-Verbose "remove /usr/local/agt/agt.tar.gz on $TEST_SYS_IP ..."
python .\cros_automation.py rm -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -i "/usr/local/agt/agt.tar.gz"

Write-Verbose "ls /usr/local/agt on $TEST_SYS_IP ..."
python .\cros_automation.py ls -p $TEST_SYS_IP -u $TEST_SYS_USERNAME -k $TEST_SYS_KEYFILE -d "/usr/local/agt"
