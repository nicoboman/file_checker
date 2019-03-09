# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.common import *
from error.datdutErrors import *

class CheckTrapezoidPatterns():
    "check trapezoid patterns of dut file"
    
    def __init__(self, obj_init):
        self.liste = obj_init.getListe()
        self.line_number = obj_init.getLineNumber()
        self.fu_type = obj_init.getFUType()
        self.error_list = []
        self.error_string = ''
        
        # Threshold file
        if self.fu_type == 'SR':
            self.threshold_file = C_THRESHOLD_DIR + C_SR_TRAPEZOID_THRESHOLD_FILE
        elif self.fu_type == 'LL':
            self.threshold_file = C_THRESHOLD_DIR + C_LL_TRAPEZOID_THRESHOLD_FILE
        elif self.fu_type == 'UL':
            self.threshold_file = C_THRESHOLD_DIR + C_UL_TRAPEZOID_THRESHOLD_FILE
            
        # set df_threshold
        self.setTrapezoidPatternThreshold()
        
        # get min, max values
        self.pos_init_min = (self.df_threshold[self.df_threshold.parameter == 'pos_init']).iloc[0,1]
        self.pos_init_max = (self.df_threshold[self.df_threshold.parameter == 'pos_init']).iloc[0,2]
        self.pos_target1_min = (self.df_threshold[self.df_threshold.parameter == 'pos_target1']).iloc[0,1]
        self.pos_target1_max = (self.df_threshold[self.df_threshold.parameter == 'pos_target1']).iloc[0,2]
        self.pos_target2_min = (self.df_threshold[self.df_threshold.parameter == 'pos_target2']).iloc[0,1]
        self.pos_target2_max = (self.df_threshold[self.df_threshold.parameter == 'pos_target2']).iloc[0,2]
        self.step_duration_min = (self.df_threshold[self.df_threshold.parameter == 'step_duration']).iloc[0,1]
        self.step_duration_max = (self.df_threshold[self.df_threshold.parameter == 'step_duration']).iloc[0,2]
        self.slope_value_min = (self.df_threshold[self.df_threshold.parameter == 'slope_value']).iloc[0,1]
        self.slope_value_max = (self.df_threshold[self.df_threshold.parameter == 'slope_value']).iloc[0,2]
        self.inter_gap_duration_min = (self.df_threshold[self.df_threshold.parameter == 'inter_gap_duration']).iloc[0,1]
        self.inter_gap_duration_max = (self.df_threshold[self.df_threshold.parameter == 'inter_gap_duration']).iloc[0,2]
            
    def checkTrapezoidPattern(self):
        self.checkMandatoryOrPointlessParameters()
        self.checkIsNumber()

        # if an error occured during check of manadatory parameters
        # do not proceed the other checks (no point doing it because maybe parameter is not defined):
        if len(self.error_list):
            self.error_list.append('line ' + str(self.line_number) + ' error in type/structure of parameters => no additionnal check for this line')
        else:
            self.checkSlope()
            self.checkStepDuration()
            self.checkIntervalDuration()
            self.checkPosInit()
            self.checkPosTarget(1)
            self.checkPosTarget(2)
            self.check600HzCommand()

        # raises an error if necessary:
        if len(self.error_list):
            while self.error_list:
                try:
                    self.error_string = self.error_string + self.error_list.pop(0) + '\n'
                except IndexError:
                    break
            
            raise TrapezoidPatternsError(self.error_string)

    def checkSlope(self):
        if float(self.liste[C_SLOPE_COLUMN]) < self.slope_value_min:
            self.error_list.append('line ' + str(self.line_number) + ' slope < min')
        elif float(self.liste[C_SLOPE_COLUMN]) > self.slope_value_max:
            self.error_list.append('line ' + str(self.line_number) + ' slope > max')

    def checkStepDuration(self):
        if float(self.liste[C_DELAY_OR_STEP_DURATION_COLUMN]) < self.step_duration_min:
            self.error_list.append('line ' + str(self.line_number) + ' step duration < min')
        elif float(self.liste[C_DELAY_OR_STEP_DURATION_COLUMN]) > self.step_duration_max:
            self.error_list.append('line ' + str(self.line_number) + ' step duration > max')
            
    def checkIntervalDuration(self):
        if float(self.liste[C_INTERVAL_DURATION_COLUMN]) < self.inter_gap_duration_min:
            self.error_list.append('line ' + str(self.line_number) + ' interval duration < min')
        elif float(self.liste[C_INTERVAL_DURATION_COLUMN]) > self.inter_gap_duration_max:
            self.error_list.append('line ' + str(self.line_number) + ' interval duration > max')
            
    def checkMandatoryOrPointlessParameters(self):
        # check mandatory parameters are mentioned
        # check pointless parameters for trapezoid patterns are missing
        trapezoid_pattern_mask = np.array([True, True, True, True, False, True, True, True, False, False, True, True, True])
                
        # structure of the processed line
        trapezoid_pattern_presence = np.array(list(map(lambda x: True if len(x) > 0 else False, self.liste)), dtype = bool)
        
        # compare the two of them
        if not np.array_equal(trapezoid_pattern_mask, trapezoid_pattern_presence):
            self.error_list.append('line ' + str(self.line_number) + ' mandatory parameter absent or pointless parameter')

    def checkPosInit(self):
        if float(self.liste[C_OFFSET_COLUMN]) < self.pos_init_min:
            self.error_list.append('line ' + str(self.line_number) + ' pos init < min')
        elif float(self.liste[C_OFFSET_COLUMN]) > self.pos_init_max:
            self.error_list.append('line ' + str(self.line_number) + ' pos init > max')
            
    def checkPosTarget(self, target):
        if target == 1:
            label = ' pos target1'
            val_min = self.pos_target1_min
            val_max = self.pos_target1_max
            column = C_AMPL_OR_STEP_INC_OR_FINAL_POS1_COLUMN
        elif target == 2:
            label = ' pos target2'
            val_min = self.pos_target2_min
            val_max = self.pos_target2_max
            column = C_FINAL_POS2_COLUMN
        if float(self.liste[column]) < val_min:
            self.error_list.append('line ' + str(self.line_number) + label + ' < min')
        elif float(self.liste[column]) > val_max:
            self.error_list.append('line ' + str(self.line_number) + label + ' > max')

    def checkIsNumber(self):
        if not isNumber(self.liste[C_DELAY_OR_STEP_DURATION_COLUMN]):
            self.error_list.append('line ' + str(self.line_number) + ' step duration is not a number')
            
        if not isNumber(self.liste[C_OFFSET_COLUMN]):
            self.error_list.append('line ' + str(self.line_number) + ' offset is not a number')

        if not isNumber(self.liste[C_AMPL_OR_STEP_INC_OR_FINAL_POS1_COLUMN]):
            self.error_list.append('line ' + str(self.line_number) + ' final pos1 is not a number')
            
        if not isNumber(self.liste[C_FINAL_POS2_COLUMN]):
            self.error_list.append('line ' + str(self.line_number) + ' final pos2 is not a number')
            
        if not isNumber(self.liste[C_SLOPE_COLUMN]):
            self.error_list.append('line ' + str(self.line_number) + ' slope is not a number')
            
        if not isNumber(self.liste[C_INTERVAL_DURATION_COLUMN]):
            self.error_list.append('line ' + str(self.line_number) + ' interval duration is not a number')

    def check600HzCommand(self):
        # for patterns != sinus, 600Hz parameter must always be set to FALSE:
        if self.liste[C_IS_600HZ_CMD_COLUMN] != 'FALSE':
            self.error_list.append('line ' + str(self.line_number) + ' invalid 600Hz parameter: must be FALSE for trapezoid patterns')

    def setTrapezoidPatternThreshold(self):
        with open (self.threshold_file,'r',encoding='utf8') as self.threshold_file_handler:                
            # Creation of df_threshold data frame:
            self.df_threshold = pd.read_csv(self.threshold_file, sep=C_SEPARATOR, comment=C_COMMENT, header = 0, skip_blank_lines=True)
