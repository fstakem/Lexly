# ------------------------------------------------------
#
#   Lexer.py
#   By: Fred Stakem
#   Created: 7.8.13
#
# ------------------------------------------------------


# Libs
from copy import deepcopy

# User defined
from Globals import *
from Utilities import *

from Lexly import Element
from Lexly import Stream
from Lexly import ParsingError
from Lexly import Token

from Corely import State
from Corely import StateMachine
from Corely import StateMachineNode

# Main
class Lexer(StateMachineNode):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
    
    def __init__(self, start_state=None, lexer_type=None, children=[], name=__name__):
        super(Lexer, self).__init__(start_state, name, children)
        self.lexer_type = lexer_type
        self.token = None
        self.sub_tokens = []
        self.errors = []
        
    def start(self, token):
        if globals.debug_lexer:
            Lexer.logger.debug('Starting lexer: %s' % (self.name))
            
        self.token = token
        super(Lexer, self).start(self.token.getStream())
        
        if self.stream == None:
            return
        
        if globals.debug_lexer:
            Lexer.logger.debug('Lexing stream:\n%s' % (self.stream.to_pretty_json()))
        
        self.reset()
        self.findAllTokens()
        
        if globals.debug_lexer:
            Lexer.logger.debug('Finishing lexer: %s' % (self.name))
                
    def findAllTokens(self):
        while 1:
            current_element = self.stream.getNextElement()
            
            while current_element.isspace():
                next_element = self.stream.peek()
                
                if next_element.isspace():
                    current_element = self.stream.getNextElement()
                    
                    if globals.debug_lexer:    
                        Lexer.logger.debug('Current lexer element: %s' % current_element)
                else:
                    break
                
            if globals.debug_lexer:    
                Lexer.logger.debug('Current lexer element: %s' % current_element)
            
            if current_element == Element.EOS:
                self.handleEndOfStream()
                break
            else:
                self.handleNewData()
                
        self.findNestedTokens()
                
    def findNestedTokens(self):
        for sub_token in self.sub_tokens:
            if globals.debug_lexer:
                Lexer.logger.debug('Finding nested tokens for token: %s' % (sub_token.data_type))
             
            if sub_token.atomic or sub_token.data_present == Token.NEVER_DATA:  
                continue
            
            sub_lexer = None 
            for lexer in self.children:
                if sub_token.data_type == lexer.lexer_type: 
                    sub_lexer = lexer
                    break
             
            if sub_lexer != None:
                sub_lexer.start(sub_token)
            else:
                error = ParsingError('No lexer found for the token.', deepcopy(self))
                self.logger.error(error.to_pretty_json())
                self.errors.append(error)   
                  
    def reset(self):
        if len(self.children) != 0:
            super(Lexer, self).reset()
            
        for lexer in self.children:
            lexer.reset()
            
        self.sub_tokens = []
        self.errors = []
                    
    def handleEndOfStream(self):
        if globals.debug_lexer:    
                Lexer.logger.debug('Current buffer: %s' % ''.join(self.stream.element_buffer))
                
        if not self.current_state.isFinalState():
            error = ParsingError('End of the stream reached before the state machine had completed.', deepcopy(self))
            self.logger.error(error.to_pretty_json())
            self.errors.append(error)
        
    def handleNewData(self):
        if globals.debug_lexer:    
                Lexer.logger.debug('Current buffer: "%s"' % ''.join(self.stream.element_buffer))
                
        next_state, sub_token = self.current_state.nextState(self.stream)
        
        if self.current_state != next_state:
            self.appendToken(sub_token)
            self.changeState(next_state)
            
    def appendToken(self, sub_token):
        if len(sub_token.data) == 0 and sub_token.data_present == Token.ALWAYS_DATA:
            error = ParsingError('No data found in the token.', deepcopy(self))
            self.logger.error(error.to_pretty_json())
            self.errors.append(error)
        elif len(sub_token.data) > 0 and sub_token.data_present == Token.NEVER_DATA:
            error = ParsingError('Token has data when specified not to.', deepcopy(self))
            self.logger.error(error.to_pretty_json())
            self.errors.append(error)
        elif sub_token.data_present == Token.NEVER_DATA:
            if globals.debug_lexer:
                Lexer.logger.debug('Found token:\n%s' % (sub_token.to_pretty_json()))
        else:
            if globals.debug_lexer:
                Lexer.logger.debug('Found token:\n%s' % (sub_token.to_pretty_json()))
                
            self.sub_tokens.append(sub_token)
            
    def getAllErrors(self):
        all_errors = []
        all_errors.extend(self.errors)
        
        for lexer in self.children:
            all_errors.extend( lexer.getAllErrors() )
            
        return all_errors
    
    def getAllTokens(self):
        all_tokens = []
        
        for token in self.sub_tokens:
            if token.atomic == True:
                all_tokens.append(token)
                
        for child in self.children:
            all_tokens.extend(child.getAllTokens())
                
        return all_tokens

    

    
    
    
    
    