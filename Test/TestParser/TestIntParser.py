# ------------------------------------------------------
#
#   TestIntParser.py
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
from Lexly.Parser import IntParser

#Main
class IntParserTest(unittest.TestCase):
    
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
        IntParserTest.logger.debug('Test parsing tokens.')
        
        # Test data
        test_data = {
                     'int': '235'
                    }
        test_msg = 235
        tokens = self.createTokens(test_data)
        int_parser = self.createParser()
                
        # Run test
        int_parser.start(tokens)
            
        # Show test output
        IntParserTest.logger.debug('Found %d parsing errors.' % len(int_parser.errors))
        for i, error in enumerate(int_parser.errors):
            IntParserTest.logger.debug('Found error %d:\n%s.' % (i, error.to_pretty_json()))
          
        IntParserTest.logger.debug('The final parser output: "%s".' % str(int_parser.data))
            
        # Verify results
        assert int_parser.data == test_msg, 'Could not parse int token.'
            
        IntParserTest.logger.debug('Test succeeded!')
        
    def createParser(self): 
        # Datetime parser
        int_parser = IntParser('int', [], ['int'], 'Int Parser')
        
        if self.debug_details:
            IntParserTest.logger.debug('Created parser:\n%s' % (int_parser.to_pretty_json()))
             
        return int_parser
         
    def createTokens(self, test_data):
        # Data structure
        tokens = []
        
        # Msg 1 token
        int_token = Token('int', Token.ALWAYS_DATA, True, test_data['int'])
        tokens.append(int_token)
         
        return tokens
        

        

    
    
    
    
    
    
    
  
        
 
        
        
        
        
        
        
     