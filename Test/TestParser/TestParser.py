# ------------------------------------------------------
#
#   TestParser.py
#   By: Fred Stakem
#   Created: 8.1.13
#
# ------------------------------------------------------


# Libs
import unittest

# User defined
from Globals import *
from Utilities import *

from Lexly import Element
from Lexly import Stream
from Lexly import Token
from Lexly import ParsingError

from Corely import Field

from Lexly.Parser import Parser

#Main
class ParserTest(unittest.TestCase):
    
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
          
    #===========================================================================
    # @log_test(logger, globals.log_separator)
    # def testGetUnusedTokens(self):
    #    ParserTest.logger.debug('Test getting all the unused tokens for the field.')
    #    
    #    # Test data
    #    parsers, fields = self.createParsers()
    #    tokens = self.createTokens()
    #    event_parser = parsers[0]
    #    datetime_parser = parsers[1]
    #    
    #    # Run test
    #    tokens = datetime_parser.createTokenDict(tokens)
    #    unused_tokens = datetime_parser.getUnusedTokens(tokens)
    #        
    #    # Show test output
    #    ParserTest.logger.debug('Found %d unused tokens.' % len(unused_tokens))
    #    i = 0
    #    for key, token in unused_tokens.iteritems():
    #        ParserTest.logger.debug('Found token %d:\n%s.' % (i, token.to_pretty_json()))
    #        i += 1
    #        
    #    # Verify results
    #    assert len(unused_tokens) == 4, 'Found incorrect number of unused tokens.'
    #    assert 'component' in unused_tokens, 'Could not find component token.'
    #    assert 'component_id' in unused_tokens, 'Could not find component id token.'
    #    assert 'level' in unused_tokens, 'Could not find level token.'
    #    assert 'sub_msg' in unused_tokens, 'Could not find sub msg token.'
    #        
    #    ParserTest.logger.debug('Test succeeded!')
    #===========================================================================
                
    @log_test(logger, globals.log_separator)
    def testGetAllErrors(self):
        ParserTest.logger.debug('Test getting all the errors from the parser.')
        
        # Test data
        parsers = self.createParsers()
        event_parser = parsers[0]
        
        # Error data
        level_parser = parsers[6]
        sub_msg_parser = parsers[7]
        
        level_error = ParsingError('Level Error')
        level_parser.errors.append(level_error)
        sub_msg_error = ParsingError('Sub Msg Error')
        sub_msg_parser.errors.append(sub_msg_error)
        
        # Run test
        errors = event_parser.getAllErrors()
        
        # Show test output
        ParserTest.logger.debug('Found %d errors.' % len(errors))
        for i, error in enumerate(errors):
            ParserTest.logger.debug('Errors %d:\n%s' % (i, error.to_pretty_json()))
            
        # Verify results
        assert errors[0] == level_error, 'Could not find level error.'
        assert errors[1] == sub_msg_error, 'Could not find sub msg error.'
            
        ParserTest.logger.debug('Test succeeded!')
        
    def createParsers(self):
        # Sub msg parser
        #sub_msg_field = Field('sub_msg', [], ['sub_msg'], 'Sub Msg Field')
        sub_msg_parser = Parser('sub_msg', [], ['sub_msg'], 'Sub Msg Parser')
        
        # Level parser
        #level_field = Field('level', [], ['level'], 'Level Field')
        level_parser = Parser('level', [], ['level'], 'Level Parser')
        
        # Msg parser
        #msg_field = Field('msg', [sub_msg_field, level_field], [], 'Msg Field')
        msg_parser = Parser('msg', [level_parser, sub_msg_parser], [], 'Msg Parser')
        
        # Component id parser
        #component_id_field = Field('component_id', [], ['component_id'], 'Component ID Field')
        component_id_parser = Parser('component_id', [], ['component_id'], 'Component ID Parser')
        
        # Component parser
        #component_field = Field('component', [], ['component'], 'Component Field')
        component_parser = Parser('component', [], ['component'], 'Component Parser')
        
        # Source parser
        #source_field = Field('source', [component_field, component_id_field], [], 'Source Field')
        source_parser = Parser('source', [component_parser, component_id_parser], [], 'Source Parser')
        
        # Datetime parser
        #timestamp_field = Field('timestamp', [], ['month', 'day', 'hour', 'minute', 'second'], 'Timestamp Field')
        datetime_parser = Parser('timestamp', [], ['month', 'day', 'hour', 'minute', 'second'], 'Datetime Parser')
        
        # Event parser
        #event_field = Field('event', [timestamp_field, source_field, msg_field], [], 'Event Field')
        event_parser = Parser('event', [datetime_parser, source_parser, msg_parser], [], 'Event Parser')
        
        if self.debug_details:
            ParserTest.logger.debug('Created parser:\n%s' % (event_parser.to_pretty_json()))
            
        parsers = (event_parser, datetime_parser, source_parser, component_parser, component_id_parser, 
                   msg_parser, level_parser, sub_msg_parser)
        #fields = (event_field, timestamp_field, source_field, component_field, component_id_field,
        #          component_id_field, msg_field, level_field, sub_msg_field)
        
        return parsers
         
    def createTokens(self):
        # Data structure
        tokens = []
        
        # Month token
        month_token = Token('month', Token.ALWAYS_DATA, True, 'Jul')
        tokens.append(month_token)
        
        # Day token
        day_token = Token('day', Token.ALWAYS_DATA, True, '11')
        tokens.append(day_token)
        
        # Hour token
        hour_token = Token('hour', Token.ALWAYS_DATA, True, '09')
        tokens.append(hour_token)
        
        # Minute token
        minute_token = Token('minute', Token.ALWAYS_DATA, True, '51')
        tokens.append(minute_token)
        
        # Second token
        second_token = Token('second', Token.ALWAYS_DATA, True, '69')
        tokens.append(second_token)
        
        # Component token
        component_token = Token('component', Token.SOMETIMES_DATA, True, 'ubuntu NetworkManager')
        tokens.append(component_token)
        
        # Component id token
        component_id_token = Token('component_id', Token.SOMETIMES_DATA, True, '887')
        tokens.append(component_id_token)
        
        # Level token
        level_token = Token('level', Token.SOMETIMES_DATA, True, 'info')
        tokens.append(level_token)
        
        # Msg token
        sub_msg_token = Token('sub_msg', Token.SOMETIMES_DATA, True, "monitoring kernel firmware directory '/lib/firmware'.")
        tokens.append(sub_msg_token)
        
        return tokens
        

        

    
    
    
    
    
    
    
  
        
 
        
        
        
        
        
        
     