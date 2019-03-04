# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.common import *
from error.datdutErrors import *

class CheckBangBangPatterns():
    "check bangbang patterns of dut file"
    
    def __init__(self, obj_init, id_list):
        self.liste = obj_init.getListe()
        self.line_number = obj_init.getLineNumber()
        self.fu_type = obj_init.getFUType()
        self.id_list = id_list
        self.error_list = []
        self.error_string = ''
        
        # Threshold file
        if self.fu_type == 'SR':
            self.threshold_file = C_THRESHOLD_DIR + C_SR_BANGBANG_THRESHOLD_FILE
        elif self.fu_type == 'LL':
            self.threshold_file = C_THRESHOLD_DIR + C_LL_BANGBANG_THRESHOLD_FILE
        elif self.fu_type == 'UL':
            self.threshold_file = C_THRESHOLD_DIR + C_UL_BANGBANG_THRESHOLD_FILE
            
        # set df_threshold
        self.setBangBangPatternThreshold()
        
        # get min, max values
        self.delay_min = (self.df_threshold[self.df_threshold.parameter == 'delay']).iloc[0,1]
        self.delay_max = (self.df_threshold[self.df_threshold.parameter == 'delay']).iloc[0,2]
        self.pos_init_min = (self.df_threshold[self.df_threshold.parameter == 'pos_init']).iloc[0,1]
        self.pos_init_max = (self.df_threshold[self.df_threshold.parameter == 'pos_init']).iloc[0,2]
        self.pos_target_min = (self.df_threshold[self.df_threshold.parameter == 'pos_target']).iloc[0,1]
        self.pos_target_max = (self.df_threshold[self.df_threshold.parameter == 'pos_target']).iloc[0,2]
        self.slope_value_min = (self.df_threshold[self.df_threshold.parameter == 'slope_value']).iloc[0,1]
        self.slope_value_max = (self.df_threshold[self.df_threshold.parameter == 'slope_value']).iloc[0,2]
        
        print(self.liste)
        
    def checkBangBangPattern(self):
        self.checkMandatoryOrPointlessParameters()
        self.checkIsNumber()

        # if an error occured during check of manadatory parameters
        # do not proceed the other checks (no point doing it because maybe parameter is not defined):
        if len(self.error_list):
            self.error_list.append('line ' + str(self.line_number) + ' error in type/structure of parameters => no additionnal check for this line')
        else:
            self.checkBangBangPatternIDsUnique()
            self.checkDelay()
            self.checkPosTarget()
            self.checkSlope()
            self.checkOffset()
            self.check600HzCommand()

        # raises an error if necessary:
        if len(self.error_list):
            while self.error_list:
                try:
                    self.error_string = self.error_string + self.error_list.pop(0) + '\n'
                except IndexError:
                    break
            
            raise BangBangPatternsError(self.error_string)
    
    def checkBangBangPatternIDsUnique(self):
        if self.liste[C_ID_COLUMN] in self.id_list:
            self.error_list.append('line ' + str(self.line_number) + ' bangbang pattern ids are not unique.')
        else:
            self.id_list.append(self.liste[C_ID_COLUMN])

    def checkDelay(self):
        if float(self.liste[C_DELAY_OR_STEP_DURATION_COLUMN]) < self.delay_min:
            self.error_list.append('line ' + str(self.line_number) + ' delay < min')
        elif float(self.liste[C_DELAY_OR_STEP_DURATION_COLUMN]) > self.delay_max:
            self.error_list.append('line ' + str(self.line_number) + ' delay > max')
            
    def checkOffset(self):
        if float(self.liste[C_OFFSET_COLUMN]) < self.pos_init_min:
            self.error_list.append('line ' + str(self.line_number) + ' offset < min')
        elif float(self.liste[C_OFFSET_COLUMN]) > self.pos_init_max:
            self.error_list.append('line ' + str(self.line_number) + ' offset > max')
            
    def checkPosTarget(self):
        if float(self.liste[C_AMPL_OR_STEP_INC_OR_FINAL_POS1_COLUMN]) < self.pos_target_min:
            self.error_list.append('line ' + str(self.line_number) + ' pos target < min')
        elif float(self.liste[C_AMPL_OR_STEP_INC_OR_FINAL_POS1_COLUMN]) > self.pos_target_max:
            self.error_list.append('line ' + str(self.line_number) + ' pos target > max')
    
    def checkSlope(self):
        if float(self.liste[C_SLOPE_COLUMN]) < self.slope_value_min:
            self.error_list.append('line ' + str(self.line_number) + ' slope < min')
        elif float(self.liste[C_SLOPE_COLUMN]) > self.slope_value_max:
            self.error_list.append('line ' + str(self.line_number) + ' slope > max')
            
    def checkMandatoryOrPointlessParameters(self):
        # check mandatory parameters are mentioned
        # check pointless parameters for bangbang patterns are missing
        bangbang_pattern_mask = np.array([True, True, True, True, False, True, True, True, False, False, False, True, False])
                
        # structure of the processed line
        bangbang_pattern_presence = np.array(list(map(lambda x: True if len(x) > 0 else False, self.liste)), dtype = bool)
        
        # compare the two of them
        if not np.array_equal(bangbang_pattern_mask, bangbang_pattern_presence):
            self.error_list.append('line ' + str(self.line_number) + ' mandatory parameter absent or pointless parameter')

    def check600HzCommand(self):
        # for patterns != sinus, 600Hz parameter must always be set to FALSE:
        if self.liste[C_IS_600HZ_CMD_COLUMN] != 'FALSE':
            self.error_list.append('line ' + str(self.line_number) + ' invalid 600Hz parameter: must be FALSE for bangbang patterns')

    def checkIsNumber(self):
        if not isNumber(self.liste[C_DELAY_OR_STEP_DURATION_COLUMN]):
            self.error_list.append('line ' + str(self.line_number) + ' step duration is not a number')
            
        if not isNumber(self.liste[C_OFFSET_COLUMN]):
            self.error_list.append('line ' + str(self.line_number) + ' offset is not a number')

        if not isNumber(self.liste[C_AMPL_OR_STEP_INC_OR_FINAL_POS1_COLUMN]):
            self.error_list.append('line ' + str(self.line_number) + ' step increment is not a number')
            
        if not isNumber(self.liste[C_SLOPE_COLUMN]):
            self.error_list.append('line ' + str(self.line_number) + ' slope is not a number')

    def setBangBangPatternThreshold(self):
        with open (self.threshold_file,'r',encoding='utf8') as self.threshold_file_handler:                
            # Creation of df_threshold data frame:
            self.df_threshold = pd.read_csv(self.threshold_file, sep=C_SEPARATOR, comment=C_COMMENT, header = 0, skip_blank_lines=True)
