# ------------------------------------------------------
#
#   LexerState.py
#   By: Fred Stakem
#   Created: 7.8.13
#
# ------------------------------------------------------


# Libs
# None

# User defined
from Utilities import *
from Lexly import Token
from Corely import State

# Main
class LexerState(State):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
    
    def __init__(self, transition_table=[], token=None, final_state=True, name=__name__):
        super(LexerState, self).__init__(transition_table, name)
        self.token = token
        self.final_state = final_state
        
    def nextState(self, stream):
        next_state = self
        
        for transition in self.transition_table:
            token_data = transition.findMatch(stream)
            
            if token_data != None:
                next_state = transition.next_state
                self.token.data = token_data
                break
        
        return (next_state, self.token)
    
    def enterState(self):
        super(LexerState, self).enterState()
    
    def exitState(self):
        super(LexerState, self).exitState()
        
    def isFinalState(self):
        return self.final_state
           

            
    
    
    