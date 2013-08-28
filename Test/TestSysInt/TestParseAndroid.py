# ------------------------------------------------------
#
#   TestParseAndroid.py
#   By: Fred Stakem
#   Created: 7.31.13
#
# ------------------------------------------------------


# Libs
import unittest
import json

# User defined
from Globals import *
from Utilities import *
from Lexly import Token
from Lexly import JsonImporter

#Main
class ParseAndroidTest(unittest.TestCase):
    
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
        self.tmp_debug_parser = globals.debug_parser
        globals.debug_lexer = False
        globals.debug_parser = False
        self.fail_on_error = True
        self.json_parser_path = '../../parsers/android.json'
        test_files = { 'log_small': '../logs/mobile_sysint_logs/android_log_small.txt',
                       'log_large': '../logs/mobile_sysint_logs/android_log.txt'}
        self.test_file = test_files['log_small']
        self.test_event = None
        self.separator = None
        self.lexer = None
        self.parser = None
        
    def tearDown(self):
        globals.debug_lexer = self.tmp_debug_lexer
        globals.debug_parser = self.tmp_debug_parser
                         
    @log_test(logger, globals.log_separator)
    def testLexing(self):
        ParseAndroidTest.logger.debug('Testing the lexing of an android log.')
        
        # Setup test
        self.separator, self.lexer, self.parser = self.createParsingComponents()
        events = self.getData(self.test_file)
        
        if self.test_event == None:
            ParseAndroidTest.logger.debug('Testing %d events.' % (len(events)))
        else:
            ParseAndroidTest.logger.debug('Testing a single event: %d' % (self.test_event))
            events = [ events[self.test_event] ]
            
        # Run test
        all_errors = []
        for i, event in enumerate(events):
            ParseAndroidTest.logger.debug('Working on event %d.' % (i))
            
            self.lexEvent(event)
            
            # Verify results 
            errors = self.lexer.getAllErrors()
            if len(errors) > 0:
                ParseAndroidTest.logger.debug('Found %d error(s) lexing event %d.' % (len(errors), i))
                all_errors.append((i, errors))
                
        ParseAndroidTest.logger.debug('Found the following errors while lexing the data.')   
        for error_set in all_errors:
            ParseAndroidTest.logger.debug('Found %d errors lexing event %d.' % (len(error_set[1]), error_set[0]))
            for error in error_set[1]:
                ParseAndroidTest.logger.debug('Error reason: %s' % (error.reason))
                
        if self.fail_on_error:
            assert len(all_errors) == 0, 'Found errors during lexing.'
            
        ParseAndroidTest.logger.debug('Test succeeded!')
        
    def lexEvent(self, event):
        token = Token('event', Token.ALWAYS_DATA, False, event)
        ParseAndroidTest.logger.debug('Created token:\n%s' % (token.to_pretty_json()))
        
        self.lexer.start(token)
        tokens = self.lexer.getAllTokens()
        
        ParseAndroidTest.logger.debug('Found %d tokens.' % (len(tokens)))
        assert len(tokens) > 0, 'No tokens found in list.'
        
        for i, sub_token in enumerate(tokens):
            ParseAndroidTest.logger.debug('Found token %d:\n%s' % (i, sub_token.to_pretty_json()))
        
    @log_test(logger, globals.log_separator)
    def testParsing(self):
        ParseAndroidTest.logger.debug('Testing the parsing of an android log.')
        
        # Setup test
        self.separator, self.lexer, self.parser = self.createParsingComponents()
        events = self.getData(self.test_file)
        
        if self.test_event == None:
            ParseAndroidTest.logger.debug('Testing %d events.' % (len(events)))
        else:
            ParseAndroidTest.logger.debug('Testing a single event: %d' % (self.test_event))
            events = [ events[self.test_event] ]
            
        # Run test
        all_errors = []
        for i, event in enumerate(events):
            ParseAndroidTest.logger.debug('Working on event %d.' % (i))
            
            self.lexEvent(event)
            tokens = self.lexer.getAllTokens()
            self.parseEvent(tokens)
            
            # Verify results 
            errors = self.parser.getAllErrors()
            if len(errors) > 0:
                ParseAndroidTest.logger.debug('Found %d error(s) parsing event %d.' % (len(errors), i))
                all_errors.append((i, errors))
                
        ParseAndroidTest.logger.debug('Found the following errors while parsing the data.')   
        for error_set in all_errors:
            ParseAndroidTest.logger.debug('Found %d errors parsing event %d.' % (len(error_set[1]), error_set[0]))
            for error in error_set[1]:
                ParseAndroidTest.logger.debug('Error reason: %s.' % (error.reason))
                
        if self.fail_on_error:
            assert len(all_errors) == 0, 'Found errors during parsing.'
            
        ParseAndroidTest.logger.debug('Test succeeded!')
        
    def parseEvent(self, tokens):
        self.parser.start(tokens)
        fields = self.parser.getAllFlatFields()
        
        ParseAndroidTest.logger.debug('Found %d fields.' % (len(fields)))
        assert len(fields) > 0, 'No fields found in list.'
        
        for i, field in enumerate(fields):
            ParseAndroidTest.logger.debug('Found field %d:\n%s' % (i, field.to_pretty_json()))
        
    def getData(self, filename):
        ParseAndroidTest.logger.debug('Using test data from file %s.' % (filename))
        test_data = Utilities.readDataFromFile(filename)
        ParseAndroidTest.logger.debug('Found %d bytes in the data file.' % (len(test_data)))
        events = self.separator.seperateEvents(test_data)
        ParseAndroidTest.logger.debug('Found %d events in the data.' % (len(events)))
        
        return events
    
    def createParsingComponents(self):
        json_data = Utilities.readDataFromFile(self.json_parser_path)
        data = json.loads(json_data)
        name, created, author, separator, lexer, parser = JsonImporter.importParser(data)
        
        return (separator, lexer, parser)
          
          
     