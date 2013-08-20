# ------------------------------------------------------
#
#   TestRawEventSeparator.py
#   By: Fred Stakem
#   Created: 6.20.13
#
# ------------------------------------------------------


# Libs
import unittest

# User defined
from Globals import *
from Utilities import *
from Lexly import RawEventSeparator

#Main
class RawEventSeparatorTest(unittest.TestCase):
    
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
    def testSeperateLines(self):
        RawEventSeparatorTest.logger.debug('Test splitting of data into separate lines.')
        
        # Test data
        separator = '\n'
        source = 'Go to heaven for the climate\nHell for the company\n'
        event_separator = RawEventSeparator(separator, 'Unit Test RawEventSeperator')
        
        # Show test data
        RawEventSeparatorTest.logger.debug('Created separator: "%s"' % (separator.replace('\n', '\\n')))
        RawEventSeparatorTest.logger.debug('Created source: "%s"' % (source.replace('\n', '\\n')))
        RawEventSeparatorTest.logger.debug('Created event separator:\n%s' % (event_separator.to_pretty_json()))
        
        # Run test
        events = event_separator.seperateEvents(source)
        
        # Show test output
        RawEventSeparatorTest.logger.debug('Returned event 0: "%s"' % (events[0]))
        RawEventSeparatorTest.logger.debug('Returned event 1: "%s"' % (events[1]))
      
        # Verify results
        assert events[0] == source.split('\n')[0], 'The first event was not properly extracted from the source.'
        assert events[1] == source.split('\n')[1], 'The second event was not properly extracted from the source.'
        assert len(events) == 2, 'Incorrect number of events extracted from the source.'
        
        RawEventSeparatorTest.logger.debug('Test succeeded!')
        
 