# ------------------------------------------------------
#
#   TestStrParser.py
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
from Lexly.Parser import StrParser

#Main
class StrParserTest(unittest.TestCase):
    
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
        StrParserTest.logger.debug('Test parsing tokens.')
        
        # Test data
        test_data = {
                     'msg_1': 'Important number => ',
                     'msg_2': 7,
                     }
        test_msg = test_data['msg_1'] + StrParser.DEFAULT_SEPARATOR + str(test_data['msg_2'])
        tokens = self.createTokens(test_data)
        str_parser = self.createParser()
                
        # Run test
        str_parser.start(tokens)
            
        # Show test output
        StrParserTest.logger.debug('Found %d parsing errors.' % len(str_parser.errors))
        for i, error in enumerate(str_parser.errors):
            StrParserTest.logger.debug('Found error %d:\n%s.' % (i, error.to_pretty_json()))
          
        StrParserTest.logger.debug('The final parser output: "%s".' % str(str_parser.data))
            
        # Verify results
        assert str_parser.data == test_msg, 'Could not parse msg tokens.'
            
        StrParserTest.logger.debug('Test succeeded!')
        
    def createParser(self): 
        # Datetime parser
        str_parser = StrParser('msg', [], ['msg_1', 'msg_2'], 'Str Parser')
        
        if self.debug_details:
            StrParserTest.logger.debug('Created parser:\n%s' % (str_parser.to_pretty_json()))
             
        return str_parser
         
    def createTokens(self, test_data):
        # Data structure
        tokens = []
        
        # Msg 1 token
        msg_token_1 = Token('msg_1', Token.ALWAYS_DATA, True, test_data['msg_1'])
        tokens.append(msg_token_1)
        
        # Msg 2 token
        msg_token_2 = Token('msg_2', Token.ALWAYS_DATA, True, test_data['msg_2'])
        tokens.append(msg_token_2)
        
        return tokens
        

        

    
    
    
    
    
    
    
  
        
 
        
        
        
        
        
        
     