# ------------------------------------------------------
#
#   TestParseSyslog.py
#   By: Fred Stakem
#   Created: 7.23.13
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
class ParseSyslogTest(unittest.TestCase):
    
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
        self.json_parser_path = '../../parsers/ubuntu_syslog.json'
        test_files = { 'ubuntu_syslog_small': '../logs/ubuntu_sysint_logs/syslog_small',
                       'ubuntu_syslog_large': '../logs/ubuntu_sysint_logs/syslog',
                       'ubuntu_auth': '../logs/ubuntu_sysint_logs/auth.log', 
                       'ubuntu_kern_small': '../logs/ubuntu_sysint_logs/kern_small.log',
                       'ubuntu_kern': '../logs/ubuntu_sysint_logs/kern.log'}
        self.test_file = test_files['ubuntu_syslog_small']
        self.test_event = None
        self.separator = None
        self.lexer = None
        self.parser = None
        
    def tearDown(self):
        globals.debug_lexer = self.tmp_debug_lexer
        globals.debug_parser = self.tmp_debug_parser
                         
    @log_test(logger, globals.log_separator)
    def testLexing(self):
        ParseSyslogTest.logger.debug('Testing the lexing of syslog.')
        
        # Setup test
        self.separator, self.lexer, self.parser = self.createParsingComponents()
        events = self.getData(self.test_file)
        
        if self.test_event == None:
            ParseSyslogTest.logger.debug('Testing %d events.' % (len(events)))
        else:
            ParseSyslogTest.logger.debug('Testing a single event: %d' % (self.test_event))
            events = [ events[self.test_event] ]
            
        ParseSyslogTest.logger.debug('\n%s' % self.lexer.to_pretty_json())
            
        # Run test
        all_errors = []
        for i, event in enumerate(events):
            ParseSyslogTest.logger.debug('Working on event %d.' % (i))
            
            self.lexEvent(event)
            
            # Verify results 
            errors = self.lexer.getAllErrors()
            if len(errors) > 0:
                ParseSyslogTest.logger.debug('Found %d error(s) lexing event %d.' % (len(errors), i))
                all_errors.append((i, errors))
                
        ParseSyslogTest.logger.debug('Found the following errors while lexing the data.')   
        for error_set in all_errors:
            ParseSyslogTest.logger.debug('Found %d errors lexing event %d.' % (len(error_set[1]), error_set[0]))
            for error in error_set[1]:
                ParseSyslogTest.logger.debug('Error reason: %s' % (error.reason))
                
        if self.fail_on_error:
            assert len(all_errors) == 0, 'Found errors during lexing.'
            
        ParseSyslogTest.logger.debug('Test succeeded!')
        
    def lexEvent(self, event):
        token = Token('event', Token.ALWAYS_DATA, False, event)
        ParseSyslogTest.logger.debug('Created token:\n%s' % (token.to_pretty_json()))
        
        self.lexer.start(token)
        tokens = self.lexer.getAllTokens()
        
        ParseSyslogTest.logger.debug('Found %d tokens.' % (len(tokens)))
        assert len(tokens) > 0, 'No tokens found in list.'
        
        for i, sub_token in enumerate(tokens):
            ParseSyslogTest.logger.debug('Found token %d:\n%s' % (i, sub_token.to_pretty_json()))
        
    @log_test(logger, globals.log_separator)
    def testParsing(self):
        ParseSyslogTest.logger.debug('Testing the parsing of syslog.')
        
        # Setup test
        self.separator, self.lexer, self.parser = self.createParsingComponents()
        events = self.getData(self.test_file)
        
        if self.test_event == None:
            ParseSyslogTest.logger.debug('Testing %d events.' % (len(events)))
        else:
            ParseSyslogTest.logger.debug('Testing a single event: %d' % (self.test_event))
            events = [ events[self.test_event] ]
                      
        # Run test
        all_errors = []
        for i, event in enumerate(events):
            ParseSyslogTest.logger.debug('Working on event %d.' % (i))
            
            self.lexEvent(event)
            tokens = self.lexer.getAllTokens()
            self.parseEvent(tokens)
            
            # Verify results 
            errors = self.parser.getAllErrors()
            if len(errors) > 0:
                ParseSyslogTest.logger.debug('Found %d error(s) parsing event %d.' % (len(errors), i))
                all_errors.append((i, errors))
                
        ParseSyslogTest.logger.debug('Found the following errors while parsing the data.')   
        for error_set in all_errors:
            ParseSyslogTest.logger.debug('Found %d errors parsing event %d.' % (len(error_set[1]), error_set[0]))
            for error in error_set[1]:
                ParseSyslogTest.logger.debug('Error reason: %s.' % (error.reason))
        
        if self.fail_on_error:
            assert len(all_errors) == 0, 'Found errors during parsing.'
        
        ParseSyslogTest.logger.debug('Test succeeded!')
        
    def parseEvent(self, tokens):
        self.parser.start(tokens)
        fields = self.parser.getAllFlatFields()
        
        ParseSyslogTest.logger.debug('Found %d fields.' % (len(fields)))
        assert len(fields) > 0, 'No fields found in list.'
        
        for i, field in enumerate(fields):
            ParseSyslogTest.logger.debug('Found field %d:\n%s' % (i, field.to_pretty_json()))
        
    def getData(self, filename):
        ParseSyslogTest.logger.debug('Using test data from file %s.' % (filename))
        test_data = Utilities.readDataFromFile(filename)
        ParseSyslogTest.logger.debug('Found %d bytes in the data file.' % (len(test_data)))
        events = self.separator.seperateEvents(test_data)
        ParseSyslogTest.logger.debug('Found %d events in the data.' % (len(events)))
        
        return events
    
    def createParsingComponents(self):
        json_data = Utilities.readDataFromFile(self.json_parser_path)
        data = json.loads(json_data)
        name, created, author, separator, lexer, parser = JsonImporter.importParser(data)
        
        return (separator, lexer, parser)
          
        