import logging, unittest
from cros_scenarios import CrosScenarios



class CrosScenariosCase(unittest.TestCase):
    def setUp(self):
        """The setUp() method is a special method that the unit testing framework executes before each test respectively.

        By changing the application configuration to sqlite://, I get SQLAlchemy to use an in-memory SQLite database during the tests. This prevents the unit tests from using the regular database that I use for development.
        """

        self.logger = logging.getLogger('cros_automation')
        self.logger.setLevel(logging.DEBUG)

        self.fh = logging.FileHandler('cros_automation.log', mode='w') # overwrite existing log file
        self.fh.setLevel(logging.DEBUG)

        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.INFO)

        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s') # output method name too
        self.fh.setFormatter(self.formatter)
        self.ch.setFormatter(self.formatter)

        self.logger.addHandler(self.fh)
        self.logger.addHandler(self.ch)

        self.test_system_ip_address = "10.6.145.180"
        self.test_system_username = "root"
        self.ssh_private_key_file = "C:/Users/scottyuxiliu/Downloads/cezanne_majolica_id_rsa"


    def tearDown(self):
        """The tearDown() method is a special method that the unit testing framework executes after each test respectively.
        """


    def test_test_connection(self):
        with CrosScenarios(self.test_system_ip_address, self.test_system_username, self.ssh_private_key_file) as cs:
            self.assertEqual(cs.test_connection(), True)


    # def test_enter_s0i3(self):
    #     with CrosScenarios(self.test_system_ip_address, self.test_system_username, self.ssh_private_key_file) as cs:
    #         try:
    #             cs.enter_s0i3()
    #         except:
    #             self.fail("exception is raised!")


    def test_launch_power_loadtest(self):
        with CrosScenarios(self.test_system_ip_address, self.test_system_username, self.ssh_private_key_file) as cs:
            try:
                cs.launch_power_loadtest()
            except:
                self.fail("exception is raised!")


if __name__ == '__main__':
    unittest.main(verbosity=2)