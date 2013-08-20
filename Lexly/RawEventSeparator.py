# ------------------------------------------------------
#
#   RawEventSeparator.py
#   By: Fred Stakem
#   Created: 6.19.13
#
# ------------------------------------------------------


# Libs
# None

# User defined
from Utilities import *
from Element import Element
from Stream import Stream
from Corely import Jsonable

# Main
class RawEventSeparator(Jsonable):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
    
    def __init__(self, separator='\n', name=__name__):
        self.name = name
        self.separator = separator
        
    def seperateEvents(self, data=None):
        raw_events = []
        
        if data == None:
            return raw_events
        
        raw_events = data.split(self.separator)
        filtered_events = []
        
        for event in raw_events:
            if len(event) != 0:
                filtered_events.append(event)
                
        return filtered_events
    
 
    
    
    
    