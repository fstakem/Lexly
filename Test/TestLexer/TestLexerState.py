# ------------------------------------------------------
#
#   TestLexerState.py
#   By: Fred Stakem
#   Created: 7.22.13
#
# ------------------------------------------------------


# Libs
import unittest

# User defined
from Globals import *
from Utilities import *

from Lexly import Stream
from Lexly import Token

from Lexly.Lexer import LexerState
from Lexly.Lexer import LexerStateTransition

#Main
class LexerStateTest(unittest.TestCase):
    
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
    def testNextState(self):
        LexerStateTest.logger.debug('Testing the matching of a sequence.')
        
        # Test data
        source = 'Jul 11 09:51:54'
        stream = Stream(source, 'Unit Test Stream') 
        token = Token('str', Token.ALWAYS_DATA, True, 'Token data')
        state_b = LexerState([], token, True, 'State B')
        pattern = '\s+\d{2}\s+'
        start_offet = 0
        end_offset = 4
        transition = LexerStateTransition(pattern, start_offet, end_offset, True, state_b, 'A to B Transition')
        state_a = LexerState([transition], token, False, 'State A')
        
        # Show test data
        LexerStateTest.logger.debug('Created stream:\n%s' % (stream.to_pretty_json()))
        LexerStateTest.logger.debug('Created state A:\n%s' % (state_a.to_pretty_json()))
        LexerStateTest.logger.debug('Created state B:\n%s' % (state_b.to_pretty_json()))
        
        # Run test
        next_state = state_a
        new_token = None
        while next_state == state_a:
            current_element = stream.getNextElement()
            next_state, new_token = state_a.nextState(stream)
            
            # Show test output
            LexerStateTest.logger.debug('Fetching element: %s' % (current_element))
            
        # Show test output
        LexerStateTest.logger.debug('Token found:\n%s' % (new_token.to_pretty_json()))
        LexerStateTest.logger.debug('Final stream state:\n%s' % (stream.to_pretty_json()))
        LexerStateTest.logger.debug('Final lexer state:\n%s' % (next_state.to_pretty_json()))
        
        # Verify results
        token.data = source[:3]
        assert new_token == token, 'The token found is incorrect.'
            
        LexerStateTest.logger.debug('Test succeeded!')
        
 
        
        
        
        
        
        
     