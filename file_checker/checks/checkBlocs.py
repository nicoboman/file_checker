# -*- coding: utf-8 -*-
import numpy as np
from utils.common import *
from error.datdutErrors import *

class CheckBlocs():
    "check blocs of dut file"
    
    def __init__(self, obj_init):
        self.liste = obj_init.getListe()
        self.line_number = obj_init.getLineNumber()
        self.error_list = []
        self.error_string = ''
            
    def checkBloc(self):
        self.checkMandatoryOrPointlessParameters()
        self.checkIsNumber()

        # if an error occured during check of manadatory parameters
        # do not proceed the other checks (no point doing it because maybe parameter is not defined):
        if len(self.error_list):
            self.error_list.append('line ' + str(self.line_number) + ' error in type/structure of parameters => no additionnal check for this line')
        else:
            self.checkAxis()

        # raises an error if necessary:
        if len(self.error_list):
            while self.error_list:
                try:
                    self.error_string = self.error_string + self.error_list.pop(0) + '\n'
                except IndexError:
                    break
            
            raise BlocError(self.error_string)

    def checkIsNumber(self):
        if not isNumber(self.liste[C_DELAY_OR_STEP_DURATION_COLUMN]):
            self.error_list.append('line ' + str(self.line_number) + ' delay is not a number')

        if not isNumber(self.liste[C_NB_ITEM_OR_FIRST_PATT_NUM]):
            self.error_list.append('line ' + str(self.line_number) + ' first pattern is not a number')

        if not isNumber(self.liste[C_NB_REPET_OR_LAST_PATT_NUM_COLUMN]):
            self.error_list.append('line ' + str(self.line_number) + ' delay is not a number')
                
    def checkAxis(self):
        if self.liste[C_AXIS_COLUMN] not in ['U', 'V', '+U-V', '-U+V']:
            self.error_list.append('line ' + str(self.line_number) + ' invalid axis')
            
    def checkMandatoryOrPointlessParameters(self):
        # check mandatory parameters are mentioned
        # check pointless parameters for square patterns are missing
        bloc_pattern_mask = np.array([True, True, True, True, True, False, False, False, True, True, False, False, False])
                
        # structure of the processed line
        bloc_pattern_presence = np.array(list(map(lambda x: True if len(x) > 0 else False, self.liste)), dtype = bool)
        
        # compare the two of them
        if not np.array_equal(bloc_pattern_mask, bloc_pattern_presence):
            self.error_list.append('line ' + str(self.line_number) + ' mandatory parameter absent or pointless parameter')
