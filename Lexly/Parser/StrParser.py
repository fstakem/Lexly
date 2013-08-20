# ------------------------------------------------------
#
#   StrParser.py
#   By: Fred Stakem
#   Created: 8.6.13
#
# ------------------------------------------------------


# Libs
from copy import deepcopy

# User defined
from Globals import *
from Utilities import *
from Parser import Parser
from Lexly import ParsingError

# Main
class StrParser(Parser):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
    
    DEFAULT_SEPARATOR = ' '
    
    def __init__(self, parser_type=None, children=[], token_names=[], name=__name__):
        super(StrParser, self).__init__(parser_type, children, token_names, name)
        self.data = None
        
    def parse(self):
        self.getData()
        
        return self.data
        
    def getData(self):
        tokens = self.tokens.values()
        
        if len(tokens) > 1:
            self.data = ''
            for i, token in enumerate(tokens):
                self.data += str(token.data)
                
                if i < len(tokens) - 1:
                    self.data += StrParser.DEFAULT_SEPARATOR
        elif len(tokens) > 0 and tokens[0] != None:
            self.data = str(tokens[0].data)
        
        
        
        
        
        
