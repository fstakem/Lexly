# ------------------------------------------------------
#
#   JsonImporter.py
#   By: Fred Stakem
#   Created: 8.22.13
#
# ------------------------------------------------------


# Libs
# None

# User defined
from Globals import *
from Utilities import *

from Lexly import RawEventSeparator
from Lexly import Token
from Lexly import ParsingError

from Lexly.Lexer import Lexer
from Lexly.Lexer import LexerState
from Lexly.Lexer import LexerStateTransition

from Lexly.Parser import Parser
from Lexly.Parser import StrParser
from Lexly.Parser import IntParser
from Lexly.Parser import DatetimeParser
from Lexly.Parser import EnumParser

# Main
class JsonImporter(object):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
     
    @classmethod    
    def importParser(cls, json_data):
        name = json_data['name']
        created = json_data['created']
        author = json_data['author']
        
        separator_json = json_data['raw_event_separator']
        separator = cls.constructSeparator(separator_json)
        
        lexer_states_json = json_data['lexer_states']
        lexer_states = cls.constructLexerStates(lexer_states_json)
        
        lexers_json = json_data['lexers']
        lexer = cls.constructLexers(lexers_json, lexer_states)
        
        parsers_json = json_data['parsers']
        parser = cls.constructParsers(parsers_json)
        
        return (name, created, author, separator, lexer, parser)
        
    @classmethod
    def constructSeparator(cls, separator_json):
        name = separator_json['name']
        separator = separator_json['separator']
        
        return RawEventSeparator(separator, name)
    
    @classmethod
    def constructLexerStates(cls, states_json):
        states = []
        for state_json in states_json:
            states.append( cls.contructLexerState(state_json) )
            
        cls.setNextStates(states)
            
        return states
    
    @classmethod
    def contructLexerState(cls, state_json):
        name = state_json['name']
        final_state = cls.getBoolean( state_json['final_state'] )
        
        # Token
        token_json = state_json['token']
        token = cls.contructToken(token_json)
        
        # Transitions
        transition_table = []
        transitions_json = state_json['transitions']
        for transition_json in transitions_json:
            transition = cls.contructTransition(transition_json)
            transition_table.append(transition)
            
        return LexerState(transition_table, token, final_state, name)
    
    @classmethod
    def contructToken(cls, token_json):
        token_type = token_json['data_type']
            
        data_aval = token_json['data'].lower()
        if data_aval == 'always':
            data_aval = Token.ALWAYS_DATA
        elif data_aval == 'sometimes':
            data_aval = Token.SOMETIMES_DATA
        elif data_aval == 'never':
            data_aval = Token.NEVER_DATA
        else:
            raise SyntaxError('Data availability not found.')
        
        atomic = cls.getBoolean( token_json['atomic'] )
        
        return Token(token_type, data_aval, atomic, '')

    @classmethod
    def contructTransition(cls, transition_json):
        name = transition_json['name']
        pattern = transition_json['pattern']
        end_offset = transition_json['end_offset']
        start_offset = transition_json['start_offset']
        strip = cls.getBoolean( transition_json['strip'] )    
        next_state = transition_json['next_state']
    
        return LexerStateTransition(pattern, end_offset, start_offset, strip, next_state, name)
    
    @classmethod
    def setNextStates(cls, states):
        for state in states:
            for transition in state.transition_table:
                next_state_name = transition.next_state
                
                if next_state_name == 'end':
                    end_token = Token('end', Token.NEVER_DATA, True, 'End Token')
                    end_state = LexerState([], end_token, True, 'End State')
                    transition.next_state = end_state
                else:
                    for inner_state in states:
                        if next_state_name == inner_state.name:
                            transition.next_state = inner_state
                            break
        
    @classmethod
    def constructLexers(cls, lexers_json, states):
        root_lexer = None
        all_lexers = []
        
        for lexer_json in lexers_json:
            lexer, root = cls.constructLexer(lexer_json)
            all_lexers.append(lexer)
            
            if root:
                root_lexer = lexer
        
        cls.addStartStateToLexers(all_lexers, states)        
        cls.setSubLexers(all_lexers)
        
        return root_lexer
    
    @classmethod
    def constructLexer(cls, lexer_json):
        # Lexer
        lexer_name = lexer_json['name']
        lexer_type = lexer_json['lexer_type']
        sub_lexers = lexer_json['sub_lexers']
        start_state = lexer_json['start_state']
        root = cls.getBoolean( lexer_json['root'] )
        
        lexer = Lexer(start_state, lexer_type, sub_lexers, lexer_name)
        
        return (lexer, root)
    
    @classmethod
    def addStartStateToLexers(cls, lexers, states):
        for lexer in lexers:
            start_state_name = lexer.start_state
            
            if start_state_name == "":
                lexer.start_state = None
            else:
                for state in states:
                    if start_state_name == state.name:
                        lexer.start_state = state
                        break
    
    @classmethod
    def setSubLexers(cls, lexers):
        for lexer in lexers:
            children = lexer.children[:]
            lexer.children = []
            for child in children:
                for inner_lexer in lexers:
                    if child == inner_lexer.lexer_type:
                        lexer.children.append(inner_lexer)
                        break
       
    @classmethod
    def constructParsers(cls, parsers_json):
        root_parser = None
        parsers = []
        for parser_json in parsers_json:
            parser, root = cls.constructParser(parser_json)
            parsers.append(parser)
            
            if root:
                root_parser = parser
                
        cls.setSubParsers(parsers)
            
        return root_parser
    
    @classmethod
    def constructParser(cls, parser_json):
        name = parser_json['name']
        parser_type = parser_json['parser_type']
        parser_class = parser_json['parser_class']
        sub_parsers = parser_json['sub_parsers']
        token_names = parser_json['token_names']
        root = cls.getBoolean( parser_json['root'] )
        #acceptable_values = parser_json['acceptable_values']
        acceptable_values = ''
        
        parser = None
        if parser_class.lower() == 'parser':
            parser = Parser(parser_type, sub_parsers, token_names, name)
        elif parser_class.lower() == 'strparser':
            parser = StrParser(parser_type, sub_parsers, token_names, name)
        elif parser_class.lower() == 'intparser':
            parser = IntParser(parser_type, sub_parsers, token_names, name)
        elif parser_class.lower() == 'datetimeparser':
            parser = DatetimeParser(parser_type, sub_parsers, token_names, name)
        elif parser_class.lower() == 'enumparser':
            parser = EnumParser(parser_type, sub_parsers, token_names, name, acceptable_values)
        else:
            raise SyntaxError('No parser found for the class specified.')
        
        return (parser, root)
    
    @classmethod
    def setSubParsers(cls, parsers):
        for parser in parsers:
            children = parser.children[:]
            parser.children = []
            
            for child in children:
                for inner_parser in parsers:
                    if child == inner_parser.parser_type:
                        parser.children.append(inner_parser)
                        break
                    
    @classmethod
    def getBoolean(cls, value):
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        
        raise SyntaxError('Boolean value is incorrect.')
        
        
        
        
        
        
        