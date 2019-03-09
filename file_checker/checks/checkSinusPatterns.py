# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.common import *
from error.datdutErrors import *
from numpy import dtype

class CheckSinusPatterns:
    "check sinus patterns of dut file"
    
    def __init__(self, obj_init):
        self.liste = obj_init.getListe()
        self.line_number = obj_init.getLineNumber()
        self.fu_type = obj_init.getFUType()
        self.error_list = []
        self.error_string = ''
        
        # Threshold file
        if self.fu_type == 'SR':
            self.threshold_file = C_THRESHOLD_DIR + C_SR_SINUS_THRESHOLD_FILE
        elif self.fu_type == 'LL':
            self.threshold_file = C_THRESHOLD_DIR + C_LL_SINUS_THRESHOLD_FILE
        elif self.fu_type == 'UL':
            self.threshold_file = C_THRESHOLD_DIR + C_UL_SINUS_THRESHOLD_FILE
            
        # set df_threshold
        self.setSinusPatternThreshold()
        
        # get min, max values
        self.delay_min = (self.df_threshold[self.df_threshold.parameter == 'delay']).iloc[0,1]
        self.delay_max = (self.df_threshold[self.df_threshold.parameter == 'delay']).iloc[0,2]
        self.offset_min = (self.df_threshold[self.df_threshold.parameter == 'offset']).iloc[0,1]
        self.offset_max = (self.df_threshold[self.df_threshold.parameter == 'offset']).iloc[0,2]
        self.ampl_min = (self.df_threshold[self.df_threshold.parameter == 'ampl']).iloc[0,1]
        self.ampl_max = (self.df_threshold[self.df_threshold.parameter == 'ampl']).iloc[0,2]
        self.nb_point_min = (self.df_threshold[self.df_threshold.parameter == 'nb_point']).iloc[0,1]
        self.nb_point_max = (self.df_threshold[self.df_threshold.parameter == 'nb_point']).iloc[0,2]
        self.nb_repet_min = (self.df_threshold[self.df_threshold.parameter == 'nb_repet']).iloc[0,1]
        self.nb_repet_max = (self.df_threshold[self.df_threshold.parameter == 'nb_repet']).iloc[0,2]
        
    def checkSinusPattern(self):
        self.checkMandatoryOrPointlessParameters()
        self.checkIsNumber()
        self.checkNbOfPointsisInteger()
        self.checkNbOfRepetisInteger()

        # if an error occured during check of manadatory parameters
        # do not proceed the other checks (no point doing it because maybe parameter is not defined):
        if len(self.error_list):
            self.error_list.append('line ' + str(self.line_number) + ' error in type/structure of parameters => no additionnal check for this line')
        else:
            self.checkAmplitude()
            self.checkNbOfPoints()
            self.checkNbOfRepet()
            self.checkDelay()
            self.checkOffset()
            self.check600HzCommand()

        # raises an error if necessary:
        if len(self.error_list):
            while self.error_list:
                try:
                    self.error_string = self.error_string + self.error_list.pop(0) + '\n'
                except IndexError:
                    break
            
            raise SinusPatternsError(self.error_string)

    def checkMandatoryOrPointlessParameters(self):
        # check mandatory parameters are mentioned
        # check pointless parameters for sinus patterns are missing
        # mask to match with
        sinus_pattern_mask = np.array([True, True, True, True, False, True, True, True, True, True, False, False, False])
        
        # structure of the processed line
        sinus_parameter_presence = np.array(list(map(lambda x: True if len(x) > 0 else False, self.liste)), dtype = bool)
        
        # compare the two of them
        if not np.array_equal(sinus_pattern_mask, sinus_parameter_presence):
            self.error_list.append('line ' + str(self.line_number) + ' mandatory parameter absent or pointless parameter')
            
    def checkIsNumber(self):
        if not isNumber(self.liste[C_DELAY_OR_STEP_DURATION_COLUMN]):
            self.error_list.append('line ' + str(self.line_number) + ' delay is not a number')
            
        if not isNumber(self.liste[C_OFFSET_COLUMN]):
            self.error_list.append('line ' + str(self.line_number) + ' offset is not a number')

        if not isNumber(self.liste[C_AMPL_OR_STEP_INC_OR_FINAL_POS1_COLUMN]):
            self.error_list.append('line ' + str(self.line_number) + ' amplitude is not a number')

    def checkAmplitude(self):
        if float(self.liste[C_AMPL_OR_STEP_INC_OR_FINAL_POS1_COLUMN]) < self.ampl_min:
            self.error_list.append('line ' + str(self.line_number) + ' amplitude < min')
        elif float(self.liste[C_AMPL_OR_STEP_INC_OR_FINAL_POS1_COLUMN]) > self.ampl_max:
            self.error_list.append('line ' + str(self.line_number) + ' amplitude > max')
            
    def check600HzCommand(self):
        if self.liste[C_IS_600HZ_CMD_COLUMN] != 'TRUE' and self.liste[C_IS_600HZ_CMD_COLUMN] != 'FALSE':
            self.error_list.append('line ' + str(self.line_number) + ' invalid 600Hz parameter: must be TRUE/FALSE')

    def checkNbOfPoints(self):
        if int(self.liste[C_NB_ITEM_OR_FIRST_PATT_NUM]) < self.nb_point_min:
            self.error_list.append('line ' + str(self.line_number) + ' number of points < min')
        elif int(self.liste[C_NB_ITEM_OR_FIRST_PATT_NUM]) > self.nb_point_max:
            self.error_list.append('line ' + str(self.line_number) + ' number of points > max')
    
    def checkNbOfPointsisInteger(self):
        if not self.liste[C_NB_ITEM_OR_FIRST_PATT_NUM].isdigit():
            self.error_list.append('line ' + str(self.line_number) + ' number of points is not a positive integer')

    def checkNbOfRepet(self):
        if int(self.liste[C_NB_REPET_OR_LAST_PATT_NUM_COLUMN]) < self.nb_repet_min:
            self.error_list.append('line ' + str(self.line_number) + ' number of repet < min')
        elif int(self.liste[C_NB_REPET_OR_LAST_PATT_NUM_COLUMN]) > self.nb_repet_max:
            self.error_list.append('line ' + str(self.line_number) + ' number of repet > max')
            
    def checkNbOfRepetisInteger(self):
        if not self.liste[C_NB_REPET_OR_LAST_PATT_NUM_COLUMN].isdigit():
            self.error_list.append('line ' + str(self.line_number) + ' number of repet is not a positive integer')
                       
    def checkDelay(self):
        if float(self.liste[C_DELAY_OR_STEP_DURATION_COLUMN]) < self.delay_min:
            self.error_list.append('line ' + str(self.line_number) + ' delay < min')
        elif float(self.liste[C_DELAY_OR_STEP_DURATION_COLUMN]) > self.delay_max:
            self.error_list.append('line ' + str(self.line_number) + ' delay > max')
            
    def checkOffset(self):
        if float(self.liste[C_OFFSET_COLUMN]) < self.offset_min:
            self.error_list.append('line ' + str(self.line_number) + ' offset < min')
        elif float(self.liste[C_OFFSET_COLUMN]) > self.offset_max:
            self.error_list.append('line ' + str(self.line_number) + ' offset > max')

    def setSinusPatternThreshold(self):
        with open (self.threshold_file,'r',encoding='utf8') as self.threshold_file_handler:                
            # Creation of df_threshold data frame:
            self.df_threshold = pd.read_csv(self.threshold_file, sep=C_SEPARATOR, comment=C_COMMENT, header = 0, skip_blank_lines=True)
                       