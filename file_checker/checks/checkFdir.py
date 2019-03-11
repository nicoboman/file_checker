'''
Created on 10 mars 2019

@author: nicolas
'''
import numpy as np
from error.datdutErrors import *
from utils.common import *

class CheckFDIR(object):
    '''
    Fdir checks
    '''

    def __init__(self, obj_init):
        '''
        Constructor
        '''
        self.liste = obj_init.getListe()
        self.line_number = obj_init.getLineNumber()
        self.fu_type = obj_init.getFUType()
        self.error_list = []
        self.error_string = ''
        
    def checkFdir(self):
        # corridor
        if self.liste[C_TYPE_COLUMN] == 'CORRIDOR':
            self.checkCorridor()
            self.checkAxis()
        # behaviour
        else:
            self.checkBehaviour(self.fu_type)
        
        # raises an error if necessary:
        if len(self.error_list):
            while self.error_list:
                try:
                    self.error_string = self.error_string + self.error_list.pop(0) + '\n'
                except IndexError:
                    break
            # remove last line jump
            self.error_string = self.error_string[:-1]
            
            raise FdirError(self.error_string)        
    
    def checkCorridor(self):
        self.checkMandatoryOrPointlessParameters('CORRIDOR')
        
    def checkBehaviour(self, FU):
        self.checkMandatoryOrPointlessParameters('BEHAVIOUR', self.fu_type)
    
    def checkMandatoryOrPointlessParameters(self, fdir_type, fu='UNDEF'):
        if fdir_type == 'CORRIDOR':
            # mask to match with
            self.fdir_corridor_mask = np.array([True, True, False, False, True, False, False, False, False, False, True, True, True])
            
            # structure of the processed line
            self.fdir_corridor_parameter_presence = np.array(list(map(lambda x: True if len(x) > 0 else False, self.liste)), dtype = bool)
            
            # compare the two of them
            if not np.array_equal(self.fdir_corridor_mask, self.fdir_corridor_parameter_presence):
                self.error_list.append('line ' + str(self.line_number) + ' fdir corridor: mandatory parameter absent or pointless parameter')
        elif fdir_type == 'BEHAVIOUR' and fu != 'LL':
            # mask to match with
            self.fdir_behaviour_mask = np.array([True, True, False, False, False, False, False, False, False, False, True, True, True])
            
            # structure of the processed line
            self.fdir_behaviour_parameter_presence = np.array(list(map(lambda x: True if len(x) > 0 else False, self.liste)), dtype = bool)
            
            # compare the two of them
            if not np.array_equal(self.fdir_behaviour_mask, self.fdir_behaviour_parameter_presence):
                self.error_list.append('line ' + str(self.line_number) + ' fdir behaviour: mandatory parameter absent or pointless parameter')
        elif fdir_type == 'BEHAVIOUR' and fu == 'LL':
            # mask to match with
            self.fdir_behaviour_ll_mask = np.array([True, True, False, False, False, False, False, False, False, False, True, True, False])
            
            # structure of the processed line
            self.fdir_behaviour_ll_parameter_presence = np.array(list(map(lambda x: True if len(x) > 0 else False, self.liste)), dtype = bool)
            
            # compare the two of them
            if not np.array_equal(self.fdir_behaviour_ll_mask, self.fdir_behaviour_ll_parameter_presence):
                self.error_list.append('line ' + str(self.line_number) + ' fdir behaviour LL: mandatory parameter absent or pointless parameter')

    def checkAxis(self):
        if self.liste[C_AXIS_COLUMN] not in ['U', 'V', '+U+V']:
            self.error_list.append('line ' + str(self.line_number) + ' invalid axis')
