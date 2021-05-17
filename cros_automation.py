import logging, argparse, textwrap, time
from custom_logger_formatter import CustomLoggerFormatter
from cros_scenario_launcher import CrosScenarioLauncher
from cros_data_logger import CrosDataLogger
from cros_data_parser import CrosDataParser
from cros_file_handler import CrosFileHandler
from cros_software_controller import CrosSoftwareController

# --------------------------------------------------------------------------------
# Set up logging
logger = logging.getLogger('cros_automation')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s') # output method name too
ch.setFormatter(formatter)

logger.addHandler(ch)
# --------------------------------------------------------------------------------


parser = argparse.ArgumentParser(description="Automation for scenarios on Chrome OS and Chromium OS", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument(
    "job",
    metavar="JOB",
    type=str,
    help=textwrap.dedent(
        '''\
        cros scenario launcher jobs.
        "test": test connection to the test system
        "launch-scenario": launches an autotest scenario [-s/--scenario] on the test system
        "prepare-scenario": prepares an autotest scenario [-s/--scenario] on the test system

        cros data logger jobs.
        "install-atitool": install atitool given the .tar.gz installation file [-i/--input]
        "uninstall-atitool": uninstall atitool on the test system
        "atitool-log": use atitool logging on the test system. support custom arguments [-i/--input].
        "agt-log": use agt logging on the test system. support custom arguments [-i/--input].
        "agt-internal-log": use agt internal logging on the test system. support custom arguments [-i/--input].
        "pac-log": use pac logging on host [-p/--ip] for [-t/--duration] seconds

        cros data parser jobs.
        "ls-local": list items in the local directory [-d/--directory], optionally with name [-i/--input]
        "keyvals-to-csv": convert keyval files [-d/--directory] to .csv files in the same directory
        "keyvals-summary": summarize keyval files in a directory [-d/--directory] to a .csv file [-o/--output]
        "results-charts-summary": summarize results-chart files in a directory [-d/--directory] to a .csv file [-o/--output]
        "agt-cols": extract agt columns from .csv file [-i/--input] and save to .csv file [-o/--output]

        cros file handler jobs.
        "ls": list items in the target system directory [-d/--directory]
        "mkdir": create directory [-d/--directory] on the target system [-p/--ip].
        "rm": remove file [-i/--input] on the target system
        "rmdir": remove directory [-d/--directory] on the target system
        "download": download file [-i/--input] to the target system [-o/--output]
        "upload": upload file [-i/--input] to the target system [-o/--output]
        "extract": extract file [-i/--input] on the target system [-p/--ip].
        "compress": compress directory/file [-i/--input] on the target system [-p/--ip].

        cros software control jobs.
        "reboot": reboot the target system [-p/--ip]
        "cold-reset": cold reset the test system. sudo password [--password] is needed.
        "flashrom": flash coreboot firmware [-i/--input] directly on the DUT [-p/--ip].
        "servo-flashrom": use servo on the host system [-p/--ip] to flash coreboot firmware [-i/--input]. sudo password [--password] is needed.
        "atitool-prog": use atitool programming with argument(s) [-i/--input] on the test system
        "agt-prog": use agt programming with argument(s) [-i/--input] on the test system
        "get-brightness": get brightness on the DUT [-p/--ip].
        "set-brightness": set brightness [-i/--input] nits on the DUT [-p/--ip].
        "get-chrome-os-version": get chrome os version on the DUT [-p/--ip].
        "get-coreboot-fw-version": get coreboot fw version on the DUT [-p/--ip].
        "get-power-supply-info": get power supply info on the DUT [-p/--ip].
        "enable-ac": enable ac on the DUT [-p/--ip].
        "disable-ac": disable ac on the DUT [-p/--ip].

        '''
    )
)
parser.add_argument("-p", "--ip", type=str, help="test system ip address.")
parser.add_argument("-u", "--username", type=str, help="test system username.")
parser.add_argument("-k", "--keyfile", type=str, help="ssh private key file path.")

parser.add_argument("-s", "--scenario", type=str, help="autotest scenario. supported scenarios are in cros_constants.py.")

parser.add_argument("-t", "--duration", type=int, default=60, help="data logging duration in seconds, default %(default)s.")
parser.add_argument("-d", "--directory", type=str, help="directory on the target system.")
parser.add_argument("-i", "--input", type=str, help="data logging source file path, or data parsing file path, or atitool logging/programming arguments.")
parser.add_argument("-o", "--output", type=str, help="data logging output file path.")
parser.add_argument("--password", type=str, help="sudo password.")
parser.add_argument("--index", type=int, default=1, help="atitool logging device index, default %(default)s.")

parser.add_argument("--debug", action="store_true", help="enable debug mode. this captures stdout from all ssh commands executed.") # the store actions create default values of False and True respectively.

args = parser.parse_args()

if args.job == "test-connection":
    with CrosScenarioLauncher(args.ip, args.username, args.keyfile, args.debug) as csl:
        csl.test_connection()

elif args.job == "launch-scenario":
    with CrosScenarioLauncher(args.ip, args.username, args.keyfile, args.debug) as csl:
        csl.launch_scenario(args.scenario)

elif args.job == "prepare-scenario":
    with CrosScenarioLauncher(args.ip, args.username, args.keyfile, args.debug) as csl:
        csl.prepare_scenario(args.scenario)

elif args.job == "install-atitool":
    with CrosFileHandler(args.ip, args.username, args.keyfile, True) as cfh:
        cfh.mkdir("/usr/local/atitool")
        cfh.upload(args.input, "/usr/local/atitool/atitool.tar.gz")
        cfh.extract("/usr/local/atitool/atitool.tar.gz")
        cfh.rm("/usr/local/atitool/atitool.tar.gz")

elif args.job == "uninstall-atitool":
    with CrosFileHandler(args.ip, args.username, args.keyfile, True) as cfh:
        cfh.rmdir("/usr/local/atitool")

elif args.job == "atitool-log":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.atitool_log(args.duration, args.index, args.input, args.output)

elif args.job == "agt-log":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.agt_log(args.duration, args.index, args.input, args.output)

elif args.job == "agt-internal-log":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.agt_internal_log(args.duration, args.index, args.input, args.output)

elif args.job == "pac-log":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.pac_log(args.duration, args.password)

# cros data parser jobs
elif args.job == "ls-local":
    with CrosDataParser() as cdp:
        cdp.ls_local(args.directory, args.input)

elif args.job == "keyvals-to-csv":
    with CrosDataParser() as cdp:
        keyval_paths = cdp.ls_local(args.directory, "*keyval*")
        cdp.keyvals_to_csv(keyval_paths)

elif args.job == "keyvals-summary":
    with CrosDataParser() as cdp:
        keyval_paths = cdp.ls_local(args.directory, "*keyval*")
        cdp.keyvals_summary(keyval_paths, args.output)

elif args.job == "results-charts-summary":
    with CrosDataParser() as cdp:
        results_chart_paths = cdp.ls_local(args.directory, "*results_chart*.json")
        cdp.results_charts_summary(results_chart_paths, args.output)

elif args.job == "agt-cols":
    with CrosDataParser() as cdp:
        cdp.agt_cols(args.input, args.output)


# cros file handler jobs
elif args.job == "ls":
    with CrosFileHandler(args.ip, args.username, args.keyfile, args.debug) as cfh:
        cfh.ls(args.directory)

elif args.job == "mkdir":
    with CrosFileHandler(args.ip, args.username, args.keyfile, args.debug) as cfh:
        cfh.mkdir(args.directory)

elif args.job == "rm":
    with CrosFileHandler(args.ip, args.username, args.keyfile, args.debug) as cfh:
        cfh.rm(args.input)

elif args.job == "rmdir":
    with CrosFileHandler(args.ip, args.username, args.keyfile, args.debug) as cfh:
        cfh.rmdir(args.directory)

elif args.job == "download":
    with CrosFileHandler(args.ip, args.username, args.keyfile, args.debug) as cfh:
        cfh.download(args.input, args.output)

elif args.job == "upload":
    with CrosFileHandler(args.ip, args.username, args.keyfile, args.debug) as cfh:
        cfh.upload(args.input, args.output)

elif args.job == "extract":
    with CrosFileHandler(args.ip, args.username, args.keyfile, args.debug) as cfh:
        cfh.extract(args.input)

elif args.job == "compress":
    with CrosFileHandler(args.ip, args.username, args.keyfile, args.debug) as cfh:
        cfh.compress(args.input)

# cros software control jobs
elif args.job == "reboot":
    with CrosSoftwareController(args.ip, args.username, args.keyfile, args.debug) as csc:
        csc.reboot()

elif args.job == "cold-reset":
    with CrosSoftwareController(args.ip, args.username, args.keyfile, args.debug) as csc:
        csc.cold_reset(sudo_password=args.sudo)

elif args.job == "flashrom":
    with CrosSoftwareController(args.ip, args.username, args.keyfile, args.debug) as csc:
        csc.flashrom(args.input)

elif args.job == "servo-flashrom":
    with CrosSoftwareController(args.ip, args.username, args.keyfile, args.debug) as csc:
        csc.servo_flashrom(args.input, sudo_password=args.sudo)

elif args.job == "atitool-prog":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.atitool_prog(args.input)

elif args.job == "agt-prog":
    with CrosSoftwareController(args.ip, args.username, args.keyfile, args.debug) as csc:
        csc.agt_prog(args.input)

elif args.job == "get-brightness":
    with CrosSoftwareController(args.ip, args.username, args.keyfile, args.debug) as csc:
        csc.get_brightness()

elif args.job == "set-brightness":
    with CrosSoftwareController(args.ip, args.username, args.keyfile, args.debug) as csc:
        csc.set_brightness(args.input)

elif args.job == "get-chrome-os-version":
    with CrosSoftwareController(args.ip, args.username, args.keyfile, args.debug) as csc:
        csc.get_chrome_os_version()

elif args.job == "get-coreboot-fw-version":
    with CrosSoftwareController(args.ip, args.username, args.keyfile, args.debug) as csc:
        csc.get_coreboot_fw_version()

elif args.job == "get-power-supply-info":
    with CrosSoftwareController(args.ip, args.username, args.keyfile, args.debug) as csc:
        csc.get_power_supply_info()

elif args.job == "enable-ac":
    with CrosSoftwareController(args.ip, args.username, args.keyfile, args.debug) as csc:
        csc.enable_ac()

elif args.job == "disable-ac":
    with CrosSoftwareController(args.ip, args.username, args.keyfile, args.debug) as csc:
        csc.disable_ac()

else:
    pass



