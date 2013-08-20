# ------------------------------------------------------
#
#   TestLexer.py
#   By: Fred Stakem
#   Created: 7.22.13
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

from Lexly.Lexer import LexerState
from Lexly.Lexer import LexerStateTransition
from Lexly.Lexer import Lexer


#Main
class LexerTest(unittest.TestCase):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
    
    @classmethod
    def setUpClass(cls):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
    
    def setUp(self):
        self.tmp_debug_lexer = globals.debug_lexer
        globals.debug_lexer = True
        
    def tearDown(self):
        globals.debug_lexer = self.tmp_debug_lexer
    
    @log_test(logger, globals.log_separator)
    def testStart(self):
        LexerTest.logger.debug('Test run the lexer.')
        
        # Test data
        lexers, tokens, states = self.createLexer()
        msg_lexer = lexers[0]
        
        # Run test
        msg_lexer.start(tokens[0])
            
        # Verify results
        self.findTokens(msg_lexer, tokens[1:])
        self.findErrors(msg_lexer)
            
        LexerTest.logger.debug('Test succeeded!')
        
    @log_test(logger, globals.log_separator)
    def testFindAllTokens(self):
        LexerTest.logger.debug('Test finding all the tokens.')
        
        # Test data
        lexers, tokens, states = self.createLexer()
        msg_lexer = lexers[0]
        
        # Run test
        msg_lexer.findAllTokens()
         
        # Verify results
        self.findTokens(msg_lexer, tokens[1:])
        self.findErrors(msg_lexer)
        
        LexerTest.logger.debug('Test succeeded!')
            
    @log_test(logger, globals.log_separator)
    def testHandleEndOfStream(self):
        LexerTest.logger.debug('Test handling the end of the stream.')
        
        # Test data
        lexers, tokens, states = self.createLexer()
        msg_lexer = lexers[0]
        
        # Run test
        while True:
            current_element = msg_lexer.stream.getNextElement()
            LexerTest.logger.debug('Current element: "%s"' % (current_element))
            
            if current_element == Element.EOS:
                msg_lexer.handleEndOfStream()
                break
            else:
                msg_lexer.handleNewData()
            
        assert len(msg_lexer.sub_tokens) > 0, 'No tokens found in list.'
        last_token = msg_lexer.sub_tokens[-1]
            
        # Show test output
        LexerTest.logger.debug('Last token added to lexer:\n%s' % (last_token.to_pretty_json()))
        
        # Verify results
        self.findErrors(msg_lexer)
        
        LexerTest.logger.debug('Test succeeded!')
        
    @log_test(logger, globals.log_separator)
    def testHandleNewData(self):
        LexerTest.logger.debug('Test handling of new data.')
        
        # Test data
        lexers, tokens, states = self.createLexer()
        msg_lexer = lexers[0]
        
        # Run test
        while msg_lexer.current_state != states[2]:
            current_element = msg_lexer.stream.getNextElement()
            LexerTest.logger.debug('Current element: "%s"' % (current_element))
            msg_lexer.handleNewData()
            
        assert len(msg_lexer.sub_tokens) > 0, 'No tokens found in list.'
        last_token = msg_lexer.sub_tokens[-1]
            
        # Show test output
        LexerTest.logger.debug('Last token added to lexer:\n%s' % (last_token.to_pretty_json()))
        
        # Verify results
        self.findErrors(msg_lexer)
        
        LexerTest.logger.debug('Test succeeded!')
            
    @log_test(logger, globals.log_separator)
    def testAppendToken(self):
        LexerTest.logger.debug('Test appending a token.')
        
        # Test data
        token = Token('str', Token.ALWAYS_DATA, True, 'Main Token')
        sub_token = Token('str', Token.ALWAYS_DATA, True, 'Sub Token')
        lexer = Lexer(None, 'msg', [], 'Unit Test Lexer')
        lexer.token = token
        
        # Show test data
        LexerTest.logger.debug('Created main token:\n%s' % (token.to_pretty_json()))
        LexerTest.logger.debug('Created sub token:\n%s' % (sub_token.to_pretty_json()))
        LexerTest.logger.debug('Created lexer:\n%s' % (lexer.to_pretty_json()))
        
        # Run test
        lexer.appendToken(sub_token)
        assert len(lexer.sub_tokens) > 0, 'No tokens found in list.'
        added_token = lexer.sub_tokens[-1]
        
        # Show test output
        LexerTest.logger.debug('Token added to lexer:\n%s' % (added_token.to_pretty_json()))
        
        # Verify results
        self.findErrors(lexer)
        
        LexerTest.logger.debug('Test succeeded!')
    
    @log_test(logger, globals.log_separator)    
    def testGetAllErrors(self):
        LexerTest.logger.debug('Test finding all the tokens.')
        
        # Test data
        lexers, tokens, states = self.createLexer()
        
        msg_lexer = lexers[0]
        month_lexer = lexers[1]
        
        msg_error = ParsingError('Msg Error', None)
        month_error = ParsingError('Month Error', None)
        
        msg_lexer.errors.append(msg_error)
        month_lexer.errors.append(month_error)
        
        # Run test
        errors = msg_lexer.getAllErrors()
        
        # Show test output
        LexerTest.logger.debug('Found %d errors.' % (len(errors)))
        for i, error in enumerate(errors):
            LexerTest.logger.debug('Found error %d:\n%s' % (i, error.to_pretty_json()))
        
        # Verify results
        assert len(errors) == 2, 'Error finding all errors.'
        assert errors[0] == msg_error, 'Error finding all errors.'
        assert errors[1] == month_error, 'Error finding all errors.'
                  
        LexerTest.logger.debug('Test succeeded!')
    
    @log_test(logger, globals.log_separator)
    def testGetAllTokens(self):
        LexerTest.logger.debug('Test finding all the tokens.')
        
        # Test data
        lexers, tokens, states = self.createLexer()
        msg_lexer = lexers[0]
        msg_token = tokens[0]
        
        # Run test
        msg_lexer.start(msg_token)
        all_tokens = msg_lexer.getAllTokens()
        
        # Show test output
        LexerTest.logger.debug('Found %d tokens.' % (len(all_tokens)))
        for i, token in enumerate(all_tokens):
            LexerTest.logger.debug('Found token %d:\n%s' % (i, token.to_pretty_json()))
        
        # Verify results
        assert len(all_tokens) == 2, 'Error finding all errors.'
        assert all_tokens[0] == tokens[1], 'Error finding all errors.'
        assert all_tokens[1] == tokens[2], 'Error finding all errors.'
                  
        LexerTest.logger.debug('Test succeeded!')
        
    def createLexer(self):
        # Test data
        source = 'Jul 11 09:51:54'
        
        # End state
        end_token = Token('end', Token.NEVER_DATA, True, 'End Token')
        end_state = LexerState([], end_token, True, 'End State')
        
        # Time lexer
        end_transition = LexerStateTransition('EOS', 0, 0, True, end_state, 'Time to End Transition')
        time_token = Token('time', Token.ALWAYS_DATA, True, 'Time Token')
        time_state = LexerState([end_transition], time_token, False, 'Time State')
        time_lexer = Lexer(time_state, 'time', [], 'Time Lexer')
        
        # Month lexer
        time_transition = LexerStateTransition('\s+\d{2}\s+', 0, 4, True, time_state, 'Month to Time Transition')
        month_token = Token('month', Token.ALWAYS_DATA, True, 'Month Token')
        month_state = LexerState([time_transition], month_token, False, 'Month State')
        month_lexer = Lexer(month_state, 'month', [], 'Month Lexer')
        
        # Msg state
        month_transition = LexerStateTransition('.', 0, -1, True, month_state, 'Msg to Month Transition')
        msg_token = Token('msg', Token.NEVER_DATA, False, source)
        msg_state = LexerState([month_transition], msg_token, False, 'Msg State')
        
        # Msg lexer
        msg_lexer = Lexer(msg_state, 'msg', [time_lexer, month_lexer], 'Msg Lexer')
        msg_lexer.changeState(msg_state)
        msg_lexer.token = msg_token
        msg_lexer.stream = msg_token.getStream()
        
        # Show test data
        LexerTest.logger.debug('Created state:\n%s' % (msg_state.to_pretty_json()))
        LexerTest.logger.debug('Created state:\n%s' % (month_state.to_pretty_json()))
        LexerTest.logger.debug('Created state:\n%s' % (time_state.to_pretty_json()))
        LexerTest.logger.debug('Created state:\n%s' % (end_state.to_pretty_json()))

        tokens = [msg_token, month_token, time_token]        
        states = [msg_state, month_state, time_state, end_state]
        lexers = [msg_lexer, month_lexer, time_lexer]
        
        return [ lexers, tokens, states ]
    
    def findTokens(self, lexer, expected_tokens):
        found_tokens = lexer.getAllTokens()
        LexerTest.logger.debug('Found %d tokens.' % (len(found_tokens)))
        
        for expected_token in expected_tokens:
            found = False
            for found_token in found_tokens:
                if expected_token == found_token:
                    found = True
                    LexerTest.logger.debug('Found token:\n%s' % (expected_token.to_pretty_json()))
                    break
                
            if not found:
                LexerTest.logger.error('Did not find token:\n%s' % (expected_token.to_pretty_json()))
                assert False, 'Error during lexing.'
    
    def findErrors(self, lexer):
        errors = lexer.getAllErrors()
        LexerTest.logger.debug('Found %d errors.' % (len(errors)))
        if len(errors) > 0:
            for i, error in enumerate(errors):
                LexerTest.logger.error('Error %d:\n%s' % (i, error.to_pretty_json()))
            assert False, 'Error during lexing.'
        
    
    
    
    
    
    
    
    
  
        
 
        
        
        
        
        
        
     