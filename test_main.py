from main import *

def test_get_secrets(self):
    secrets = get_secrets()
    assert len(secrets) == 5
