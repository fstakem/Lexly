#===============================================================================
# # ------------------------------------------------------
# #
# #   TestParseAndroid.py
# #   By: Fred Stakem
# #   Created: 7.31.13
# #
# # ------------------------------------------------------
# 
# 
# # Libs
# import unittest
# 
# # User defined
# from Globals import *
# from Utilities import *
# 
# from Lexly import Stream
# from Lexly import RawEventSeparator
# from Lexly import Token
# 
# from Lexly.Lexer import LexerState
# from Lexly.Lexer import LexerStateTransition
# from Lexly.Lexer import Lexer
# 
# from Lexly.Parser import Parser
# from Lexly.Parser import DatetimeParser
# from Lexly.Parser import StrParser
# from Lexly.Parser import IntParser
# from Lexly.Parser import EnumParser
# 
# #Main
# class ParseAndroidTest(unittest.TestCase):
#   
#   # Setup logging
#   logger = Utilities.getLogger(__name__)
#   
#   @classmethod
#   def setUpClass(cls):
#       pass
#   
#   @classmethod
#   def tearDownClass(cls):
#       pass
#   
#   def setUp(self):
#       self.tmp_debug_lexer = globals.debug_lexer
#       globals.debug_lexer = True
#       test_files = { 'log_small': '../logs/mobile_sysint_logs/android_log_small.txt',
#                      'log_large': '../logs/mobile_sysint_logs/android_log.txt'}
#       self.test_file = test_files['log_small']
#       self.lexer = None
#       self.parser = None
#       
#   def tearDown(self):
#       globals.debug_lexer = self.tmp_debug_lexer
#                        
#   @log_test(logger, globals.log_separator)
#   def testLexing(self):
#       ParseAndroidTest.logger.debug('Testing the lexing of an android log.')
#       
#       # Test data
#       test_event = None
#       
#       # Setup test
#       events = self.getData(self.test_file)
#       
#       if test_event == None:
#           ParseAndroidTest.logger.debug('Testing %d events.' % (len(events)))
#       else:
#           ParseAndroidTest.logger.debug('Testing a single event: %d' % (test_event))
#           events = [ events[test_event] ]
#           
#       self.lexer = self.createEventLexer()
#       ParseAndroidTest.logger.debug('\n%s' % self.lexer.to_pretty_json())
#       
#       # Run test
#       all_errors = []
#       for i, event in enumerate(events):
#           ParseAndroidTest.logger.debug('Working on event %d.' % (i))
#           ParseAndroidTest.logger.debug('-----< START TEST RUN >-----')
#           
#           self.lexEvent(event)
#           
#           # Verify results 
#           errors = self.lexer.getAllErrors()
#           ParseAndroidTest.logger.debug('Found %d errors.' % (len(errors)))
#           if len(errors) > 0:
#               for j, error in enumerate(errors):
#                   ParseAndroidTest.logger.debug('Found error lexing %d.' % (i))
#               all_errors.append((i, errors))
#               
#           ParseAndroidTest.logger.debug('-----< FINISH TEST RUN >-----')
#        
#       ParseAndroidTest.logger.debug('Found the following errors while parsing the data.')   
#       for error_set in all_errors:
#           ParseAndroidTest.logger.debug('Found %d errors lexing event %d.' % (len(error_set[1]), error_set[0]))
#           
#       ParseAndroidTest.logger.debug('Test succeeded!')
#       
#   def lexEvent(self, event):
#       token = Token('event', Token.ALWAYS_DATA, False, event)
#       ParseAndroidTest.logger.debug('Created token:\n%s' % (token.to_pretty_json()))
#       
#       self.lexer.start(token)
#       tokens = self.lexer.getAllTokens()
#       
#       ParseAndroidTest.logger.debug('Found %d tokens.' % (len(tokens)))
#       assert len(tokens) > 0, 'No tokens found in list.'
#       
#       for i, sub_token in enumerate(tokens):
#           ParseAndroidTest.logger.debug('Found token %d:\n%s' % (i, sub_token.to_pretty_json()))
#       
#   @log_test(logger, globals.log_separator)
#   def testParsing(self):
#       ParseAndroidTest.logger.debug('Testing the parsing of an android log.')
#       
#       # Test data
#       test_event = None
#       
#       # Setup test
#       events = self.getData(self.test_file)
#       
#       if test_event == None:
#           ParseAndroidTest.logger.debug('Testing %d events.' % (len(events)))
#       else:
#           ParseAndroidTest.logger.debug('Testing a single event: %d' % (test_event))
#           events = [ events[test_event] ]
#           
#       self.lexer = self.createEventLexer()
#       parsers = self.createEventParser()
#       self.parser = parsers[0]
#       
#       # Run test
#       all_errors = []
#       for i, event in enumerate(events):
#           ParseAndroidTest.logger.debug('Working on event %d.' % (i))
#           ParseAndroidTest.logger.debug('-----< START TEST RUN >-----')
#           
#           self.lexEvent(event)
#           tokens = self.lexer.getAllTokens()
#           self.parseEvent(tokens)
#           
#           # Verify results 
#           errors = self.lexer.getAllErrors()
#           ParseAndroidTest.logger.debug('Found %d errors.' % (len(errors)))
#           if len(errors) > 0:
#               for j, error in enumerate(errors):
#                   ParseAndroidTest.logger.debug('Found error parsing %d.' % (i))
#               all_errors.append((i, errors))
#               
#           ParseAndroidTest.logger.debug('-----< FINISH TEST RUN >-----')
#        
#       ParseAndroidTest.logger.debug('Found the following errors while parsing the data.')   
#       for error_set in all_errors:
#           ParseAndroidTest.logger.debug('Found %d errors parsing event %d.' % (len(error_set[1]), error_set[0]))
#           
#       ParseAndroidTest.logger.debug('Test succeeded!')
#       
#   def parseEvent(self, tokens):
#       self.parser.start(tokens)
#       fields = self.parser.getAllFlatFields()
#       
#       ParseAndroidTest.logger.debug('Found %d fields.' % (len(fields)))
#       assert len(fields) > 0, 'No fields found in list.'
#       
#       for i, field in enumerate(fields):
#           ParseAndroidTest.logger.debug('Found field %d:\n%s' % (i, field.to_pretty_json()))
#       
#       
#   def getData(self, filename):
#       ParseAndroidTest.logger.debug('Using test data from file %s.' % (filename))
#       test_data = Utilities.readDataFromFile(filename)
#       ParseAndroidTest.logger.debug('Found %d bytes in the data file.' % (len(test_data)))
#       
#       separator = RawEventSeparator('\n', 'Unit Test RawEventSeparator')
#       ParseAndroidTest.logger.debug('Created raw event separator:\n%s' % (separator.to_pretty_json()))
#       events = separator.seperateEvents(test_data)
#       ParseAndroidTest.logger.debug('Found %d events in the data.' % (len(events)))
#       
#       return events
#         
#   def createEventLexer(self):
#       # End state
#       end_token = Token('end', Token.NEVER_DATA, True, 'End Token')
#       end_state = LexerState([], end_token, True, 'End State')
#       
#       # Msg lexer
#       end_transition = LexerStateTransition('EOS', 0, 0, True, end_state, 'Msg to End Transition')
#       msg_token = Token('msg', Token.SOMETIMES_DATA, True, 'Msg Token')
#       msg_state = LexerState([end_transition], msg_token, False, 'Msg State')
#       msg_lexer = Lexer(None, 'source', [], 'Msg Lexer')
#       
#       # Source
#       msg_transition = LexerStateTransition(':', 0, 1, True, msg_state, 'Source to Msg Transition')
#       source_token = Token('source', Token.SOMETIMES_DATA, True, 'Source Token')
#       source_state = LexerState([msg_transition], source_token, False, 'Source State')
#       source_lexer = Lexer(None, 'source', [], 'Source Lexer')
#       
#       # Level lexer
#       source_transition = LexerStateTransition('\s+', 0, 1, True, source_state, 'Level to Source Transition')
#       level_token = Token('level', Token.ALWAYS_DATA, True, 'Level Token')
#       level_state = LexerState([source_transition], level_token, False, 'Level State')
#       level_lexer = Lexer(None, 'level', [], 'Level Lexer')
#       
#       # TID lexer
#       level_transition = LexerStateTransition('\d{1}\s+', 1, 2, True, level_state, 'TID to Level Transition')
#       tid_token = Token('tid', Token.ALWAYS_DATA, True, 'TID Token')
#       tid_state = LexerState([level_transition], tid_token, False, 'TID State')
#       tid_lexer = Lexer(None, 'tid', [], 'TID Lexer')
#       
#       # PID lexer
#       tid_transition = LexerStateTransition('\d{1}\s+', 1, 2, True, tid_state, 'PID to TID Transition')
#       pid_token = Token('pid', Token.ALWAYS_DATA, True, 'PID Token')
#       pid_state = LexerState([tid_transition], pid_token, False, 'PID State')
#       pid_lexer = Lexer(None, 'pid', [], 'PID Lexer')
#       
#       # Datetime lexer
#       pid_transition = LexerStateTransition('\d{3}\s+', 3, 5, True, pid_state, 'Datetime to PID Transition')
#       datetime_token = Token('datetime', Token.ALWAYS_DATA, False, 'Outer Datetime Token')
#       datetime_state = LexerState([pid_transition], datetime_token, False, 'Outer Datetime State')
#       datetime_sub_lexers, datetime_start_state = self.createDatetimeLexers()
#       datetime_lexer = Lexer(datetime_start_state, 'datetime', datetime_sub_lexers, 'Outer Datetime Lexer')
#       
#       # Event lexer
#       datetime_transition = LexerStateTransition('.', 0, -1, True, datetime_state, 'Event to Datetime Transition')
#       event_token = Token('event', Token.NEVER_DATA, False, 'Event Token')
#       event_state = LexerState([datetime_transition], event_token, False, 'Event State')
#       event_lexer = Lexer(event_state, 'event', [datetime_lexer, pid_lexer, tid_lexer, level_lexer, source_lexer, msg_lexer], 'Event Lexer')
#       
#       return event_lexer
#       
#   def createDatetimeLexers(self):
#       # End state
#       end_token = Token('end', Token.NEVER_DATA, True, 'End Token')
#       end_state = LexerState([], end_token, True, 'End State')
#       
#       # Millisecond lexer
#       end_transition = LexerStateTransition('EOS', 0, 0, False, end_state, 'Ms to End Transition')
#       ms_token = Token('millisecond', Token.ALWAYS_DATA, True, 'Millisecond Token')
#       ms_state = LexerState([end_transition], ms_token, False, 'Millisecond State')
#       ms_lexer = Lexer(None, 'millisecond', [], 'Millisecond Lexer')
#       
#       # Second lexer
#       ms_transition = LexerStateTransition('\.', 0, 1, False, ms_state, 'Second to Ms Transition')
#       second_token = Token('second', Token.ALWAYS_DATA, True, 'Second Token')
#       second_state = LexerState([ms_transition], second_token, False, 'Second State')
#       second_lexer = Lexer(None, 'second', [], 'Second Lexer')
#       
#       # Minute lexer
#       second_transition = LexerStateTransition(':', 0, 1, False, second_state, 'Minute to Second Transition')
#       minute_token = Token('minute', Token.ALWAYS_DATA, True, 'Minute Token')
#       minute_state = LexerState([second_transition], minute_token, False, 'Minute State')
#       minute_lexer = Lexer(None, 'minute', [], 'Minute Lexer')
#       
#       # Hour lexer
#       minute_transition = LexerStateTransition(':', 0, 1, False, minute_state, 'Hour to Minute Transition')
#       hour_token = Token('hour', Token.ALWAYS_DATA, True, 'Hour Token')
#       hour_state = LexerState([minute_transition], hour_token, False, 'Hour State')
#       hour_lexer = Lexer(None, 'hour', [], 'Hour Lexer')
#       
#       # Day lexer
#       hour_transition = LexerStateTransition('\s+', 0, 1, True, hour_state, 'Day to Hour Transition')
#       day_token = Token('day', Token.ALWAYS_DATA, True, 'Day Token')
#       day_state = LexerState([hour_transition], day_token, False, 'Day State')
#       day_lexer = Lexer(None, 'day', [], 'Day Lexer')
#       
#       # Month lexer
#       day_transition = LexerStateTransition('-', 0, 1, True, day_state, 'Month to Day Transition')
#       month_token = Token('month', Token.ALWAYS_DATA, True, 'Month Token')
#       month_state = LexerState([day_transition], month_token, False, 'Month State')
#       month_lexer = Lexer(None, 'month', [], 'Month Lexer')
#        
#       # Datetime lexer
#       month_transition = LexerStateTransition('.', 0, -1, True, month_state, 'Datetime to Month Transition')
#       datetime_token = Token('datetime', Token.NEVER_DATA, False, 'Datetime Token')
#       datetime_state = LexerState([month_transition], datetime_token, False, 'Datetime State')
#       datetime_lexer = Lexer(None, 'datetime', [], 'Datetime Lexer')
#       
#       return ((datetime_lexer, month_lexer, day_lexer, hour_lexer, minute_lexer, second_lexer, ms_lexer), datetime_state)
#   
#   def createEventParser(self):
#       # Msg parser
#       msg_parser = StrParser('msg', [], ['msg'], 'Msg Parser')
#       
#       # Source parser
#       source_parser = StrParser('source', [], ['source'], 'Source Parser')
#       
#       # Level parser
#       level_parser = EnumParser('level', [], ['level'], 'Level Parser', ['D', 'V', 'I', 'E', 'W'])
#       
#       # TID
#       tid_parser = IntParser('tid', [], ['tid'], 'Level Parser')
#       
#       # PID
#       pid_parser = IntParser('pid', [], ['pid'], 'PID Parser')
#       
#       # Datetime parser
#       datetime_parser = DatetimeParser('timestamp', [], ['month', 'day', 'hour', 'minute', 'second', 'millisecond'], 'Datetime Parser')
#       
#       # Event parser
#       event_parser = Parser('event', [datetime_parser, pid_parser, tid_parser, level_parser, source_parser, msg_parser], [], 'Event Parser')
#           
#       parsers = (event_parser, datetime_parser, pid_parser, tid_parser, level_parser, source_parser, msg_parser)
#       
#       return parsers
# 
#   
#   
#   
#    
#       
#       
#       
#===============================================================================
