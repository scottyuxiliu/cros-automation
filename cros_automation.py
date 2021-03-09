import logging, argparse, textwrap, time
from custom_logger_formatter import CustomLoggerFormatter
from cros_scenarios import CrosScenarios
from cros_data_logger import CrosDataLogger
from cros_data_parser import CrosDataParser

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
        "plt-1h": launch power_loadtest_1hour on the test system
        "aquarium": launch aquarium on the test system
        "glbench": launch glbench on the test system

        data logging scenarios.
        "install-atitool": install atitool given the .tar.gz installation file [-i/--input]
        "uninstall-atitool": uninstall atitool on the test system
        "atitool-log": use atitool logging on the test system. support custom arguments [-i/--input].
        "atitool-prog": use atitool programming with argument(s) [-i/--input] on the test system
        "install-agt": install agt given the .tar.gz installation file [-i/--input]
        "uninstall-agt": uninstall agt on the test system
        "agt-internal-log": use agt internal logging on the test system. support custom arguments [-i/--input].
        "agt-log": use agt logging on the test system. support custom arguments [-i/--input].
        "download": download file [-i/--input] to the local host system [-o/--output]
        "upload": upload file [-i/--input] to the test system [-o/--output]
        "remove": remove file [-i/--input] on the test system
        "rmdir": remove directory [-d/--directory] on the test system
        "ls": list items in the test system directory [-d/--directory]

        data parsing scenarios.
        "ls-local": list items in the local directory [-d/--directory]
        "keyvals-to-csv": convert keyval files [-d/--directory] to .csv files in the same directory
        "keyvals-summary": summarize keyval file contents [-d/--directory] to a .csv file [-o/--output]
        '''
    )
)
parser.add_argument("-p", "--ip", type=str, help="test system ip address.")
parser.add_argument("-u", "--username", type=str, help="test system username.")
parser.add_argument("-k", "--keyfile", type=str, help="ssh private key file path.")

parser.add_argument("-t", "--duration", type=int, default=60, help="data logging duration in seconds, default %(default)s.")
parser.add_argument("-d", "--directory", type=str, help="directory on the test system.")
parser.add_argument("-i", "--input", type=str, help="data logging source file name, or data parsing file name, or atitool logging/programming arguments.")
parser.add_argument("-o", "--output", type=str, help="data logging output file name.")
parser.add_argument("--index", type=int, default=1, help="atitool logging device index, default %(default)s.")

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

elif args.scenario == "plt-1h":
    with CrosScenarios(args.ip, args.username, args.keyfile, args.debug) as cs:
        cs.launch_power_loadtest_1hour()

elif args.scenario == "aquarium":
    with CrosScenarios(args.ip, args.username, args.keyfile, args.debug) as cs:
        cs.launch_aquarium()

elif args.scenario == "glbench":
    with CrosScenarios(args.ip, args.username, args.keyfile, args.debug) as cs:
        cs.launch_glbench()

elif args.scenario == "install-atitool":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.mkdir("/usr/local/atitool")
        cdl.upload_file(args.input, "/usr/local/atitool/atitool.tar.gz")
        cdl.extract_file("/usr/local/atitool/atitool.tar.gz")
        cdl.remove_file("/usr/local/atitool/atitool.tar.gz")

elif args.scenario == "uninstall-atitool":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.rmdir("/usr/local/atitool")

elif args.scenario == "atitool-log":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.atitool_log(args.duration, args.index, args.input, args.output)

elif args.scenario == "atitool-prog":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.atitool_prog(args.input)

elif args.scenario == "install-agt":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.mkdir("/usr/local/agt")
        cdl.upload_file(args.input, "/usr/local/agt/agt.tar.gz")
        cdl.extract_file("/usr/local/agt/agt.tar.gz")
        cdl.remove_file("/usr/local/agt/agt.tar.gz")

        items = cdl.ls("/usr/local/agt")
        if len(items) == 1:
            print(items)
            print(items[0])
            print(f"/usr/local/agt/{items[0]}/*")
            # cdl.move_file(f"/usr/local/agt/{items[0]}/*", "/usr/local/agt")
            # cdl.rmdir(f"/usr/local/agt/{items[0]}")



elif args.scenario == "uninstall-agt":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.rmdir("/usr/local/agt")

elif args.scenario == "agt-log":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.agt_log(args.duration, args.index, args.input, args.output)

elif args.scenario == "agt-internal-log":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.agt_internal_log(args.duration, args.index, args.input, args.output)

elif args.scenario == "download":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.download_file(args.input, args.output)

elif args.scenario == "upload":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.upload_file(args.input, args.output)

elif args.scenario == "remove":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.remove_file(args.input)

elif args.scenario == "rmdir":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.rmdir(args.directory)

elif args.scenario == "ls":
    with CrosDataLogger(args.ip, args.username, args.keyfile, args.debug) as cdl:
        cdl.ls(args.directory)

elif args.scenario == "ls-local":
    with CrosDataParser() as cdp:
        cdp.ls_local(args.directory, args.input)

elif args.scenario == "keyvals-to-csv":
    with CrosDataParser() as cdp:
        keyval_paths = cdp.ls_local(args.directory, "*keyval*")
        cdp.keyvals_to_csv(keyval_paths)

elif args.scenario == "keyvals-summary":
    with CrosDataParser() as cdp:
        keyval_paths = cdp.ls_local(args.directory, "*keyval*")
        cdp.keyvals_summary(keyval_paths, args.output)

else:
    pass



