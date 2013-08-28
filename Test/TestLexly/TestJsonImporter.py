# ------------------------------------------------------
#
#   TestJsonImporter.py
#   By: Fred Stakem
#   Created: 8.22.13
#
# ------------------------------------------------------


# Libs
import unittest
import json

# User defined
from Globals import *
from Utilities import *

from Lexly import JsonImporter
from Lexly import RawEventSeparator
from Lexly import Token

#Main
class JsonImporterTest(unittest.TestCase):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
    
    @classmethod
    def setUpClass(cls):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
    
    def setUp(self):
        self.json_parser_path = '../../parsers/ubuntu_syslog.json'
        self.test_data_path = '../logs/ubuntu_sysint_logs/syslog_small'
        self.test_event = None
        self.fail_on_error = True
        self.lexer = None
        self.parser = None
        
        self.tmp_debug_lexer = globals.debug_lexer
        self.tmp_debug_parser = globals.debug_parser
        self.tmp_debug_state_machine = globals.debug_state_machine
        globals.debug_lexer = True
        globals.debug_parser = True
        globals.debug_state_machine = True
        
    def tearDown(self):
        globals.debug_lexer = self.tmp_debug_lexer
        globals.debug_parser = self.tmp_debug_parser
        globals.debug_state_machine = self.tmp_debug_state_machine
    
    @log_test(logger, globals.log_separator)
    def testImportParser(self):
        JsonImporterTest.logger.debug('Test the importation of a parser from json.')
        
        # Test data
        data = self.getJsonFromFile()
        
        # Show test data
        JsonImporterTest.logger.debug('Initial parser data:\n%s' % json.dumps(data, indent=4))
        
        # Run test
        JsonImporterTest.logger.debug('Parsing the json parser.')
        name, created, author, separator, self.lexer, self.parser = JsonImporter.importParser(data)
        
        # Show test output
        JsonImporterTest.logger.debug('Found name: %s' % name)
        JsonImporterTest.logger.debug('Found creation time: %s' % created)
        JsonImporterTest.logger.debug('Found author: %s' % author)
        JsonImporterTest.logger.debug('Found separator:\n%s' % separator.to_pretty_json())
        JsonImporterTest.logger.debug('Found lexer:\n%s' % self.lexer.to_pretty_json())
        JsonImporterTest.logger.debug('Found parser:\n%s' % self.parser.to_pretty_json())
        
        # Verify results
        events = self.getTestData()
        self.verifyParser(self.parser, events)
        
        JsonImporterTest.logger.debug('Test succeeded!')
            
    def verifyParser(self, parser, events):
        if self.test_event == None:
            JsonImporterTest.logger.debug('Testing %d events.' % (len(events)))
        else:
            JsonImporterTest.logger.debug('Testing a single event: %d' % (self.test_event))
            events = [ events[self.test_event] ]
            
        all_errors = []
        for i, event in enumerate(events):
            JsonImporterTest.logger.debug('Working on event %d.' % (i))
            
            self.lexEvent(event)
            tokens = self.lexer.getAllTokens()
            errors = self.lexer.getAllErrors()
            if len(errors) > 0:
                all_errors.append((i, errors))
                
            self.parseEvent(tokens)
            errors = self.parser.getAllErrors()
            if len(errors) > 0:
                all_errors.append((i, errors))
                
        JsonImporterTest.logger.debug('Found the following errors while parsing the data.')   
        for error_set in all_errors:
            JsonImporterTest.logger.debug('Found %d errors parsing event %d.' % (len(error_set[1]), error_set[0]))
            
        if self.fail_on_error:
            assert len(all_errors) == 0, 'Found errors during parsing.'
        
    def getJsonFromFile(self):
        JsonImporterTest.logger.debug('Using test data from file %s.' % (self.json_parser_path))
        json_data = Utilities.readDataFromFile(self.json_parser_path)
        JsonImporterTest.logger.debug('Found %d bytes in the data file.' % (len(json_data)))
        data = json.loads(json_data)
        
        return data
    
    def getTestData(self):
        JsonImporterTest.logger.debug('Using test data from file %s.' % (self.test_data_path))
        test_data = Utilities.readDataFromFile(self.test_data_path)
        JsonImporterTest.logger.debug('Found %d bytes in the data file.' % (len(test_data)))
        
        separator = RawEventSeparator('\n', 'Unit Test RawEventSeparator')
        events = separator.seperateEvents(test_data)
        JsonImporterTest.logger.debug('Found %d events in the data.' % (len(events)))
        
        return events
    
    def lexEvent(self, event):
        token = Token('event', Token.ALWAYS_DATA, False, event)
        JsonImporterTest.logger.debug('Created token:\n%s' % (token.to_pretty_json()))
        
        self.lexer.start(token)
        tokens = self.lexer.getAllTokens()
        
        JsonImporterTest.logger.debug('Found %d tokens.' % (len(tokens)))
        assert len(tokens) > 0, 'No tokens found in list.'
        
        for i, sub_token in enumerate(tokens):
            JsonImporterTest.logger.debug('Found token %d:\n%s' % (i, sub_token.to_pretty_json()))
            
    def parseEvent(self, tokens):
        self.parser.start(tokens)
        fields = self.parser.getAllFlatFields()
        
        JsonImporterTest.logger.debug('Found %d fields.' % (len(fields)))
        assert len(fields) > 0, 'No fields found in list.'
        
        for i, field in enumerate(fields):
            JsonImporterTest.logger.debug('Found field %d:\n%s' % (i, field.to_pretty_json()))



