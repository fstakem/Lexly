# ------------------------------------------------------
#
#   Parser.py
#   By: Fred Stakem
#   Created: 8.1.13
#
# ------------------------------------------------------


# Libs
from copy import deepcopy
from collections import OrderedDict

# User defined
from Globals import *
from Utilities import *
from Corely import Node
from Corely import Field

# Main
class Parser(Node):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
    
    def __init__(self, parser_type=None, children=[], token_names=[], name=__name__):
        super(Parser, self).__init__(children, name)
        self.parser_type = parser_type
        self.data = None
        self.token_names = token_names
        self.tokens = OrderedDict()
        self.errors = []
        
    def start(self, tokens):
        if globals.debug_parser:
            Parser.logger.debug('Starting parser: %s' % (self.name))
         
        self.reset()   
        unused_tokens = self.setLocalTokens(tokens)
        result = self.parse()
        
        if result != None:
            self.data = result
        
        for child in self.children:
            child.start(unused_tokens)
        
        if globals.debug_parser:
            Parser.logger.debug('Finishing parser: %s' % (self.name))
            
    def reset(self):
        self.data = None
        self.errors = []
        
        for name in self.token_names:
            self.tokens[name] = None
                
    def parse(self):
        pass
    
    def setLocalTokens(self, all_tokens):
        unused_tokens = [] 
        for token in all_tokens:
            if token.data_type in self.tokens:
                self.tokens[token.data_type] = token
            else:
                unused_tokens.append(token)
                
        return unused_tokens
                              
    def getAllErrors(self):
        all_errors = []
        all_errors.extend(self.errors)
        
        for parser in self.children:
            all_errors.extend( parser.getAllErrors() )
            
        return all_errors
    
    def getAllFields(self):
        field = Field(self.data, [], self.parser_type)
        
        for child in self.children:
            field.children.append( child.getAllFields() )
        
        return field
    
    def getAllFlatFields(self):
        all_fields = []
        field = Field(self.data, [], self.parser_type)
    
        all_fields.append(field)
        for child in self.children:
            all_fields.extend( child.getAllFlatFields() )
        
        return all_fields
                
                
            
            
                
                
 
                
                
        
            
            
            
            
            
            
            