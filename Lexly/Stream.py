# ------------------------------------------------------
#
#   Stream.py
#   By: Fred Stakem
#   Created: 6.20.13
#
# ------------------------------------------------------


# Libs
# None

# User defined
from Utilities import *
from Element import Element
from Corely import Jsonable

# Main
class Stream(Jsonable):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
    
    def __init__(self, source=[], name=__name__):
        self.name = name
        self.source = source
        self.reset()
        
    def reset(self):
        self.element_buffer = []
        self.current_element = None
        self.start_position = -1
        self.current_position = -1
        
    def atEos(self):
        if self.current_position >= len(self.source) - 1:
            return True
        
        return False
    
    def acceptElementRange(self, start, end):
        tmp_buffer = []
        accept_buffer = []
        
        for i, element in enumerate(self.element_buffer):
            if i < start:
                tmp_buffer.append(element)
            elif i > end:
                tmp_buffer.append(element)
            else:
                accept_buffer.append(element)
            
        self.element_buffer = tmp_buffer
        self.current_element = None
        self.start_position = self.current_position
            
        return accept_buffer
    
    def acceptAllElements(self):
        start = 0
        end = len(self.element_buffer)
        
        self.acceptElementRange(start, end)
    
    def acceptElements(self):
        buffer = self.element_buffer
        self.element_buffer = []
        self.current_element = None
        self.start_position = self.current_position
        
        return buffer
    
    def flushElementRange(self, start, end):
        tmp_buffer = []
        
        for i, element in enumerate(self.element_buffer):
            if i < start:
                tmp_buffer.append(element)
            elif i > end:
                tmp_buffer.append(element)
            
        self.element_buffer = tmp_buffer
        self.current_element = None
        self.start_position = self.current_position
            
        return self.element_buffer
    
    def flushElements(self):
        self.element_buffer = []
        self.current_element = None
        self.start_position = self.current_position
        
        return self.element_buffer
        
    def getNextElement(self):
        next_position = self.current_position + 1
        try:
            self.current_element = self.source[next_position]
            self.current_position = next_position
        except IndexError:
            return Element.EOS
        
        self.element_buffer.append(self.current_element)
        
        return self.current_element
    
    def getAllElements(self):
        for element in self.source:
            self.getNextElement()
            
        return ''.join(self.element_buffer)
    
    def peek(self):
        next_pos = self.current_position + 1
        try:
            element = self.source[next_pos]
        except IndexError:
            return Element.EOS
        
        return element
    
    
    
    