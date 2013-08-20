# ------------------------------------------------------
#
#   TestEnumParser.py
#   By: Fred Stakem
#   Created: 8.6.13
#
# ------------------------------------------------------


# Libs
import unittest
from datetime import datetime

# User defined
from Globals import *
from Utilities import *

from Lexly import Element
from Lexly import Stream
from Lexly import Token
from Lexly import ParsingError

from Corely import Field

from Lexly.Parser import Parser
from Lexly.Parser import EnumParser

#Main
class EnumParserTest(unittest.TestCase):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
    
    @classmethod
    def setUpClass(cls):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
    
    def setUp(self):
        self.tmp_debug_parser = globals.debug_parser
        globals.debug_parser = True
        self.debug_details = False
        
    def tearDown(self):
        globals.debug_parser = self.tmp_debug_parser
          
    @log_test(logger, globals.log_separator)
    def testStart(self):
        EnumParserTest.logger.debug('Test parsing tokens.')
        
        # Test data
        test_data = 'idle'
        tokens = self.createTokens(test_data)
        state_parser = self.createParser()
                
        # Run test
        state_parser.start(tokens)
            
        # Show test output
        EnumParserTest.logger.debug('Found %d parsing errors.' % len(state_parser.errors))
        for i, error in enumerate(state_parser.errors):
            EnumParserTest.logger.debug('Found error %d:\n%s.' % (i, error.to_pretty_json()))
          
        EnumParserTest.logger.debug('The final parser output: "%s".' % str(state_parser.data))
            
        # Verify results
        assert state_parser.data == test_data, 'Could not parse enum token.'
            
        EnumParserTest.logger.debug('Test succeeded!')
        
    def createParser(self): 
        # Datetime parser
        state_parser = EnumParser('state', [], ['state'], 'State Parser', ['on', 'off', 'idle'])
        
        if self.debug_details:
            EnumParserTest.logger.debug('Created parser:\n%s' % (state_parser.to_pretty_json()))
             
        return state_parser
         
    def createTokens(self, test_data):
        # Data structure
        tokens = []
        
        # Msg 1 token
        state_token = Token('state', Token.ALWAYS_DATA, True, test_data)
        tokens.append(state_token)
         
        return tokens
        

        

    
    
    
    
    
    
    
  
        
 
        
        
        
        
        
        
     