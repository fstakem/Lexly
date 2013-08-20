# ------------------------------------------------------
#
#   TestLexerStateTransition.py
#   By: Fred Stakem
#   Created: 7.14.13
#
# ------------------------------------------------------


# Libs
import unittest

# User defined
from Globals import *
from Utilities import *

from Lexly import Element
from Lexly import Stream

from Lexly.Lexer import LexerStateTransition

#Main
class LexerStateTransitionTest(unittest.TestCase):
    
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
    def testFindMatch(self):
        LexerStateTransitionTest.logger.debug('Testing the matching of a sequence.')
        
        # Test data
        source = 'Jul 11 09:51:54'
        patterns = [ '\d{2}:\d{2}:\d{2}', 'EOS']
        offsets = ( (0, 0), (0, 0) )
        test_slices = ( ( (0, 6), (7, len(source)) ), ( (0, len(source)), (len(source), len(source)) ) )
        
        # Run test
        for i, pattern in enumerate(patterns):
            LexerStateTransitionTest.logger.debug('Testing pattern %d.' % (i))
            data, new_buffer = self.findMatchPattern(source, pattern, offsets[i][0], offsets[i][0])
        
            # Verify results
            slices = test_slices[i]
            data_slices = slices[0]
            buffer_slices = slices[1]
            LexerStateTransitionTest.logger.debug('The token data should equal: "%s"' % (source[data_slices[0]:data_slices[1]]))
            assert data == source[data_slices[0]:data_slices[1]], 'The data from the accepted buffer is incorrect.'
            
            LexerStateTransitionTest.logger.debug('The buffer data should equal: "%s"' % (source[buffer_slices[0]:buffer_slices[1]]))
            assert ''.join(new_buffer) == source[buffer_slices[0]:buffer_slices[1]], 'The new stream buffer is incorrect.'
        
        LexerStateTransitionTest.logger.debug('Test succeeded!')
        
    def findMatchPattern(self, source, pattern, start, end):
        # Test data
        stream = Stream(source, 'Unit Test Stream')
        stream.element_buffer = list(source)
        if pattern == Element.EOS:
            stream.current_position = len(stream.element_buffer)
        transition = LexerStateTransition(pattern, start, end, True, None, 'Unit Test State Transition')
        
        # Show test data
        LexerStateTransitionTest.logger.debug('Created stream:\n%s' % (stream.to_pretty_json()))
        LexerStateTransitionTest.logger.debug('Created state transition:\n%s' % (transition.to_pretty_json()))
        
        # Run test
        data = transition.findMatch(stream)
        new_buffer = stream.element_buffer
        
        # Show test output
        LexerStateTransitionTest.logger.debug('Token data found: "%s"' % (data))
        LexerStateTransitionTest.logger.debug('New buffer: %s' % (str(new_buffer)))
        LexerStateTransitionTest.logger.debug('Final stream state:\n%s' % (stream.to_pretty_json()))
        
        return (data, new_buffer)
        
    @log_test(logger, globals.log_separator)
    def testGetTokenData(self):
        LexerStateTransitionTest.logger.debug('Testing the matching of a sequence.')
        
        # Test data
        location = (3, 4)
        start_offet = 0
        end_offset = 4
        source = 'Jul 11 09:51:54'
        stream = Stream(source, 'Unit Test Stream')
        stream.element_buffer = list(source)
        transition = LexerStateTransition('', start_offet, end_offset, True, None, 'Unit Test State Transition')
        
        # Show test data
        LexerStateTransitionTest.logger.debug('Created stream:\n%s' % (stream.to_pretty_json()))
        LexerStateTransitionTest.logger.debug('Created state transition:\n%s' % (transition.to_pretty_json()))
        
        # Run test
        data = transition.getTokenData(stream, location)
        
        # Show test output
        LexerStateTransitionTest.logger.debug('Token data found: "%s"' % (data))
        LexerStateTransitionTest.logger.debug('Final stream state:\n%s' % (stream.to_pretty_json()))
        
        # Verify results
        assert data == source[:location[0]], 'The data from the accepted buffer is incorrect.'
        
        LexerStateTransitionTest.logger.debug('Test succeeded!')
    
    @log_test(logger, globals.log_separator)
    def testSplitBuffer(self):
        LexerStateTransitionTest.logger.debug('Testing the matching of a sequence.')
        
        # Test data
        test_data = 'Jul 11 09:51:54'
        buffer = list(test_data)
        end = 3
        start = 7
        transition = LexerStateTransition('', 0, 0, True, None, 'Unit Test State Transition')
        
        # Show test data
        LexerStateTransitionTest.logger.debug('Input buffer: %s' % (str(buffer)))
        
        # Run test
        accepted_buffer, remaining_buffer = transition.splitBuffer(buffer, end, start)
        
        # Show test output
        LexerStateTransitionTest.logger.debug('Data from accepted buffer: %s' % (str(accepted_buffer)))
        LexerStateTransitionTest.logger.debug('Data from remaining buffer: %s' % (str(remaining_buffer)))
        
        # Verify results
        assert accepted_buffer == list(test_data[:end]), 'The data from the accepted buffer is incorrect.'
        assert remaining_buffer == list(test_data[start:]), 'The data from the remaining buffer is incorrect.'
        
        LexerStateTransitionTest.logger.debug('Test succeeded!')
    
    @log_test(logger, globals.log_separator)
    def testGetDataFromBuffer(self):
        LexerStateTransitionTest.logger.debug('Testing the matching of a sequence.')
        
        # Test data
        test_data = 'Jul 11 09:51:54'
        
        # Test with strip
        buffer_str = '  ' + test_data + '  '
        result_data = self.subTestGetDataFromBuffer(list(buffer_str), True)
        assert result_data == test_data, 'The data from the buffer is incorrect.'
        
        # Test without strip
        buffer_str = test_data
        result_data = self.subTestGetDataFromBuffer(list(buffer_str), False)
        assert result_data == test_data, 'The data from the buffer is incorrect.'
        
        LexerStateTransitionTest.logger.debug('Test succeeded!')
        
    def subTestGetDataFromBuffer(self, buffer, stripped):
        # Test data
        transition = LexerStateTransition('', 0, 0, stripped, None, 'Unit Test State Transition')
        
        # Show test data
        LexerStateTransitionTest.logger.debug('Input buffer: %s' % (str(buffer)))
        
        # Run test
        data = transition.getDataFromBuffer(buffer)
        
        # Show test output
        LexerStateTransitionTest.logger.debug('Data from buffer: "%s"' % (str(data)))
        
        return data
    
   
        
        
        