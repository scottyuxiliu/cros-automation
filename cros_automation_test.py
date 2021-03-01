import logging, unittest
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

class CrosAutomationCase(unittest.TestCase):
    def setUp(self):
        """The setUp() method is a special method that the unit testing framework executes before each test respectively.

        By changing the application configuration to sqlite://, I get SQLAlchemy to use an in-memory SQLite database during the tests. This prevents the unit tests from using the regular database that I use for development.
        """

        self.test_system_ip_address = "10.6.145.180"
        self.test_system_username = "root"
        self.ssh_private_key_file = "id_rsa"
        self.debug = True


    def tearDown(self):
        """The tearDown() method is a special method that the unit testing framework executes after each test respectively.
        """


    def test_cs_test_connection(self):
        with CrosScenarios(self.test_system_ip_address, self.test_system_username, self.ssh_private_key_file, self.debug) as cs:
            self.assertEqual(cs.test_connection(), True)

    def test_cdl_test_connection(self):
        with CrosDataLogger(self.test_system_ip_address, self.test_system_username, self.ssh_private_key_file, self.debug) as cdl:
            self.assertEqual(cdl.test_connection(), True)
    
    def test_cdp_ls_local_1(self):
        """test CrosDataParser.ls_local with name=None
        """
        expected = ["unittest\\input\\keyval_1", "unittest\\input\\keyval_2", "unittest\\input\\keyval_3", "unittest\\input\\keyval_4"]
        result = []

        with CrosDataParser() as cdp:
            result = cdp.ls_local("./unittest/input")

        self.assertCountEqual(result, expected) # compare two lists having the same elements but in a different order

    def test_cdp_ls_local_2(self):
        """test CrosDataParser.ls_local with name="*keyval*"
        """
        expected = ["unittest\\input\\keyval_1", "unittest\\input\\keyval_2", "unittest\\input\\keyval_3", "unittest\\input\\keyval_4"]
        result = []

        with CrosDataParser() as cdp:
            result = cdp.ls_local("./unittest/input", "*keyval*")

        self.assertCountEqual(result, expected) # compare two lists having the same elements but in a different order
    
    def test_cdp_ls_local_3(self):
        """test CrosDataParser.ls_local with name="*keyval"
        """
        expected = []
        result = []

        with CrosDataParser() as cdp:
            result = cdp.ls_local("./unittest/input", "*keyval")

        self.assertCountEqual(result, expected) # compare two lists having the same elements but in a different order
    
    def test_cdp_ls_local_4(self):
        """test CrosDataParser.ls_local with name="keyval*"
        """
        expected = ["unittest\\input\\keyval_1", "unittest\\input\\keyval_2", "unittest\\input\\keyval_3", "unittest\\input\\keyval_4"]
        result = []

        with CrosDataParser() as cdp:
            result = cdp.ls_local("./unittest/input", "keyval*")

        self.assertCountEqual(result, expected) # compare two lists having the same elements but in a different order
    
    def test_cdp_ls_local_5(self):
        """test CrosDataParser.ls_local with name="keyval"
        """
        expected = []
        result = []

        with CrosDataParser() as cdp:
            result = cdp.ls_local("./unittest/input", "keyval")

        self.assertCountEqual(result, expected) # compare two lists having the same elements but in a different order



    # def test_enter_s0i3(self):
    #     with CrosScenarios(self.test_system_ip_address, self.test_system_username, self.ssh_private_key_file) as cs:
    #         try:
    #             cs.enter_s0i3()
    #         except:
    #             self.fail("exception is raised!")


    # def test_launch_power_loadtest(self):
    #     with CrosScenarios(self.test_system_ip_address, self.test_system_username, self.ssh_private_key_file) as cs:
    #         try:
    #             cs.launch_power_loadtest()
    #         except:
    #             self.fail("exception is raised!")


if __name__ == '__main__':
    unittest.main(verbosity=2)