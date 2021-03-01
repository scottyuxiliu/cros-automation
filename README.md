# cros-automation
Automation for scenarios on Chrome OS and Chromium OS

For Windows users, a sample powershell script `cros_automation.ps1` is included to show a simple flow of what this automation can achieve.


## Pre-requisites
1.   `cros_sdk` should already be set up on a host system. `cros_sdk` guide: https://chromium.googlesource.com/chromiumos/docs/+/main/developer_guide.md
2.   `autotest` should be launched at least once. This way, `/usr/local/autotest` directory is set up on the test system. A sample scenario to run using `autotest` is shown here: https://chromium.googlesource.com/chromiumos/third_party/autotest/+/refs/heads/master/client/site_tests/power_LoadTest/README.md

## Quick-start guide
1.   Install all required Python packages by running `pip install -r requirements.txt`
2.   Run `python .\cros_automation.py --help` to see a list of available arguments and their usages


## Common use cases

Capture ATITOOL log

```
python .\cros_automation.py atitool -p "192.168.123.456" -u "root" -k "id_rsa" -t 120 -o "atitool_log.csv"
```

Run graphics_WebGLAquarium

```
python .\cros_automation.py aquarium -p "192.168.123.456" -u "root" -k "id_rsa"
```

List items in a directory

```
# list items in a test system directory
python .\cros_automation.py ls -p "192.168.123.456" -u "root" -k "id_rsa" -d "/usr/local/atitool"

# list items in a local directory
python .\cros_automation.py ls-local -d "C:\Users\scottyuxiliu\Documents\cros-automation\unittest\input"
```


Download atitool_log.csv to the local host system

```
python .\cros_automation.py download -p "192.168.123.456" -u "root" -k "id_rsa" -i "/usr/local/atitool/atitool_log.csv" -o "C:\Users\scottyuxiliu\Downloads\atitool_log.csv"
```

Remove atitool_log.csv on the test system

```
python .\cros_automation.py remove -p "192.168.123.456" -u "root" -k "id_rsa" -i "/usr/local/atitool/atitool_log.csv"
```