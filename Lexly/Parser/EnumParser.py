# ------------------------------------------------------
#
#   EnumParser.py
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
class EnumParser(Parser):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
    
    def __init__(self, parser_type=None, children=[], token_names=[], name=__name__, acceptable_values=[]):
        super(EnumParser, self).__init__(parser_type, children, token_names, name)
        self.data = None
        self.acceptable_values = [x.lower() for x in acceptable_values]
        
    def parse(self):
        self.getData()
        
        return self.data
        
    def getData(self):
        tokens = self.tokens.values()
        
        if len(tokens) > 0 and tokens[0] != None:
            data = str(tokens[0].data).lower()
            if data in self.acceptable_values:
                self.data = data
            
        return None
        
        
        
        
