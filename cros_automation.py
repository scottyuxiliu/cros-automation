import logging, argparse, textwrap
from custom_logger_formatter import CustomLoggerFormatter
from cros_scenarios import CrosScenarios
from cros_data_logger import CrosDataLogger

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
    "scenario",
    metavar="scenario",
    type=str,
    help=textwrap.dedent(
        '''\
        cros scenarios.
        "test": test connection to the test system
        "reboot": reboot the test system
        "s0i3": enter s0i3 on the test system
        "idle": do nothing on the test system
        "plt": launch power_loadtest on the test system
        "aquarium": launch aquarium on the test system

        data logging scenarios.
        "atitool": use atitool logging on the test system
        "download": download file [-i/--input] to the local host system [-o/--output]
        "remove": remove file [-i/--input] on the test system
        "ls": list items in the directory [-d/--directory]

        data parsing scenarios.
        "parse": parse top logs
        '''
    )
)
parser.add_argument("-p", "--ip", type=str, required=True, help="test system ip address, default %(default)s.")
parser.add_argument("-u", "--username", type=str, required=True, help="test system username, default %(default)s.")
parser.add_argument("-k", "--keyfile", type=str, required=True, help="ssh private key file path, default %(default)s.")

parser.add_argument("-t", "--duration", type=int, default=60, help="data logging duration in seconds.")
parser.add_argument("-d", "--directory", type=str, help="directory on the test system.")
parser.add_argument("-i", "--input", type=str, default="pm.csv", help="data logging source file name.")
parser.add_argument("-o", "--output", type=str, default="pm.csv", help="data logging output file name.")

parser.add_argument("--debug", action="store_true", help="enable debug mode. this captures stdout from all ssh commands executed.") # the store actions create default values of False and True respectively.

args = parser.parse_args()

if args.scenario == "test":
    with CrosScenarios(args.ip, args.username, args.keyfile, args.debug) as cs:
        cs.test_connection()

elif args.scenario == "idle":
    pass

elif args.scenario == "reboot":
    with CrosScenarios(args.ip, args.username, args.keyfile, args.debug) as cs:
        cs.reboot()

elif args.scenario == "s0i3":
    with CrosScenarios(args.ip, args.username, args.keyfile, args.debug) as cs:
        cs.enter_s0i3()

elif args.scenario == "plt":
    with CrosScenarios(args.ip, args.username, args.keyfile, args.debug) as cs:
        cs.launch_power_loadtest()

elif args.scenario == "aquarium":
    with CrosScenarios(args.ip, args.username, args.keyfile, args.debug) as cs:
        cs.launch_aquarium()

elif args.scenario == "atitool":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.launch_atitool_logging(args.duration, args.output)

elif args.scenario == "download":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.download_file(args.input, args.output)

elif args.scenario == "remove":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.remove_file(args.input)

elif args.scenario == "ls":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.ls(args.directory)

else:
    pass



