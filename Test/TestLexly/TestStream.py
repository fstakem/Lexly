# ------------------------------------------------------
#
#   TestStream.py
#   By: Fred Stakem
#   Created: 6.19.13
#
# ------------------------------------------------------


# Libs
import unittest

# User defined
from Globals import *
from Utilities import *
from Lexly import Stream

#Main
class StreamTest(unittest.TestCase):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
    
    @classmethod
    def setUpClass(cls):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
    
    def setUp(self):
        # Test data
        self.source = 'Jul 11 09:51:54'
        
        # Show test data
        StreamTest.logger.debug('Created source: "%s"' % (self.source))
    
    def tearDown(self):
        pass
    
    @log_test(logger, globals.log_separator)
    def testAtEos(self):
        StreamTest.logger.debug('Test when the end of the stream is reached.')
        
        # Test data
        stream = Stream(self.source, 'Unit Test Stream')
        
        # Show test data
        StreamTest.logger.debug('Current stream state:\n%s' % (stream.to_pretty_json()))
        
        # Run test
        for i in range(len(self.source)):
            element = stream.getNextElement()
            
            # Show test output
            StreamTest.logger.debug('Fetching element %d.' % (i))
            StreamTest.logger.debug('Fetched element: "%s"' % (element))
            StreamTest.logger.debug('Current stream state:\n%s' % (stream.to_pretty_json()))
            StreamTest.logger.debug('Fetched element buffer: %s' % (str(stream.element_buffer)))
        
        # Show test output
        StreamTest.logger.debug('Current stream state:\n%s' % (stream.to_pretty_json()))
        
        # Verify results
        assert stream.atEos(), 'Stream buffer is not at the end.'
        
        StreamTest.logger.debug('Test succeeded!')
    
    @log_test(logger, globals.log_separator)
    def testAcceptElementRange(self):
        StreamTest.logger.debug('Test accepting data in a particular range from the buffer.')
        
        # Test data
        stream = Stream(self.source, 'Unit Test Stream')
        number_of_elements = 9
        start = 3
        end = 6
        
        # Show test data
        StreamTest.logger.debug('Current stream state:\n%s' % (stream.to_pretty_json()))
        
        # Run test
        for i in range(number_of_elements):
            element = stream.getNextElement()
            
            # Show test output
            StreamTest.logger.debug('Fetching element %d.' % (i))
            StreamTest.logger.debug('Fetched element: "%s"' % (element))
            StreamTest.logger.debug('Current stream state:\n%s' % (stream.to_pretty_json()))
            StreamTest.logger.debug('Fetched element buffer: %s' % (str(stream.element_buffer)))
            
        buffer = stream.acceptElementRange(start, end)
        
        # Show test output
        StreamTest.logger.debug('Accepting elements between %d and %d.' % (start, end))
        StreamTest.logger.debug('Accepted buffer: %s' % (str(buffer)))
        StreamTest.logger.debug('Buffer after accepting elements: %s' % (str(stream.element_buffer)))
        StreamTest.logger.debug('Current stream state:\n%s' % (stream.to_pretty_json()))
        
        # Verify results
        assert len(stream.element_buffer) == number_of_elements - end + start - 1, 'Stream buffer was not properly emptied.'
        assert stream.start_position == number_of_elements - 1, 'Stream start position is not correct.'
        assert stream.current_element == None, 'Stream current element is incorrect.'
        
        StreamTest.logger.debug('Test succeeded!')
    
    @log_test(logger, globals.log_separator)
    def testAcceptElements(self):
        StreamTest.logger.debug('Test accepting data from the buffer.')
        
        # Test data
        stream = Stream(self.source, 'Unit Test Stream')
        number_of_elements = 3
        
        # Show test data
        StreamTest.logger.debug('Current stream state:\n%s' % (stream.to_pretty_json()))
        
        # Run test
        for i in range(number_of_elements):
            element = stream.getNextElement()
            
            # Show test output
            StreamTest.logger.debug('Fetching element %d.' % (i))
            StreamTest.logger.debug('Fetched element: "%s"' % (element))
            StreamTest.logger.debug('Current stream state:\n%s' % (stream.to_pretty_json()))
            StreamTest.logger.debug('Fetched element buffer: %s' % (str(stream.element_buffer)))
        
        buffer = stream.acceptElements()
        
        # Show test output
        StreamTest.logger.debug('Accepted buffer: %s' % (str(buffer)))
        StreamTest.logger.debug('Buffer after accepting elements: %s' % (str(stream.element_buffer)))
        StreamTest.logger.debug('Current stream state:\n%s' % (stream.to_pretty_json()))
        
        # Verify results
        assert len(stream.element_buffer) == 0, 'Stream buffer was not properly emptied.'
        assert stream.start_position == number_of_elements - 1, 'Stream start position is not correct.'
        assert stream.current_element == None, 'Stream current element is incorrect.'
        assert ''.join(buffer) == self.source[:number_of_elements], 'Accepted buffer is incorrect.'
        
        StreamTest.logger.debug('Test succeeded!')
        
    @log_test(logger, globals.log_separator)
    def testFlushElementRange(self):
        StreamTest.logger.debug('Test flushing data in a particular range from the buffer.')
        
        # Test data
        stream = Stream(self.source, 'Unit Test Stream')
        number_of_elements = 9
        start = 3
        end = 6
        
        # Show test data
        StreamTest.logger.debug('Current stream state:\n%s' % (stream.to_pretty_json()))
        
        # Run test
        for i in range(number_of_elements):
            element = stream.getNextElement()
            
            # Show test output
            StreamTest.logger.debug('Fetching element %d.' % (i))
            StreamTest.logger.debug('Fetched element: "%s"' % (element))
            StreamTest.logger.debug('Current stream state:\n%s' % (stream.to_pretty_json()))
            StreamTest.logger.debug('Fetched element buffer: %s' % (str(stream.element_buffer)))
            
        stream.flushElementRange(start, end)
        
        # Show test output
        StreamTest.logger.debug('Flushing elements between %d and %d.' % (start, end))
        StreamTest.logger.debug('Buffer after flush: %s' % (str(stream.element_buffer)))
        StreamTest.logger.debug('Current stream state:\n%s' % (stream.to_pretty_json()))
        
        # Verify results
        assert len(stream.element_buffer) == number_of_elements - end + start - 1, 'Stream buffer was not properly emptied.'
        assert stream.start_position == number_of_elements - 1, 'Stream start position is not correct.'
        assert stream.current_element == None, 'Stream current element is incorrect.'
        
        StreamTest.logger.debug('Test succeeded!')
        
    @log_test(logger, globals.log_separator)
    def testFlushElements(self):
        StreamTest.logger.debug('Test flushing data from the buffer.')
        
        # Test data
        stream = Stream(self.source, 'Unit Test Stream')
        number_of_elements = 3
        
        # Show test data
        StreamTest.logger.debug('Current stream state:\n%s' % (stream.to_pretty_json()))
        
        # Run test
        for i in range(number_of_elements):
            element = stream.getNextElement()
            
            # Show test output
            StreamTest.logger.debug('Fetching element %d.' % (i))
            StreamTest.logger.debug('Fetched element: "%s"' % (element))
            StreamTest.logger.debug('Current stream state:\n%s' % (stream.to_pretty_json()))
            StreamTest.logger.debug('Fetched element buffer: %s' % (str(stream.element_buffer)))
            
        stream.flushElements()
        
        # Show test output
        StreamTest.logger.debug('Buffer after flush: %s' % (str(stream.element_buffer)))
        StreamTest.logger.debug('Current stream state:\n%s' % (stream.to_pretty_json()))
        
        # Verify results
        assert len(stream.element_buffer) == 0, 'Stream buffer was not properly emptied.'
        assert stream.start_position == number_of_elements - 1, 'Stream start position is not correct.'
        assert stream.current_element == None, 'Stream current element is incorrect.'
        
        StreamTest.logger.debug('Test succeeded!')
        
    @log_test(logger, globals.log_separator)
    def testGetNextElement(self):
        StreamTest.logger.debug('Test getting next element from the source.')
        
        # Test data
        stream = Stream(self.source, 'Unit Test Stream')
        number_of_elements = 3
        
        # Show test data
        StreamTest.logger.debug('Current stream state:\n%s' % (stream.to_pretty_json()))
        
        # Run test
        for i in range(number_of_elements):
            element = stream.getNextElement()
            buffer = ''.join(stream.element_buffer)
            
            # Show test output
            StreamTest.logger.debug('Fetching element %d.' % (i))
            StreamTest.logger.debug('Fetched element: "%s"' % (element))
            StreamTest.logger.debug('Current stream state:\n%s' % (stream.to_pretty_json()))
            StreamTest.logger.debug('Fetched element buffer: %s' % (str(stream.element_buffer)))
            
            # Verify results
            assert self.source[i] == element, 'Stream current element does not equal the source character.'
            assert stream.current_position == i, 'Stream current position is incorrect.'
            assert self.source[:i+1] == buffer, 'Stream buffer does not equal the source sequence.'
            
        StreamTest.logger.debug('Test succeeded!')
        
    @log_test(logger, globals.log_separator)
    def testGetAllElements(self):
        StreamTest.logger.debug('Test getting next element from the source.')
        
        # Test data
        stream = Stream(self.source, 'Unit Test Stream')
        
        # Show test data
        StreamTest.logger.debug('Current stream state:\n%s' % (stream.to_pretty_json()))
        
        # Run test
        elements = stream.getAllElements()
         
        # Show test output   
        StreamTest.logger.debug('Final stream state:\n%s' % (stream.to_pretty_json()))
        StreamTest.logger.debug('Fetched element buffer:\n%s' % (str(stream.element_buffer)))
        
        # Verify results
        assert self.source == elements, 'Stream buffer does not equal the source.'
            
        StreamTest.logger.debug('Test succeeded!')
        
    @log_test(logger, globals.log_separator)
    def testPeek(self):
        StreamTest.logger.debug('Test getting next element from the source.')
        
        # Test data
        stream = Stream(self.source, 'Unit Test Stream')
        number_of_elements = 3
        
        # Show test data
        StreamTest.logger.debug('Current stream state:\n%s' % (stream.to_pretty_json()))
        
        # Run test
        for i in range(number_of_elements):
            element = stream.getNextElement()
            next_element = stream.peek()
            
            # Show test output
            StreamTest.logger.debug('Fetching element %d.' % (i))
            StreamTest.logger.debug('Fetched element: "%s"' % (element))
            StreamTest.logger.debug('Peeked at element: "%s"' % (next_element))
            StreamTest.logger.debug('Current stream state:\n%s' % (stream.to_pretty_json()))
            StreamTest.logger.debug('Fetched element buffer: %s' % (str(stream.element_buffer)))
            StreamTest.logger.debug('')
            
            # Verify results
            assert next_element == self.source[i+1], 'Peeked at element does not equal the next element in the source'
         
        # Show test output   
        StreamTest.logger.debug('Final stream state:\n%s' % (stream.to_pretty_json()))
        StreamTest.logger.debug('Fetched element buffer:\n%s' % (str(stream.element_buffer)))
            
        StreamTest.logger.debug('Test succeeded!')
   
   
   
   
   
   
   
   
        
 