# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.common import *
from error.datdutErrors import *

class CheckSquarePatterns():
    "check square patterns of dut file"
    
    def __init__(self, obj_init, id_list):
        self.liste = obj_init.getListe()
        self.line_number = obj_init.getLineNumber()
        self.fu_type = obj_init.getFUType()
        self.id_list = id_list
        self.error_list = []
        self.error_string = ''
        
        # Threshold file
        if self.fu_type == 'SR':
            self.threshold_file = C_THRESHOLD_DIR + C_SR_SQUARE_THRESHOLD_FILE
        elif self.fu_type == 'LL':
            self.threshold_file = C_THRESHOLD_DIR + C_LL_SQUARE_THRESHOLD_FILE
        elif self.fu_type == 'UL':
            self.threshold_file = C_THRESHOLD_DIR + C_UL_SQUARE_THRESHOLD_FILE
            
        # set df_threshold
        self.setSquarePatternThreshold()
        
        # get min, max values
        self.nb_steps_min = (self.df_threshold[self.df_threshold.parameter == 'nb_steps']).iloc[0,1]
        self.nb_steps_max = (self.df_threshold[self.df_threshold.parameter == 'nb_steps']).iloc[0,2]
        self.offset_min = (self.df_threshold[self.df_threshold.parameter == 'offset']).iloc[0,1]
        self.offset_max = (self.df_threshold[self.df_threshold.parameter == 'offset']).iloc[0,2]
        self.step_duration_min = (self.df_threshold[self.df_threshold.parameter == 'step_duration']).iloc[0,1]
        self.step_duration_max = (self.df_threshold[self.df_threshold.parameter == 'step_duration']).iloc[0,2]
        self.step_increment_min = (self.df_threshold[self.df_threshold.parameter == 'step_increment']).iloc[0,1]
        self.step_increment_max = (self.df_threshold[self.df_threshold.parameter == 'step_increment']).iloc[0,2]
        
        print(self.liste)
    
    def checkSquarePattern(self):
        self.checkMandatoryOrPointlessParameters()
        self.checkIsNumber()
        self.checkNbOfStepsisInteger()

        # if an error occured during check of manadatory parameters
        # do not proceed the other checks (no point doing it because maybe parameter is not defined):
        if len(self.error_list):
            self.error_list.append('line ' + str(self.line_number) + ' error in type/structure of parameters => no additionnal check for this line')
        else:
            self.checkSquarePatternIDsUnique()
            self.checkNbOfSteps()
            self.checkNbOfStepsIsEven()
            self.checkStepDuration()
            self.checkIncrement()
            self.checkOffset()
            self.check600HzCommand()

        # raises an error if necessary:
        if len(self.error_list):
            while self.error_list:
                try:
                    self.error_string = self.error_string + self.error_list.pop(0) + '\n'
                except IndexError:
                    break
            
            raise SquarePatternsError(self.error_string)

    def checkSquarePatternIDsUnique(self):
        if self.liste[C_ID_COLUMN] in self.id_list:
            self.error_list.append('line ' + str(self.line_number) + ' square pattern ids are not unique.')
        else:
            self.id_list.append(self.liste[C_ID_COLUMN])

    def checkIsNumber(self):
        if not isNumber(self.liste[C_DELAY_OR_STEP_DURATION_COLUMN]):
            self.error_list.append('line ' + str(self.line_number) + ' step duration is not a number')
            
        if not isNumber(self.liste[C_OFFSET_COLUMN]):
            self.error_list.append('line ' + str(self.line_number) + ' offset is not a number')

        if not isNumber(self.liste[C_AMPL_OR_STEP_INC_OR_FINAL_POS1_COLUMN]):
            self.error_list.append('line ' + str(self.line_number) + ' step increment is not a number')
            
        if not isNumber(self.liste[C_NB_ITEM_OR_FIRST_PATT_NUM]):
            self.error_list.append('line ' + str(self.line_number) + ' nb of steps is not a number')

    def checkNbOfSteps(self):
        if int(self.liste[C_NB_ITEM_OR_FIRST_PATT_NUM]) < self.nb_steps_min:
            self.error_list.append('line ' + str(self.line_number) + ' number of steps < min')
        elif int(self.liste[C_NB_ITEM_OR_FIRST_PATT_NUM]) > self.nb_steps_max:
            self.error_list.append('line ' + str(self.line_number) + ' number of steps > max')

    def checkNbOfStepsisInteger(self):
        if not self.liste[C_NB_ITEM_OR_FIRST_PATT_NUM].isdigit():
            self.error_list.append('line ' + str(self.line_number) + ' number of points is not a positive integer')
    
    def checkNbOfStepsIsEven(self):
        if int(self.liste[C_NB_ITEM_OR_FIRST_PATT_NUM])%2 != 0:
            self.error_list.append('line ' + str(self.line_number) + ' number of repet is odd number => must be even.')

    def checkStepDuration(self):
        if float(self.liste[C_DELAY_OR_STEP_DURATION_COLUMN]) < self.step_duration_min:
            self.error_list.append('line ' + str(self.line_number) + ' step duration < min')
        elif float(self.liste[C_DELAY_OR_STEP_DURATION_COLUMN]) > self.step_duration_max:
            self.error_list.append('line ' + str(self.line_number) + ' step duration > max')

    def checkIncrement(self):
        if float(self.liste[C_AMPL_OR_STEP_INC_OR_FINAL_POS1_COLUMN]) < self.step_increment_min:
            self.error_list.append('line ' + str(self.line_number) + ' step increment < min')
        elif float(self.liste[C_AMPL_OR_STEP_INC_OR_FINAL_POS1_COLUMN]) > self.step_increment_max:
            self.error_list.append('line ' + str(self.line_number) + ' step increment > max')

    def checkMandatoryOrPointlessParameters(self):
        # check mandatory parameters are mentioned
        # check pointless parameters for square patterns are missing
        square_pattern_mask = np.array([True, True, True, True, False, True, True, True, True, False, False, False, False])
                
        # structure of the processed line
        square_pattern_presence = np.array(list(map(lambda x: True if len(x) > 0 else False, self.liste)), dtype = bool)
        
        # compare the two of them
        if not np.array_equal(square_pattern_mask, square_pattern_presence):
            self.error_list.append('line ' + str(self.line_number) + ' mandatory parameter absent or pointless parameter')

    def checkOffset(self):
        if float(self.liste[C_OFFSET_COLUMN]) < self.offset_min:
            self.error_list.append('line ' + str(self.line_number) + ' offset < min')
        elif float(self.liste[C_OFFSET_COLUMN]) > self.offset_max:
            self.error_list.append('line ' + str(self.line_number) + ' offset > max')
    
    def check600HzCommand(self):
        # for patterns != sinus, 600Hz parameter must always be set to FALSE:
        if self.liste[C_IS_600HZ_CMD_COLUMN] != 'FALSE':
            self.error_list.append('line ' + str(self.line_number) + ' invalid 600Hz parameter: must be FALSE for square patterns')

    def setSquarePatternThreshold(self):
        with open (self.threshold_file,'r',encoding='utf8') as self.threshold_file_handler:                
            # Creation of df_threshold data frame:
            self.df_threshold = pd.read_csv(self.threshold_file, sep=C_SEPARATOR, comment=C_COMMENT, header = 0, skip_blank_lines=True)
