# ------------------------------------------------------
#
#   Element.py
#   By: Fred Stakem
#   Created: 6.20.13
#
# ------------------------------------------------------


# Libs

# User defined
import Utilities

class Element(str):   
    # Setup logging
    logger = Utilities.getLogger(__name__)
    
    # Class constants
    symbol_table = {
                    'eos': 'EOS',
                   }
    
   
    EOS = symbol_table['eos']
            
    
    
    
    