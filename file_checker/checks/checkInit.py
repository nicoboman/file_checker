# -*- coding: utf-8 -*-
import pandas as pd
from utils.common import *
from error.datdutErrors import *

class CheckInit:
    
    "process init checks of dut file"
    
    def __init__(self, liste, line_number):
        self.liste = liste
        self.line_number = line_number
        self.error_flag = False
        self.error_list = []
        self.error_string = ''
        
    def checkInit(self):
        # elementary checks on the structure of line, definition and type
        if len(self.liste) != C_NB_OF_FIELD:
            self.error_flag = True
            self.error_list.append('[Initial Checks Error] invalid number of fields')
        elif self.liste[C_DEFINITION_COLUMN] not in ['PATTERN', 'BLOC', 'FDIR']:
            self.error_flag = True
            self.error_list.append('\n[Initial Checks Error] invalid definition')
        elif self.liste[C_TYPE_COLUMN] not in ['SINUS', 'SQUARE', 'TRAPEZOID', 'BANGBANG', 'CORRIDOR', 'BEHAVIOUR']:
            self.error_flag = True
            self.error_list.append('\n[Initial Checks Error] invalid type')
        # check if id is an integer and is >= 0:
        elif not self.liste[C_ID_COLUMN].isdigit():
            self.error_flag = True
            self.error_list.append('\n[Initial Checks Error] ID is not a positive integer')
        
        # raises an error if necessary:
        if self.error_flag:
            while self.error_list:
                try:
                    self.error_string = self.error_string + self.error_list.pop(0)
                except IndexError:
                    break
                    
            raise InitialChecksError(self.error_string, self.line_number)
