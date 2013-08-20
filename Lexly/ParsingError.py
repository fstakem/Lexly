# ------------------------------------------------------
#
#   ParsingError.py
#   By: Fred Stakem
#   Created: 7.10.13
#
# ------------------------------------------------------


# Libs
# None

# User defined
from Utilities import *
from Corely import Jsonable

# Main
class ParsingError(Jsonable):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
    
    def __init__(self, reason='Unknown', object='None'):
        self.reason = reason
        self.object = object
        
        
    
 
    