import logging, argparse, textwrap, time
from custom_logger_formatter import CustomLoggerFormatter
from cros_scenario_launcher import CrosScenarioLauncher
from cros_data_logger import CrosDataLogger
from cros_data_parser import CrosDataParser
from cros_file_handler import CrosFileHandler
from cros_hw_ctrl import CrosHwCtrl

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
    metavar="job",
    type=str,
    help=textwrap.dedent(
        '''\
        cros scenario launcher jobs.
        "test": test connection to the test system
        "reboot": reboot the test system
        "s0i3": enter s0i3 on the test system
        "idle": do nothing on the test system
        "launch-scenario": launches an autotest scenario [-s/--scenario] on the test system
        "prepare-scenario": prepares an autotest scenario [-s/--scenario] on the test system

        cros data logger jobs.
        "install-atitool": install atitool given the .tar.gz installation file [-i/--input]
        "uninstall-atitool": uninstall atitool on the test system
        "atitool-log": use atitool logging on the test system. support custom arguments [-i/--input].
        "atitool-prog": use atitool programming with argument(s) [-i/--input] on the test system
        "uninstall-agt": uninstall agt on the test system
        "agt-internal-log": use agt internal logging on the test system. support custom arguments [-i/--input].
        "agt-log": use agt logging on the test system. support custom arguments [-i/--input].

        cros data parser jobs.
        "ls-local": list items in the local directory [-d/--directory]
        "keyvals-to-csv": convert keyval files [-d/--directory] to .csv files in the same directory
        "keyvals-summary": summarize keyval file contents [-d/--directory] to a .csv file [-o/--output]

        cros file handler jobs.
        "ls": list items in the target system directory [-d/--directory]
        "mkdir": create directory [-d/--directory] on the target system
        "rm": remove file [-i/--input] on the target system
        "rmdir": remove directory [-d/--directory] on the target system
        "download": download file [-i/--input] to the target system [-o/--output]
        "upload": upload file [-i/--input] to the target system [-o/--output]

        cros hardware control jobs.
        "cold-reset": cold reset the test system. sudo password [--sudo] is needed.

        cros software control jobs
        "install-agt": install agt given the .tar.gz installation file [-i/--input]
        '''
    )
)
parser.add_argument("-p", "--ip", type=str, help="test system ip address.")
parser.add_argument("-u", "--username", type=str, help="test system username.")
parser.add_argument("-k", "--keyfile", type=str, help="ssh private key file path.")

parser.add_argument("-s", "--scenario", type=str, help="autotest scenario. supported scenarios are plt-1h, aquarium, glbench, ptl.")

parser.add_argument("-t", "--duration", type=int, default=60, help="data logging duration in seconds, default %(default)s.")
parser.add_argument("-d", "--directory", type=str, help="directory on the test system.")
parser.add_argument("-i", "--input", type=str, help="data logging source file name, or data parsing file name, or atitool logging/programming arguments.")
parser.add_argument("-o", "--output", type=str, help="data logging output file name.")
parser.add_argument("--sudo", type=str, help="sudo password.")
parser.add_argument("--index", type=int, default=1, help="atitool logging device index, default %(default)s.")

parser.add_argument("--debug", action="store_true", help="enable debug mode. this captures stdout from all ssh commands executed.") # the store actions create default values of False and True respectively.

args = parser.parse_args()

if args.job == "test":
    with CrosScenarioLauncher(args.ip, args.username, args.keyfile, args.debug) as cs:
        cs.test_connection()

elif args.job == "idle":
    pass

elif args.job == "reboot":
    with CrosScenarioLauncher(args.ip, args.username, args.keyfile, args.debug) as cs:
        cs.reboot()

elif args.job == "s0i3":
    with CrosScenarioLauncher(args.ip, args.username, args.keyfile, args.debug) as cs:
        cs.enter_s0i3()

elif args.job == "launch-scenario":
    with CrosScenarioLauncher(args.ip, args.username, args.keyfile, args.debug) as cs:
        cs.launch_scenario(args.scenario)

elif args.job == "prepare-scenario":
    with CrosScenarioLauncher(args.ip, args.username, args.keyfile, args.debug) as cs:
        cs.prepare_scenario(args.scenario)

elif args.job == "install-atitool":
    with CrosFileHandler(args.ip, args.username, args.keyfile, True) as cfh:
        cfh.mkdir("/usr/local/atitool")
        cfh.upload(args.input, "/usr/local/atitool/atitool.tar.gz")
        cfh.extract("/usr/local/atitool/atitool.tar.gz", target_is_linux=True)
        cfh.rm("/usr/local/atitool/atitool.tar.gz")

elif args.job == "uninstall-atitool":
    with CrosFileHandler(args.ip, args.username, args.keyfile, True) as cfh:
        cfh.rmdir("/usr/local/atitool")

elif args.job == "atitool-log":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.atitool_log(args.duration, args.index, args.input, args.output)

elif args.job == "atitool-prog":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.atitool_prog(args.input)

elif args.job == "uninstall-agt":
    with CrosFileHandler(args.ip, args.username, args.keyfile, args.debug) as cfh:
        cfh.rmdir("/usr/local/agt")

elif args.job == "agt-log":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.agt_log(args.duration, args.index, args.input, args.output)

elif args.job == "agt-internal-log":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.agt_internal_log(args.duration, args.index, args.input, args.output)

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

# cros hardware control jobs
elif args.job == "cold-reset":
    with CrosHwCtrl(args.ip, args.username, args.keyfile, args.debug) as chc:
        chc.cold_reset(sudo_password=args.sudo)

# cros software control jobs
elif args.job == "install-agt":
    with CrosFileHandler(args.ip, args.username, args.keyfile, True) as cfh:
        cfh.mkdir("/usr/local/agt")
        cfh.upload(args.input, "/usr/local/agt/agt.tar.gz")
        cfh.extract("/usr/local/agt/agt.tar.gz", target_is_linux=True)
        cfh.ls("/usr/local/agt")
        cfh.rm("/usr/local/agt/agt.tar.gz")

else:
    pass



