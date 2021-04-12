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

### Run graphics_WebGLAquarium

```
python .\cros_automation.py launch-scenario -s "graphics_webglaquarium" -p "192.168.123.456" -u "root" -k "id_rsa"
```

---

### Capture ATITOOL log

```
python .\cros_automation.py atitool-log -p "192.168.123.456" -u "root" -k "id_rsa" -t 120 -o "atitool_log.csv"
```

### Capture AGT log

```
python .\cros_automation.py agt-log -p "192.168.123.456" -u "root" -k "id_rsa" -t 120 -o "agt_log.csv"
```

---

### List items in a directory

```
# list items in a test system directory
python .\cros_automation.py ls -p "192.168.123.456" -u "root" -k "id_rsa" -d "/usr/local/atitool"

# list items in a local directory
python .\cros_automation.py ls-local -d "C:\Users\scottyuxiliu\Documents\cros-automation\unittest\input"

# list items in a local directory, with name "keyval*"
python .\cros_automation.py ls-local -d "C:\Users\scottyuxiliu\Documents\cros-automation\unittest\input" -i "keyval*"
```


### Download atitool_log.csv to the local host system

```
python .\cros_automation.py download -p "192.168.123.456" -u "root" -k "id_rsa" -i "/usr/local/atitool/atitool_log.csv" -o "C:\Users\scottyuxiliu\Downloads\atitool_log.csv"
```

### Upload atitool_log.csv to the local host system

```
python .\cros_automation.py upload -p "192.168.123.456" -u "root" -k "id_rsa" -i "C:\Users\scottyuxiliu\Downloads\atitool_log.csv" -o "/usr/local/atitool/atitool_log.csv"
```

### Remove atitool_log.csv on the test system

```
python .\cros_automation.py rm -p "192.168.123.456" -u "root" -k "id_rsa" -i "/usr/local/atitool/atitool_log.csv"
```

### Remove /usr/local/atitool directory on the test system

```
python .\cros_automation.py rmdir -p "192.168.123.456" -u "root" -k "id_rsa" -d "/usr/local/atitool"
```

### Cold-reset the test system through servo

Servo is needed and should be connected to the host system

```
python .\cros_automation.py cold-reset -p [host_ip] -u [host_username] -k [ssh_private_key_file] --sudo [sudo_password]
```

For example,

```
python .\cros_automation.py cold-reset -p "192.168.111.111" -u "admin" -k "id_rsa" --sudo "password"
```

### Summarize results-chart.json files to a .csv file

```
python .\cros_automation.py results-charts-summary -d [directory] -o [output_file]
```

For example,

```
python .\cros_automation.py results-charts-summary -d "C:\Users\scottyuxiliu\Documents\cros-automation\unittest\input" -o "results_charts_summary.csv"
```


## To-do
1.   Organize cros software control jobs
2.   Add flashrom support
3.   Add chroot support