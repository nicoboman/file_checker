# -*- coding: utf-8 -*-
from utils.common import *
from error.datdutErrors import *

class CheckInit(object):
    "process init checks of dut file"
    
    def __init__(self, liste, line_number, fu_type):
        self.liste = liste
        self.line_number = line_number
        self.fu_type = fu_type
        self.error_list = []
        self.error_string = ''
        
    def checkInit(self):
        # elementary checks on the structure of line, definition and type
        if len(self.liste) != C_NB_OF_FIELD:
            self.error_list.append('line ' + str(self.line_number) + ' invalid number of fields')
            
        if self.liste[C_DEFINITION_COLUMN] not in ['PATTERN', 'BLOC', 'FDIR']:
            self.error_list.append('line ' + str(self.line_number) + ' invalid definition')
            
        if self.liste[C_TYPE_COLUMN] not in ['SINUS', 'SQUARE', 'TRAPEZOID', 'BANGBANG', 'CORRIDOR', 'BEHAVIOUR']:
            self.error_list.append('line ' + str(self.line_number) + ' invalid type')
            
        # check if id is an integer and is >= 0:
        if not self.liste[C_ID_COLUMN].isdigit() and self.liste[C_DEFINITION_COLUMN] != 'FDIR':
            self.error_list.append('line ' + str(self.line_number) + ' ID is not a positive integer')
        
        # raises an error if necessary:
        if len(self.error_list):
            while self.error_list:
                try:
                    self.error_string = self.error_string + self.error_list.pop(0) + '\n'
                except IndexError:
                    break
            # remove last line jump
            self.error_string = self.error_string[:-1]
            
            raise InitialChecksError(self.error_string, self.line_number)
    
    def getType(self):
        return self.liste[C_TYPE_COLUMN]
    
    def getDefinition(self):
        return self.liste[C_DEFINITION_COLUMN]
    
    def getListe(self):
        return self.liste

    def getLineNumber(self):
        return self.line_number
    
    def getFUType(self):
        return self.fu_type
