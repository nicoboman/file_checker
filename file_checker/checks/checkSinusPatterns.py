# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.common import *
from builtins import range
from error.datdutErrors import *
from numpy import dtype

class CheckSinusPatterns:
    "check sinus patterns of dut file"
    
    def __init__(self, liste, line_number, fu_type):
        self.liste = liste
        self.line_number = line_number
        self.fu_type = fu_type
        self.error_list = []
        self.error_string = ''
        self.keys = {}
        
        # Threshold file
        if fu_type == 'SR':
            self.threshold_file = C_THRESHOLD_DIR + C_SR_SINUS_THRESHOLD_FILE
        elif fu_type == 'LL':
            self.threshold_file = C_THRESHOLD_DIR + C_LL_SINUS_THRESHOLD_FILE
        elif fu_type == 'UL':
            self.threshold_file = C_THRESHOLD_DIR + C_UL_SINUS_THRESHOLD_FILE
        else:
            raise SinusPatternsError("[Sinus Pattern Error]: Unknown FU type: ", self.fu_type)
            
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
        
        print(self.liste)

    def checkThisSinusPattern(self):
        self.checkMandatoryOrPointlessParameters()
        
        # if an error occured during check of manadatory parameters
        # do not proceed the other checks (no point doing it because maybe parameter is not defined):
        if not len(self.error_list):
#             self.checkSinusPatternIDsUnique()
            self.checkAmplitude()
            self.checkNbOfPoints()
            self.checkNbOfPointsisInteger()
            self.checkNbOfRepet()
            self.checkNbOfRepetisInteger()
#             self.checkSinusDelay()
#             self.checkOffset()

        # raises an error if necessary:
        if len(self.error_list):
            while self.error_list:
                try:
                    self.error_string = self.error_string + self.error_list.pop(0) + '\n'
                except IndexError:
                    break
            
            raise SinusPatternsError(self.error_string)

#     def checkSinusPatternIDsUnique(self):
# #         TODO

    def checkAmplitude(self):
        if float(self.liste[C_AMPL_OR_STEP_INC_OR_FINAL_POS1_COLUMN]) < self.ampl_min:
            self.error_list.append('line ' + str(self.line_number) + ' amplitude < min')
        elif float(self.liste[C_AMPL_OR_STEP_INC_OR_FINAL_POS1_COLUMN]) > self.ampl_max:
            self.error_list.append('line ' + str(self.line_number) + ' amplitude > max')

    def checkNbOfPoints(self):
        if float(self.liste[C_NB_ITEM_OR_FIRST_PATT_NUM]) < self.nb_point_min:
            self.error_list.append('line ' + str(self.line_number) + ' number of points < min')
        elif float(self.liste[C_NB_ITEM_OR_FIRST_PATT_NUM]) > self.nb_point_max:
            self.error_list.append('line ' + str(self.line_number) + ' number of points > max')
    
    def checkNbOfPointsisInteger(self):
        if not self.liste[C_NB_ITEM_OR_FIRST_PATT_NUM].isdigit():
            self.error_list.append('line ' + str(self.line_number) + ' number of points is not a positive integer')

    def checkNbOfRepet(self):
        if float(self.liste[C_NB_REPET_OR_LAST_PATT_NUM_COLUMN]) < self.nb_repet_min:
            self.error_list.append('line ' + str(self.line_number) + ' number of repet < min')
        elif float(self.liste[C_NB_REPET_OR_LAST_PATT_NUM_COLUMN]) > self.nb_repet_max:
            self.error_list.append('line ' + str(self.line_number) + ' number of repet > max')
            
    def checkNbOfRepetisInteger(self):
        if not self.liste[C_NB_REPET_OR_LAST_PATT_NUM_COLUMN].isdigit():
            self.error_list.append('line ' + str(self.line_number) + ' number of repet is not a positive integer')
    
    def checkMandatoryOrPointlessParameters(self):
        # check mandatory parameters are mentioned
        # check pointless parameters for sinus patterns are missing
        # mask to match with
        sinus_pattern_mask = np.array([True, True, True, True, False, True, True, True, True, True, False, False, False])
        
        # structure of the processed line
        sinus_parameter_presence = np.array(list(map(lambda x: True if len(x) > 0 else False, self.liste)), dtype = bool)
        
        # compare the two of them
        if not np.array_equal(sinus_pattern_mask, sinus_parameter_presence):
            self.error_list.append('line ' + str(self.line_number) + ' mandatory parameter absent or pointless parameter => no additionnal check for this line')
                   
    def checkSinusDelay(self):
        # get lines where:
        #   - delay_or_step_duration is out of range
        # then return line and delay_or_step_duration columns for those lines
        self.temp_df_low = self.df_sinus_pattern_rows.loc[self.df_sinus_pattern_rows.loc[:, 'delay_or_step_duration'] < self.delay_min,'line':'delay_or_step_duration':C_DELAY_OR_STEP_DURATION_COLUMN]
        self.temp_df_high = self.df_sinus_pattern_rows.loc[self.df_sinus_pattern_rows.loc[:, 'delay_or_step_duration'] > self.delay_max,'line':'delay_or_step_duration':C_DELAY_OR_STEP_DURATION_COLUMN]

        if not self.temp_df_low.empty:
            raise SinusPatternsError("[Sinus Pattern Error]: delay_or_step_duration(s) < min in line(s) below: \n", self.temp_df_low.values)
            
        if not self.temp_df_high.empty:
            raise SinusPatternsError("[Sinus Pattern Error]: delay_or_step_duration(s) > max in line(s) below: \n", self.temp_df_high.values)
            
    def checkOffset(self):
        # get lines where:
        #   - offset is out of range
        # then return line and offset columns for those lines
        self.temp_df_low = self.df_sinus_pattern_rows.loc[self.df_sinus_pattern_rows.loc[:, 'offset'] < self.offset_min,'line':'offset':C_OFFSET_COLUMN]
        self.temp_df_high = self.df_sinus_pattern_rows.loc[self.df_sinus_pattern_rows.loc[:, 'offset'] > self.offset_max,'line':'offset':C_OFFSET_COLUMN]

        if not self.temp_df_low.empty:
            raise SinusPatternsError("[Sinus Pattern Error]: offset(s) < min in line(s) below: \n", self.temp_df_low.values)
            
        if not self.temp_df_high.empty:
            raise SinusPatternsError("[Sinus Pattern Error]: offset(s) > max in line(s) below: \n", self.temp_df_high.values)
            
    def setSinusPatternThreshold(self):
        with open (self.threshold_file,'r',encoding='utf8') as self.threshold_file_handler:                
            # Creation of df_threshold data frame:
            self.df_threshold = pd.read_csv(self.threshold_file, sep=C_SEPARATOR, comment=C_COMMENT, header = 0, skip_blank_lines=True)
                           