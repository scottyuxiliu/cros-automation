import logging, argparse, textwrap
from cros_scenarios import CrosScenarios

# --------------------------------------------------------------------------------
# Set up logging
logger = logging.getLogger('cros_automation')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('cros_automation.log', mode='w') # overwrite existing log file
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s') # output method name too
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)
# --------------------------------------------------------------------------------


parser = argparse.ArgumentParser(description="Automation for scenarios on Chrome OS and Chromium OS", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument(
    "scenario",
    metavar="scenario",
    type=str,
    help=textwrap.dedent(
        '''\
        scenarios.
        "test": test connection to the test system
        "s0i3": enter s0i3 on the test system
        "parse": parse top logs
        '''
    )
)
parser.add_argument("-p", "--ip", type=str, default=None, help="test system ip address, default %(default)s.")
parser.add_argument("-u", "--username", type=str, default=None, help="test system username, default %(default)s.")
parser.add_argument("-i", "--keyfile", type=str, default=None, help="ssh private key file path, default %(default)s.")

args = parser.parse_args()

if args.scenario == "test":
    if args.ip is None:
        parser.error("test scenario requires test system ip address (-p/--ip)")
    elif args.username is None:
        parser.error("test scenario requires test system username (-u/--username)")
    elif args.keyfile is None:
        parser.error("test scenario requires ssh private key file path (-i/--keyfile)")
    else:
        with CrosScenarios(args.test_system_ip_address, args.test_system_username, args.ssh_private_key_file) as cs:
            cs.test_connection()

elif args.scenario == "s0i3":
    if args.ip is None:
        parser.error("test scenario requires test system ip address (-p/--ip)")
    elif args.username is None:
        parser.error("test scenario requires test system username (-u/--username)")
    elif args.keyfile is None:
        parser.error("test scenario requires ssh private key file path (-i/--keyfile)")
    else:
        with CrosScenarios(args.test_system_ip_address, args.test_system_username, args.ssh_private_key_file) as cs:
            cs.enter_s0i3()

else:
    pass



