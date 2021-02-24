# cros-automation
Automation for scenarios on Chrome OS and Chromium OS

For Windows users, a sample powershell script `cros_automation.ps1` is included to show a simple flow of what this automation can achieve.


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
python .\cros_automation.py ls -p "10.4.44.5" -u "root" -k "id_rsa" -d "/usr/local/atitool"
```


Download atitool_log.csv to the local host system

```
python .\cros_automation.py download -p "192.168.123.456" -u "root" -k "id_rsa" -i "/usr/local/atitool/atitool_log.csv" -o "C:\Users\scottyuxiliu\Downloads\atitool_log.csv"
```

Remove atitool_log.csv on the test system

```
python .\cros_automation.py remove -p "192.168.123.456" -u "root" -k "id_rsa" -i "/usr/local/atitool/atitool_log.csv"
```