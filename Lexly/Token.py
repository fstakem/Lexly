# ------------------------------------------------------
#
#   Token.py
#   By: Fred Stakem
#   Created: 7.8.13
#
# ------------------------------------------------------


# Libs
# None

# User defined
from Utilities import *
from Stream import Stream
from Corely import Jsonable

# Main
class Token(Jsonable):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
    
    # Class constants
    NEVER_DATA = 1
    SOMETIMES_DATA = 2
    ALWAYS_DATA = 3
    
    def __init__(self, data_type='str', data_present=None, atomic=True, data='Token data'):
        self.data_type = data_type
        self.data_present = data_present
        self.atomic = atomic
        self.data = data
        
    def getStream(self):
        if self.atomic:
            return None
        
        return Stream(self.data, self.data_type)
    

    

        
    
 
    