# ------------------------------------------------------
#
#   TestToken.py
#   By: Fred Stakem
#   Created: 7.24.13
#
# ------------------------------------------------------


# Libs
import unittest

# User defined
from Globals import *
from Utilities import *
from Lexly import Token
from Lexly import ParsingError
from Lexly import Stream

#Main
class TokenTest(unittest.TestCase):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
    
    @classmethod
    def setUpClass(cls):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    @log_test(logger, globals.log_separator)
    def testGetStream(self):
        TokenTest.logger.debug('Test run creation of a stream from the token.')
        
        # Test data
        data = 'Jul 11 09:51:54'
        data_type = 'str'
        token = Token(data_type, Token.ALWAYS_DATA, False, data)
        
        # Show test data
        TokenTest.logger.debug('Created data: "%s"' % (data))
        TokenTest.logger.debug('Created token:\n%s' % (token.to_pretty_json()))
        
        # Run test
        stream = token.getStream()
        
        # Show test output
        TokenTest.logger.debug('Returned stream:\n%s' % (stream.to_pretty_json()))
        
        # Verify results
        assert stream.source == data, 'The stream data was set incorrectly.'
        assert stream.name == data_type, 'The stream data type was set incorrectly.'
        
        TokenTest.logger.debug('Test succeeded!')
        
