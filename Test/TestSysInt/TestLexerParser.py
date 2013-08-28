# ------------------------------------------------------
#
#   TestLexerParser.py
#   By: Fred Stakem
#   Created: 8.28.13
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
class LexerParserTest(unittest.TestCase):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
    
    @classmethod
    def setUpClass(cls):
        cls.test_vector = { 'syslog':   { 'parser_path': '../parsers/ubuntu_syslog.json', 
                                          'log_files': ['../logs/ubuntu_sysint_logs/syslog_small', '../logs/ubuntu_sysint_logs/syslog'] },
                            'auth':     { 'parser_path': '../parsers/ubuntu_syslog.json', 
                                          'log_files': ['../logs/ubuntu_sysint_logs/auth.log'] },
                            'kern':     { 'parser_path': '../parsers/ubuntu_syslog.json', 
                                          'log_files': ['../logs/ubuntu_sysint_logs/kern_small.log', '../logs/ubuntu_sysint_logs/kern.log'] },
                            'android':  { 'parser_path': '../parsers/android.json', 
                                          'log_files': ['../logs/mobile_sysint_logs/android_log_small.txt', '../logs/mobile_sysint_logs/android_log.txt'] },
                            'ios':      { 'parser_path': '../parsers/ios.json', 
                                          'log_files': ['../logs/mobile_sysint_logs/iphone_log.txt'] },}
        
    @classmethod
    def tearDownClass(cls):
        pass
    
    def setUp(self):
        # Debugging
        self.tmp_debug_lexer = globals.debug_lexer
        self.tmp_debug_parser = globals.debug_parser
        globals.debug_lexer = False
        globals.debug_parser = False
        self.fail_on_error = True
        
        # Test
        self.test = LexerParserTest.test_vector['syslog']
        self.json_parser_path = self.test['parser_path']
        self.test_file = self.test['log_files'][0]
        self.test_event = None
        
        # Parser vars
        self.name, self.created, self.author, self.separator, self.lexer, self.parser = self.createParsingComponents()
        
    def tearDown(self):
        globals.debug_lexer = self.tmp_debug_lexer
        globals.debug_parser = self.tmp_debug_parser
                         
    @log_test(logger, globals.log_separator)
    def testLexing(self):
        LexerParserTest.logger.debug('Testing the lexing of: %s' % self.name)
        LexerParserTest.logger.debug('JSON parser created: %s' % self.created)
        LexerParserTest.logger.debug('JSON parser created by: %s' % self.author)
        
        # Setup test
        events = self.getData(self.test_file)
        
        if self.test_event == None:
            LexerParserTest.logger.debug('Testing %d events.' % (len(events)))
        else:
            LexerParserTest.logger.debug('Testing a single event: %d' % (self.test_event))
            events = [ events[self.test_event] ]
            
        LexerParserTest.logger.debug('\n%s' % self.lexer.to_pretty_json())
            
        # Run test
        all_errors = []
        for i, event in enumerate(events):
            LexerParserTest.logger.debug('Working on event %d.' % (i))
            
            self.lexEvent(event)
            
            # Verify results 
            errors = self.lexer.getAllErrors()
            if len(errors) > 0:
                LexerParserTest.logger.debug('Found %d error(s) lexing event %d.' % (len(errors), i))
                all_errors.append((i, errors))
                
        LexerParserTest.logger.debug('Found the following errors while lexing the data.')   
        for error_set in all_errors:
            LexerParserTest.logger.debug('Found %d errors lexing event %d.' % (len(error_set[1]), error_set[0]))
            for error in error_set[1]:
                LexerParserTest.logger.debug('Error reason: %s' % (error.reason))
                
        if self.fail_on_error:
            assert len(all_errors) == 0, 'Found errors during lexing.'
            
        LexerParserTest.logger.debug('Test succeeded!')
        
    def lexEvent(self, event):
        token = Token('event', Token.ALWAYS_DATA, False, event)
        LexerParserTest.logger.debug('Created token:\n%s' % (token.to_pretty_json()))
        
        self.lexer.start(token)
        tokens = self.lexer.getAllTokens()
        
        LexerParserTest.logger.debug('Found %d tokens.' % (len(tokens)))
        assert len(tokens) > 0, 'No tokens found in list.'
        
        for i, sub_token in enumerate(tokens):
            LexerParserTest.logger.debug('Found token %d:\n%s' % (i, sub_token.to_pretty_json()))
        
    @log_test(logger, globals.log_separator)
    def testParsing(self):
        LexerParserTest.logger.debug('Testing the parsing of: %s' % self.name)
        LexerParserTest.logger.debug('JSON parser created: %s' % self.created)
        LexerParserTest.logger.debug('JSON parser created by: %s' % self.author)
        
        # Setup test
        events = self.getData(self.test_file)
        
        if self.test_event == None:
            LexerParserTest.logger.debug('Testing %d events.' % (len(events)))
        else:
            LexerParserTest.logger.debug('Testing a single event: %d' % (self.test_event))
            events = [ events[self.test_event] ]
                      
        # Run test
        all_errors = []
        for i, event in enumerate(events):
            LexerParserTest.logger.debug('Working on event %d.' % (i))
            
            self.lexEvent(event)
            tokens = self.lexer.getAllTokens()
            self.parseEvent(tokens)
            
            # Verify results 
            errors = self.parser.getAllErrors()
            if len(errors) > 0:
                LexerParserTest.logger.debug('Found %d error(s) parsing event %d.' % (len(errors), i))
                all_errors.append((i, errors))
                
        LexerParserTest.logger.debug('Found the following errors while parsing the data.')   
        for error_set in all_errors:
            LexerParserTest.logger.debug('Found %d errors parsing event %d.' % (len(error_set[1]), error_set[0]))
            for error in error_set[1]:
                LexerParserTest.logger.debug('Error reason: %s.' % (error.reason))
        
        if self.fail_on_error:
            assert len(all_errors) == 0, 'Found errors during parsing.'
        
        LexerParserTest.logger.debug('Test succeeded!')
        
    def parseEvent(self, tokens):
        self.parser.start(tokens)
        fields = self.parser.getAllFlatFields()
        
        LexerParserTest.logger.debug('Found %d fields.' % (len(fields)))
        assert len(fields) > 0, 'No fields found in list.'
        
        for i, field in enumerate(fields):
            LexerParserTest.logger.debug('Found field %d:\n%s' % (i, field.to_pretty_json()))
        
    def getData(self, filename):
        LexerParserTest.logger.debug('Using test data from file %s.' % (filename))
        test_data = Utilities.readDataFromFile(filename)
        LexerParserTest.logger.debug('Found %d bytes in the data file.' % (len(test_data)))
        events = self.separator.seperateEvents(test_data)
        LexerParserTest.logger.debug('Found %d events in the data.' % (len(events)))
        
        return events
    
    def createParsingComponents(self):
        json_data = Utilities.readDataFromFile(self.json_parser_path)
        data = json.loads(json_data)
        name, created, author, separator, lexer, parser = JsonImporter.importParser(data)
        
        return (name, created, author, separator, lexer, parser)
          
        