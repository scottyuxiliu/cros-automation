import unittest
from cros_scenarios import CrosScenarios

class CrosScenariosCase(unittest.TestCase):
    def setUp(self):
        """The setUp() method is a special method that the unit testing framework executes before each test respectively.

        By changing the application configuration to sqlite://, I get SQLAlchemy to use an in-memory SQLite database during the tests. This prevents the unit tests from using the regular database that I use for development.
        """

        self.test_system_ip_address = "10.6.145.180"
        self.test_system_username = "root"
        self.ssh_private_key_file = "C:/Users/scottyuxiliu/Downloads/cezanne_majolica_id_rsa"


    def tearDown(self):
        """The tearDown() method is a special method that the unit testing framework executes after each test respectively.
        """

    def test_init_ssh_connection(self):
        cs = CrosScenarios()
        cs.init_ssh_connection(self.test_system_ip_address, self.test_system_username, self.ssh_private_key_file)
        self.assertRaises(ValueError)


if __name__ == '__main__':
    unittest.main(verbosity=2)