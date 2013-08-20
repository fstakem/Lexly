# ------------------------------------------------------
#
#   LexerStateTransition.py
#   By: Fred Stakem
#   Created: 7.8.13
#
# ------------------------------------------------------


# Libs
import re

# User defined
from Utilities import *
from Corely import StateTransition
from Lexly import Element

# Main
class LexerStateTransition(StateTransition):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
    
    def __init__(self, pattern='', end_offset=0, start_offset=0, strip=True, next_state=None, name=__name__):
        super(LexerStateTransition, self).__init__(next_state, name)
        self.pattern = pattern
        self.end_offset = end_offset
        self.start_offset = start_offset
        self.strip = strip
        
    def findMatch(self, stream):
        if stream.atEos():
            if self.pattern == Element.EOS:
                buffer_len = len(stream.element_buffer)
                self.start_offset = 1
                loc = (buffer_len, buffer_len)
                
                return self.getTokenData(stream, loc)
            
            return None
        else:
            buffer_str = ''.join(stream.element_buffer)
            match = re.search(self.pattern, buffer_str)
            
            if match != None:
                return self.getTokenData(stream, match.regs[0])
                
            return None
    
    def getTokenData(self, stream, loc):
        accept_buffer = stream.acceptElements()
        end = loc[0] + self.end_offset
        start = loc[0] + self.start_offset
        token_buffer, stream.element_buffer = self.splitBuffer(accept_buffer, end, start)
        
        return self.getDataFromBuffer(token_buffer)
    
    def splitBuffer(self, buffer, end, start):
        accepted_buffer = []
        remaining_buffer = []
        
        for i, element in enumerate(buffer):
            if i < end:
                accepted_buffer.append(element)
            
            if i >= start:
                remaining_buffer.append(element)
                
        return (accepted_buffer, remaining_buffer)
    
    def getDataFromBuffer(self, buffer):
        data = ''.join(buffer)
        if self.strip:
            data = data.strip()
            
        return data
    
    
    
    
            
        
        
                
    
    
    