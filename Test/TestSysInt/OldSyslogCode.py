#===============================================================================
# # ------------------------------------------------------
# #
# #   TestParseSyslog.py
# #   By: Fred Stakem
# #   Created: 7.23.13
# #
# # ------------------------------------------------------
# 
# 
# # Libs
# import unittest
# import json
# 
# # User defined
# from Globals import *
# from Utilities import *
# 
# from Lexly import Stream
# from Lexly import RawEventSeparator
# from Lexly import Token
# from Lexly import JsonImporter
# 
# from Lexly.Lexer import LexerState
# from Lexly.Lexer import LexerStateTransition
# from Lexly.Lexer import Lexer
# 
# from Lexly.Parser import Parser
# from Lexly.Parser import DatetimeParser
# from Lexly.Parser import StrParser
# from Lexly.Parser import IntParser
# 
# #Main
# class ParseSyslogTest(unittest.TestCase):
# 
#    # Setup logging
#    logger = Utilities.getLogger(__name__)
# 
#    @classmethod
#    def setUpClass(cls):
#        pass
# 
#    @classmethod
#    def tearDownClass(cls):
#        pass
# 
#    def setUp(self):
#        self.tmp_debug_lexer = globals.debug_lexer
#        self.tmp_debug_parser = globals.debug_parser
#        globals.debug_lexer = False
#        globals.debug_parser = False
#        self.fail_on_error = True
#         test_files = { 'ubuntu_syslog_small': '../logs/ubuntu_sysint_logs/syslog_small',
#                        'ubuntu_syslog_large': '../logs/ubuntu_sysint_logs/syslog',
#                       'ubuntu_auth': '../logs/ubuntu_sysint_logs/auth.log',
#                        'ubuntu_kern_small': '../logs/ubuntu_sysint_logs/kern_small.log',
#                       'ubuntu_kern': '../logs/ubuntu_sysint_logs/kern.log'}
#        self.test_file = test_files['ubuntu_syslog_small']
#        self.test_event = None
#        self.lexer = None
#        self.parser = None
# 
#    def tearDown(self):
#        globals.debug_lexer = self.tmp_debug_lexer
#        globals.debug_parser = self.tmp_debug_parser
# 
#    @log_test(logger, globals.log_separator)
#    def testLexing(self):
#        ParseSyslogTest.logger.debug('Testing the lexing of syslog.')
# 
#        # Setup test
#        events = self.getData(self.test_file)
# 
#        if self.test_event == None:
#             ParseSyslogTest.logger.debug('Testing %d events.' % (len(events)))
#        else:
#             ParseSyslogTest.logger.debug('Testing a single event: %d' % (self.test_event))
#            events = [ events[self.test_event] ]
# 
#        #self.lexer = self.createEventLexer()
#        self.lexer, self.parser = self.createParser()
#        for i in range(20):
#             ParseSyslogTest.logger.debug('++++++++++++++++++++++++++++++++++++++++')
#        ParseSyslogTest.logger.debug('\n%s' % self.lexer.to_pretty_json())
# 
#        # Run test
#        all_errors = []
#        for i, event in enumerate(events):
#            ParseSyslogTest.logger.debug('Working on event %d.' % (i))
#            ParseSyslogTest.logger.debug('-----< START TEST RUN >-----')
# 
#            self.lexEvent(event)
# 
#            # Verify results
#            errors = self.lexer.getAllErrors()
#            ParseSyslogTest.logger.debug('Found %d errors.' % (len(errors)))
#            if len(errors) > 0:
#                for j, error in enumerate(errors):
#                     ParseSyslogTest.logger.debug('Found error lexing %d.' % (i))
#                all_errors.append((i, errors))
# 
#            ParseSyslogTest.logger.debug('-----< FINISH TEST RUN >-----')
# 
#         ParseSyslogTest.logger.debug('Found the following errors while parsing the data.')
#        for error_set in all_errors:
#             ParseSyslogTest.logger.debug('Found %d errors lexing event %d.' % (len(error_set[1]), error_set[0]))
# 
#        if self.fail_on_error:
#            assert len(all_errors) == 0, 'Found errors during lexing.'
# 
#        ParseSyslogTest.logger.debug('Test succeeded!')
# 
#    def lexEvent(self, event):
#        token = Token('event', Token.ALWAYS_DATA, False, event)
#         ParseSyslogTest.logger.debug('Created token:\n%s' % (token.to_pretty_json()))
# 
#        self.lexer.start(token)
#        tokens = self.lexer.getAllTokens()
# 
#        ParseSyslogTest.logger.debug('Found %d tokens.' % (len(tokens)))
#        assert len(tokens) > 0, 'No tokens found in list.'
# 
#        for i, sub_token in enumerate(tokens):
#             ParseSyslogTest.logger.debug('Found token %d:\n%s' % (i, sub_token.to_pretty_json()))
# 
#    @log_test(logger, globals.log_separator)
#    def testParsing(self):
#        ParseSyslogTest.logger.debug('Testing the parsing of syslog.')
# 
#        # Setup test
#        events = self.getData(self.test_file)
# 
#        if self.test_event == None:
#             ParseSyslogTest.logger.debug('Testing %d events.' % (len(events)))
#        else:
#             ParseSyslogTest.logger.debug('Testing a single event: %d' % (self.test_event))
#            events = [ events[self.test_event] ]
# 
#        self.lexer = self.createEventLexer()
#        parsers = self.createEventParser()
#        self.parser = parsers[0]
# 
#        # Run test
#        all_errors = []
#        for i, event in enumerate(events):
#            ParseSyslogTest.logger.debug('Working on event %d.' % (i))
#            ParseSyslogTest.logger.debug('-----< START TEST RUN >-----')
# 
#            self.lexEvent(event)
#            tokens = self.lexer.getAllTokens()
#            self.parseEvent(tokens)
# 
#            # Verify results
#            errors = self.parser.getAllErrors()
#            ParseSyslogTest.logger.debug('Found %d errors.' % (len(errors)))
#            if len(errors) > 0:
#                for j, error in enumerate(errors):
#                     ParseSyslogTest.logger.debug('Found error parsing %d.' % (i))
#                all_errors.append((i, errors))
# 
#            ParseSyslogTest.logger.debug('-----< FINISH TEST RUN >-----')
# 
#         ParseSyslogTest.logger.debug('Found the following errors while parsing the data.')
#        for error_set in all_errors:
#             ParseSyslogTest.logger.debug('Found %d errors parsing event %d.' % (len(error_set[1]), error_set[0]))
# 
#        if self.fail_on_error:
#            assert len(all_errors) == 0, 'Found errors during parsing.'
# 
#        ParseSyslogTest.logger.debug('Test succeeded!')
# 
#    def parseEvent(self, tokens):
#        self.parser.start(tokens)
#        fields = self.parser.getAllFlatFields()
# 
#        ParseSyslogTest.logger.debug('Found %d fields.' % (len(fields)))
#        assert len(fields) > 0, 'No fields found in list.'
# 
#        for i, field in enumerate(fields):
#             ParseSyslogTest.logger.debug('Found field %d:\n%s' % (i, field.to_pretty_json()))
# 
#    def getData(self, filename):
#         ParseSyslogTest.logger.debug('Using test data from file %s.' % (filename))
#        test_data = Utilities.readDataFromFile(filename)
#         ParseSyslogTest.logger.debug('Found %d bytes in the data file.' % (len(test_data)))
# 
#        separator = RawEventSeparator('\n', 'Unit Test RawEventSeparator')
#         ParseSyslogTest.logger.debug('Created raw event separator:\n%s' % (separator.to_pretty_json()))
#        events = separator.seperateEvents(test_data)
#         ParseSyslogTest.logger.debug('Found %d events in the data.' % (len(events)))
# 
#        return events
# 
#    def createParser(self):
#        # Added code
#        file_path = '../../parsers/ubuntu_syslog.json'
#        json_data = Utilities.readDataFromFile(file_path)
#        data = json.loads(json_data)
#         name, created, author, separator, lexer, parser = JsonImporter.importParser(data)
# 
#        return (lexer, parser)
# 
#    def createEventLexer(self):
#        # End state
#        end_token = Token('end', Token.NEVER_DATA, True, 'End Token')
#        end_state = LexerState([], end_token, True, 'End State')
# 
#        # Msg lexer
#         end_transition = LexerStateTransition('EOS', 0, 0, True, end_state, 'Msg to End Transition')
#         msg_token = Token('msg', Token.SOMETIMES_DATA, False, 'Outer Msg Token')
#         msg_state = LexerState([end_transition], msg_token, False, 'Outer Msg State')
#        msg_sub_lexers, msg_start_state = self.createMsgLexers()
#         msg_lexer = Lexer(msg_start_state, 'msg', msg_sub_lexers, 'Outer Msg Lexer')
# 
#        # Source lexer
#         msg_transition = LexerStateTransition(':', 0, 1, True, msg_state, 'Source to Msg Transition')
#         source_token = Token('source', Token.ALWAYS_DATA, False, 'Outer Source Token')
#         source_state = LexerState([msg_transition], source_token, True, 'Outer Source State')
#        source_sub_lexers, source_start_state = self.createSourceLexers()
#         source_lexer = Lexer(source_start_state, 'source', source_sub_lexers, 'Outer Source Lexer')
# 
#        # Datetime lexer
#         source_transition = LexerStateTransition('\d{2}:\d{2}:\d{2}', 8, 8, True, source_state, 'Datetime to Source Transition')
#         datetime_token = Token('datetime', Token.ALWAYS_DATA, False, 'Outer Datetime Token')
#         datetime_state = LexerState([source_transition], datetime_token, False, 'Outer Datetime State')
#         datetime_sub_lexers, datetime_start_state = self.createDatetimeLexers()
#         datetime_lexer = Lexer(datetime_start_state, 'datetime', datetime_sub_lexers, 'Outer Datetime Lexer')
# 
#        # Event lexer
#         datetime_transition = LexerStateTransition('.', 0, -1, True, datetime_state, 'Event to Datetime Transition')
#        event_token = Token('event', Token.NEVER_DATA, False, 'Event Token')
#         event_state = LexerState([datetime_transition], event_token, False, 'Event State')
#         event_lexer = Lexer(event_state, 'event', [datetime_lexer, source_lexer, msg_lexer], 'Event Lexer')
# 
#        return event_lexer
# 
#    def createDatetimeLexers(self):
#        # End state
#        end_token = Token('end', Token.NEVER_DATA, True, 'End Token')
#        end_state = LexerState([], end_token, True, 'End State')
# 
#        # Second lexer
#         end_transition = LexerStateTransition('EOS', 0, 0, False, end_state, 'Second to End Transition')
#         second_token = Token('second', Token.ALWAYS_DATA, True, 'Second Token')
#         second_state = LexerState([end_transition], second_token, False, 'Second State')
#        second_lexer = Lexer(None, 'second', [], 'Second Lexer')
# 
#        # Minute lexer
#         second_transition = LexerStateTransition(':', 0, 1, False, second_state, 'Minute to Second Transition')
#         minute_token = Token('minute', Token.ALWAYS_DATA, True, 'Minute Token')
#         minute_state = LexerState([second_transition], minute_token, False, 'Minute State')
#        minute_lexer = Lexer(None, 'minute', [], 'Minute Lexer')
# 
#        # Hour lexer
#         minute_transition = LexerStateTransition(':', 0, 1, False, minute_state, 'Hour to Minute Transition')
#        hour_token = Token('hour', Token.ALWAYS_DATA, True, 'Hour Token')
#         hour_state = LexerState([minute_transition], hour_token, False, 'Hour State')
#        hour_lexer = Lexer(None, 'hour', [], 'Hour Lexer')
# 
#        # Day lexer
#         hour_transition = LexerStateTransition('\s+', 0, 1, True, hour_state, 'Day to Hour Transition')
#        day_token = Token('day', Token.ALWAYS_DATA, True, 'Day Token')
#         day_state = LexerState([hour_transition], day_token, False, 'Day State')
#        day_lexer = Lexer(None, 'day', [], 'Day Lexer')
# 
#        # Month lexer
#         day_transition = LexerStateTransition('\s+', 0, 1, True, day_state, 'Month to Day Transition')
#        month_token = Token('month', Token.ALWAYS_DATA, True, 'Month Token')
#         month_state = LexerState([day_transition], month_token, False, 'Month State')
#        month_lexer = Lexer(None, 'month', [], 'Month Lexer')
# 
#        # Datetime lexer
#         month_transition = LexerStateTransition('.', 0, -1, True, month_state, 'Datetime to Month Transition')
#         datetime_token = Token('datetime', Token.NEVER_DATA, False, 'Datetime Token')
#         datetime_state = LexerState([month_transition], datetime_token, False, 'Datetime State')
#        datetime_lexer = Lexer(None, 'datetime', [], 'Datetime Lexer')
# 
#         return ((datetime_lexer, month_lexer, day_lexer, hour_lexer, minute_lexer, second_lexer), datetime_state)
# 
#    def createSourceLexers(self):
#        # End state
#        end_token = Token('end', Token.NEVER_DATA, True, 'End Token')
#        end_state = LexerState([], end_token, True, 'End State')
# 
#        # Component id lexer
#         comp_id_to_end_transition = LexerStateTransition('EOS', -1, 0, True, end_state, 'Component ID to End Transition')
#         comp_id_token = Token('component_id', Token.SOMETIMES_DATA, True, 'Component ID Token')
#         comp_id_state = LexerState([comp_id_to_end_transition], comp_id_token, False, 'Component ID State')
#        comp_id_lexer = Lexer(None, 'component_id', [], 'Component ID Lexer')
# 
#        # Component lexer
#         comp_to_end_transition = LexerStateTransition('EOS', 0, 0, True, end_state, 'Component to End Transition')
#         comp_id_transition = LexerStateTransition('\[', 0, 1, True, comp_id_state, 'Component to Component ID Transition')
#         comp_token = Token('component', Token.ALWAYS_DATA, True, 'Component Token')
#         comp_state = LexerState([comp_to_end_transition, comp_id_transition], comp_token, False, 'Component State')
#        comp_lexer = Lexer(None, 'component', [], 'Component Lexer')
# 
#        # Source lexer
#         comp_transition = LexerStateTransition('.', 0, -1, False, comp_state, 'Source to Component Transition')
#         source_token = Token('source', Token.NEVER_DATA, False, 'Source Token')
#         source_state = LexerState([comp_transition], source_token, False, 'Source State')
#        source_lexer = Lexer(None, 'source', [], 'Source Lexer')
# 
#        return ((source_lexer, comp_lexer, comp_id_lexer), source_state)
# 
#    def createMsgLexers(self):
#        # End state
#        end_token = Token('end', Token.NEVER_DATA, True, 'End Token')
#        end_state = LexerState([], end_token, True, 'End State')
# 
#        # Sub msg lexer
#         end_transition = LexerStateTransition('EOS', 0, 1, True, end_state, 'Sub Msg to End Transition')
#         sub_msg_token = Token('sub_msg', Token.SOMETIMES_DATA, True, 'Sub Msg Token')
#         sub_msg_state = LexerState([end_transition], sub_msg_token, False, 'Sub Msg State')
#        sub_msg_lexer = Lexer(None, 'sub_msg', [], 'Sub Msg Lexer')
# 
#        # Level lexer
#         level_to_sub_msg_transition = LexerStateTransition('>', 0, 1, True, sub_msg_state, 'Level to Sub Msg Transition')
#         level_token = Token('level', Token.SOMETIMES_DATA, True, 'Level Token')
#         level_state = LexerState([level_to_sub_msg_transition], level_token, False, 'Level State')
#        level_lexer = Lexer(None, 'level', [], 'Level Lexer')
# 
#        # Msg lexer
#         level_transition = LexerStateTransition('[<]', -1, 1, False, level_state, 'Msg to Level Transition')
#         sub_msg_transition = LexerStateTransition('[^<]', -1, 0, False, sub_msg_state, 'Msg to Sub Msg Transition')
#         end_transition = LexerStateTransition('EOS', 0, 1, True, end_state, 'Msg to End Transition')
#        msg_token = Token('msg', Token.NEVER_DATA, False, 'Msg Token')
#         msg_state = LexerState([level_transition, sub_msg_transition, end_transition], msg_token, True, 'Msg State')
#        msg_lexer = Lexer(None, 'msg', [], 'Msg Lexer')
# 
#        return ((msg_lexer, level_lexer, sub_msg_lexer), msg_state)
# 
#    def createEventParser(self):
#        # Sub msg parser
#         sub_msg_parser = StrParser('sub_msg', [], ['sub_msg'], 'Sub Msg Parser')
# 
#        # Level parser
#        level_parser = StrParser('level', [], ['level'], 'Level Parser')
# 
#        # Msg parser
#         msg_parser = Parser('msg', [level_parser, sub_msg_parser], [], 'Msg Parser')
# 
#        # Component id parser
#         component_id_parser = IntParser('component_id', [], ['component_id'], 'Component ID Parser')
# 
#        # Component parser
#         component_parser = StrParser('component', [], ['component'], 'Component Parser')
# 
#        # Source parser
#         source_parser = Parser('source', [component_parser, component_id_parser], [], 'Source Parser')
# 
#        # Datetime parser
#         datetime_parser = DatetimeParser('timestamp', [], ['month', 'day', 'hour', 'minute', 'second'], 'Datetime Parser')
# 
#        # Event parser
#         event_parser = Parser('event', [datetime_parser, source_parser, msg_parser], [], 'Event Parser')
# 
#         parsers = (event_parser, datetime_parser, source_parser, component_parser, component_id_parser,
#                   msg_parser, level_parser, sub_msg_parser)
# 
#        return parsers
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
#===============================================================================
