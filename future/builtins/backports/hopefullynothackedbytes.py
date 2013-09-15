from future import utils
if not utils.PY3:
    assert 'fromhex' not in dir(b'blah')
