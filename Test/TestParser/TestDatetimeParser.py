# ------------------------------------------------------
#
#   TestDatetimeParser.py
#   By: Fred Stakem
#   Created: 8.5.13
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
from Lexly.Parser import DatetimeParser

#Main
class DatetimeParserTest(unittest.TestCase):
    
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
        DatetimeParserTest.logger.debug('Test parsing tokens.')
        
        # Test data
        test_data = {
                     'year': '2013',
                     'month': 'Jul',
                     'day': '11',
                     'hour': '9',
                     'minute': '51',
                     'second': '46',
                     }
        test_datetime = datetime(year=int(test_data['year']),
                                 month=7,
                                 day=int(test_data['day']),
                                 hour=int(test_data['hour']),
                                 minute=int(test_data['minute']),
                                 second=int(test_data['second']))
        tokens = self.createTokens(test_data)
        datetime_parser = self.createParser()
                
        # Run test
        datetime_parser.start(tokens)
            
        # Show test output
        DatetimeParserTest.logger.debug('Found %d parsing errors.' % len(datetime_parser.errors))
        for i, error in enumerate(datetime_parser.errors):
            DatetimeParserTest.logger.debug('Found error %d:\n%s.' % (i, error.to_pretty_json()))
          
        DatetimeParserTest.logger.debug('The final parser output: %s' % str(datetime_parser.data))
            
        # Verify results
        assert datetime_parser.data == test_datetime, 'Could not parse datetime tokens.'
            
        DatetimeParserTest.logger.debug('Test succeeded!')
        
    def createParser(self): 
        # Datetime parser
        datetime_parser = DatetimeParser('timestamp', [], ['month', 'day', 'hour', 'minute', 'second'], 'Datetime Parser')
        
        if self.debug_details:
            DatetimeParserTest.logger.debug('Created parser:\n%s' % (datetime_parser.to_pretty_json()))
             
        return datetime_parser
         
    def createTokens(self, test_data):
        # Data structure
        tokens = []
        
        # Month token
        month_token = Token('month', Token.ALWAYS_DATA, True, test_data['month'])
        tokens.append(month_token)
        
        # Day token
        day_token = Token('day', Token.ALWAYS_DATA, True, test_data['day'])
        tokens.append(day_token)
        
        # Hour token
        hour_token = Token('hour', Token.ALWAYS_DATA, True, test_data['hour'])
        tokens.append(hour_token)
        
        # Minute token
        minute_token = Token('minute', Token.ALWAYS_DATA, True, test_data['minute'])
        tokens.append(minute_token)
        
        # Second token
        second_token = Token('second', Token.ALWAYS_DATA, True, test_data['second'])
        tokens.append(second_token)
        
        return tokens
        

        

    
    
    
    
    
    
    
  
        
 
        
        
        
        
        
        
     