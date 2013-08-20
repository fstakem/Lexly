# ------------------------------------------------------
#
#   DatetimeParser.py
#   By: Fred Stakem
#   Created: 8.5.13
#
# ------------------------------------------------------


# Libs
from copy import deepcopy
from datetime import datetime

# User defined
from Globals import *
from Utilities import *
from Parser import Parser
from Lexly import ParsingError

# Main
class DatetimeParser(Parser):
    
    # Setup logging
    logger = Utilities.getLogger(__name__)
    
    MONTH = { 
              'jan' : 1, 
              'feb' : 2, 
              'mar' : 3,
              'apr' : 4,
              'may' : 5, 
              'jun' : 6,
              'jul' : 7,
              'aug' : 8,
              'sep' : 9,
              'oct' : 10,
              'nov' : 11,
              'dec' : 12
            }
    
    DEFAULT_YEAR = 2013
    DEFAULT_MONTH = 1
    DEFAULT_DAY = 1
    DEFAULT_HOUR = 0
    DEFAULT_MINUTE = 0
    DEFAULT_SECOND = 0
    DEFAULT_MICROSECOND = 0
    
    def __init__(self, parser_type=None, children=[], token_names=[], name=__name__):
        super(DatetimeParser, self).__init__(parser_type, children, token_names, name)
        self.year = DatetimeParser.DEFAULT_YEAR
        self.month = DatetimeParser.DEFAULT_MONTH
        self.day = DatetimeParser.DEFAULT_DAY
        self.hour = DatetimeParser.DEFAULT_HOUR
        self.minute = DatetimeParser.DEFAULT_MINUTE
        self.second = DatetimeParser.DEFAULT_SECOND
        self.microsecond = DatetimeParser.DEFAULT_MICROSECOND
        
    def parse(self):
        num_errors = len(self.errors)
        self.getYear()
        self.getMonth()
        self.getDay()
        self.getHour()
        self.getMinute()
        self.getSecond()
        self.getMicrosecond()
        
        if len(self.errors) > num_errors:
            return None
        
        dt = datetime(year=self.year, month=self.month, day=self.day,
                      hour=self.hour, minute=self.minute, second=self.second,
                      microsecond=self.microsecond)
        
        return dt
            
    def getYear(self):
        if 'year' in self.tokens:
            year = self.tokens['year']
            if year != None:
                self.year = int( year.data )
        
    def getMonth(self):
        if 'month' in self.tokens:
            month = self.tokens['month'].data
            if month != None:
                if month.isalpha():
                    month = month.lower()
                    
                    if month in DatetimeParser.MONTH:
                        self.month = DatetimeParser.MONTH[month]
                    else:
                        error = ParsingError('Cannot parse the month.', deepcopy(self))
                        self.errors.append(error)
                else:
                    month = self.tokens['month'].data.lstrip('0')
                    if month > 0 and month <= 12:
                        self.month = month
            
    def getDay(self):
        if 'day' in self.tokens:
            day = self.tokens['day']
            if day != None:
                self.day = int( day.data )
        
    def getHour(self):
        if 'hour' in self.tokens:
            hour = self.tokens['hour']
            if hour != None:
                self.hour = int( hour.data )
    
    def getMinute(self):
        if 'minute' in self.tokens:
            minute = self.tokens['minute']
            if minute != None:
                self.minute = int( minute.data )
    
    def getSecond(self):
        if 'second' in self.tokens:
            second = self.tokens['second']
            if second != None:
                self.second = int( second.data )
    
    def getMicrosecond(self):
        if 'millisecond' in self.tokens:
            millisecond = self.tokens['millisecond']
            if millisecond != None:
                self.microsecond = int( millisecond.data ) * 1000
        
        
        
  
                
        
    
    
    
        
        
        
        
        