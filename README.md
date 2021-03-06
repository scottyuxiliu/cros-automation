# cros-automation
Automate benchmarks and tasks in Chrome OS and Chromium OS.

For Windows users, a sample powershell script `cros_automation.ps1` is included to show a simple flow of what this automation can achieve.

For Ubuntu users, sample bash script `measurement.sh` is included.


<!-- ## Pre-requisites
1.   `cros_sdk` should already be set up on a host system. `cros_sdk` guide: https://chromium.googlesource.com/chromiumos/docs/+/main/developer_guide.md
2.   `autotest` should be launched at least once. This way, `/usr/local/autotest` directory is set up on the test system. A sample scenario to run using `autotest` is shown here: https://chromium.googlesource.com/chromiumos/third_party/autotest/+/refs/heads/master/client/site_tests/power_LoadTest/README.md -->

## Quick-start guide
1.   Download latest Python from https://www.python.org/
1.   Install all required Python packages by running `pip install -r requirements`
2.   Run `python cros_automation.py --help` to see a list of available arguments and their usages


## Available jobs



### Test connection
```
python cros_automation.py test-connection -p [dut_ip] -u [dut_username] -k [dut_ssh_keyfile]

# for example
python cros_automation.py test-connection -p 192.168.123.456 -u root -k id_rsa
```

### Launch scenarios

```
python cros_automation.py launch-scenario -s [scenario] -p [dut_ip] -u [dut_username] -k [dut_ssh_keyfile]

# for example
python cros_automation.py launch-scenario -s graphics_WebGLAquarium -p 192.168.123.456 -u root -k id_rsa
```

### Capture ATITOOL log

```
python .\cros_automation.py atitool-log -p "192.168.123.456" -u "root" -k "id_rsa" -t 120 -o "atitool_log.csv"
```

### Capture AGT log

```
python cros_automation.py agt-log -p [dut_ip] -u [dut_username] -k [dut_ssh_keyfile] -t [duration] -o [output_file]

# for example
python cros_automation.py agt-log -p "192.168.123.456" -u "root" -k "id_rsa" -t 120 -o "agt_log.csv"
```

### List items in a directory

```
# list items in a DUT directory
python cros_automation.py ls -p 192.168.123.456 -u root -k id_rsa -d /usr/local

# list items in a local directory
python cros_automation.py ls-local -d C:\Users\scottyuxiliu\Documents\cros-automation\unittest\input

# list items in a local directory, with name "keyval*"
python cros_automation.py ls-local -d C:\Users\scottyuxiliu\Documents\cros-automation\unittest\input -i "keyval*"
```

### Remove file on the DUT

```
python .\cros_automation.py rm -p "192.168.123.456" -u "root" -k "id_rsa" -i "/usr/local/atitool/atitool_log.csv"
```

### Remove directory on the DUT

```
python .\cros_automation.py rmdir -p "192.168.123.456" -u "root" -k "id_rsa" -d "/usr/local/atitool"
```


### Download file
```
python cros_automation.py download -p [dut_ip] -u [dut_username] -k [dut_ssh_keyfile] -i [source] -o [dest]

# for example
python cros_automation.py download -p "192.168.123.456" -u "root" -k "id_rsa" -i "/usr/local/atitool/atitool_log.csv" -o "/home/scottyuxiliu/Downloads/atitool_log.csv"
python cros_automation.py download -p "192.168.123.456" -u "root" -k "id_rsa" -i "/usr/local/agt/agt_log.csv" -o "C:\Users\scottyuxiliu\Downloads\agt_log.csv"
```

### Upload file to the DUT

```
python .\cros_automation.py upload -p "192.168.123.456" -u "root" -k "id_rsa" -i "C:\Users\scottyuxiliu\Downloads\atitool_log.csv" -o "/usr/local/atitool/atitool_log.csv"
```


### Cold-reset the test system through servo

Servo is needed and should be connected to the host system

```
python .\cros_automation.py cold-reset -p [host_ip] -u [host_username] -k [dut_ssh_keyfile] --sudo [sudo_password]
```

For example,

```
python .\cros_automation.py cold-reset -p "192.168.111.111" -u "admin" -k "id_rsa" --sudo "password"
```

### Summarize results-chart.json files to a .csv file


```
python cros_automation.py results-charts-summary -d [directory] -o [output_file]

# for example
python cros_automation.py results-charts-summary -d ~/Downloads/test/ -o ~/Downloads/test/results_charts_summary.csv
python cros_automation.py results-charts-summary -d C:\Users\scottyuxiliu\Documents\cros-automation\unittest\input -o results_charts_summary.csv
```



### List items in a directory


```
python cros_automation.py ls -p "192.168.123.456" -u "root" -k "id_rsa" -d "/usr/local"
```


### Remove file on the DUT

```
python cros_automation.py rm -p "192.168.123.456" -u "root" -k "id_rsa" -i "/usr/local/atitool/atitool_log.csv"
```

### Reboot

```
python cros_automation.py reboot -p [dut_ip] -u [dut_username] -k [dut_ssh_keyfile]

# for example
python cros_automation.py reboot -p 192.168.123.456 -u root -k id_rsa
```

### Get brightness
```
python cros_automation.py get-brightness -p [dut_ip] -u [dut_username] -k [dut_ssh_keyfile]

# for example
python cros_automation.py get-brightness -p 192.168.123.456 -u root -k id_rsa
```

### Set brightness
```
python cros_automation.py set-brightness -p [dut_ip] -u [dut_username] -k [dut_ssh_keyfile] -i [nits]

# for example
python cros_automation.py set-brightness -p 192.168.123.456 -u root -k id_rsa -i 80
```

### Get power supply info
```
python cros_automation.py get-power-supply-info -p [dut_ip] -u [dut_username] -k [dut_ssh_keyfile]

# for example
python cros_automation.py get-power-supply-info -p 192.168.123.456 -u root -k id_rsa
```

### Enable AC
```
python cros_automation.py enable-ac -p [dut_ip] -u [dut_username] -k [dut_ssh_keyfile]

# for example
python cros_automation.py enable-ac -p 192.168.123.456 -u root -k id_rsa
```

### Disable AC
```
python cros_automation.py disable-ac -p [dut_ip] -u [dut_username] -k [dut_ssh_keyfile]

# for example
python cros_automation.py disable-ac -p 192.168.123.456 -u root -k id_rsa
```


## To-do
1.   Organize cros software control jobs
2.   Add flashrom support
3.   Add chroot support