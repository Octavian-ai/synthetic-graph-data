from os import environ

INTEGRATION = 'INTEGRATION'
UNIT = 'UNIT'


MODE = environ.get('TEST_MODE', UNIT)