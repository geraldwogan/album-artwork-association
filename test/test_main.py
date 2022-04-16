import unittest
import main
# Add tests for main.py
# - get_secrets()
# - get_auth_client()

class TestMain(unittest.TestCase):

    def test_get_secrets(self):

            secrets = main.get_secrets()
            self.assertIsNotNone(secrets)
            length = len(secrets)
            assertEquals(secrets, 5)

            

if __name__ == '__main__':

        unittest.main()

