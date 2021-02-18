import logging, argparse
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


parser = argparse.ArgumentParser(description="Automation for scenarios on Chrome OS and Chromium OS")
parser.add_argument("test_system_ip_address", metavar="ip", type=str, help="test system ip address")
parser.add_argument("test_system_username", metavar="username", type=str, help="test system username")
parser.add_argument("--scenario", type=str, default="init_ssh_connection", help="scenarios, default 'init_ssh_connection'. possible values: 'init_ssh_connection', 'enter_s0i3'.")
parser.add_argument("--ssh_private_key_file", type=str, default=None, help="ssh private key file path")

args = parser.parse_args()

cs = CrosScenarios()

if args.scenario == "init_ssh_connection":
    cs.init_ssh_connection(args.test_system_ip_address, args.test_system_username, args.ssh_private_key_file)

elif args.scenario == "enter_s0i3":
    cs.enter_s0i3(args.test_system_ip_address, args.test_system_username, args.ssh_private_key_file)

else:
    pass



