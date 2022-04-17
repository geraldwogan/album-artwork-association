import unittest
import main

class TestMain(unittest.TestCase):

    def test_get_secrets(self):
        secrets = main.get_secrets()
        self.assertIsNotNone(secrets)
        length = len(secrets)
        assertEquals(secrets, 5)

    def test_setup_auth_client(self, secrets):
        client = setup_auth_client(secrets)
        self.assertIsNotNone(client)

if __name__ == '__main__':
        unittest.main()
