# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.common import *
from checks.checkDATDUT import *
from checks.checkPatterns import *
from builtins import range
from error.datdutErrors import *

class CheckSinusPatterns(CheckPatterns):
    "check sinus patterns from DAT DUT file"
    
    def __init__(self, data_frame, fu_type):
        CheckPatterns.__init__(self, data_frame, fu_type)
        
        # Select sinus pattern rows
        self.df_sinus_pattern_rows = self.df_pattern_rows[self.df_pattern_rows.type == "sinus"]
        
        # Threshold file
        if self.fu_type == 'SR':
            self.threshold_file = C_THRESHOLD_DIR + C_SR_SINUS_THRESHOLD_FILE
        elif self.fu_type == 'LL':
            self.threshold_file = C_THRESHOLD_DIR + C_LL_SINUS_THRESHOLD_FILE
        elif self.fu_type == 'UL':
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

    def checkSinusPatternIDsUnique(self):
        self.temp_df = self.df_sinus_pattern_rows.loc[:,'id']
        
        if not self.temp_df.is_unique:
            self.temp_df = self.df_sinus_pattern_rows.loc[:, 'line':'id':C_ID_COLUMN]
            raise SinusPatternsError("[Sinus Pattern Error]: Sinus patterns id's are not unique, in line(s) below: \n", self.temp_df.values)

    def checkAmplitude(self):
        # get lines where:
        #   - ampl_or_stepinc_or_finalpos1 column is out of range
        # then return line and ampl_or_stepinc_or_finalpos1 columns for those lines
        self.temp_df_low = self.df_sinus_pattern_rows.loc[self.df_sinus_pattern_rows.loc[:, 'ampl_or_stepinc_or_finalpos1'] < self.ampl_min,'line':'ampl_or_stepinc_or_finalpos1':C_AMPL_OR_STEP_INC_OR_FINAL_POS1_COLUMN]
        self.temp_df_high = self.df_sinus_pattern_rows.loc[self.df_sinus_pattern_rows.loc[:, 'ampl_or_stepinc_or_finalpos1'] > self.ampl_max,'line':'ampl_or_stepinc_or_finalpos1':C_AMPL_OR_STEP_INC_OR_FINAL_POS1_COLUMN]

        if not self.temp_df_low.empty:
            raise SinusPatternsError("[Sinus Pattern Error]: ampl_or_stepinc_or_finalpos1(s) < min in line(s) below: \n", self.temp_df_low.values)
            
        if not self.temp_df_high.empty:
            raise SinusPatternsError("[Sinus Pattern Error]: ampl_or_stepinc_or_finalpos1(s) > max in line(s) below: \n", self.temp_df_high.values)

    def checkNbOfPoints(self):
        # get lines where:
        #   - nb_item_or_first_patt_num column <= 0
        # then return line and nb_item_or_first_patt_num columns for those lines
        self.temp_df_low = self.df_sinus_pattern_rows.loc[self.df_sinus_pattern_rows.loc[:, 'nb_item_or_first_patt_num'] < self.nb_point_min,'line':'nb_item_or_first_patt_num':C_NB_ITEM_OR_FIRST_PATT_NUM]
        self.temp_df_high = self.df_sinus_pattern_rows.loc[self.df_sinus_pattern_rows.loc[:, 'nb_item_or_first_patt_num'] > self.nb_point_max,'line':'nb_item_or_first_patt_num':C_NB_ITEM_OR_FIRST_PATT_NUM]

        if not self.temp_df_low.empty:
            raise SinusPatternsError("[Sinus Pattern Error]: nb_item_or_first_patt_num(s) < min in line(s) below: \n", self.temp_df_low.values)
            
        if not self.temp_df_high.empty:
            raise SinusPatternsError("[Sinus Pattern Error]: nb_item_or_first_patt_num(s) > max in line(s) below: \n", self.temp_df_high.values)
    
    def checkNbOfPointsisInteger(self):
        # nb_points must always be an integer        
        for i in range(self.df_sinus_pattern_rows.shape[0]):
            if not isInteger(self.df_sinus_pattern_rows.iloc[i,C_NB_ITEM_OR_FIRST_PATT_NUM]):
                raise SinusPatternsError("[Sinus Pattern Error]: nb of points is not an integer in line: ", self.df_sinus_pattern_rows.iloc[i,C_LINE_COLUMN])

    def checkNbOfRepet(self):
        # get lines where:
        #   - nb_repet_or_last_patt_num column <= 0
        # then return line and nb_repet_or_last_patt_num columns for those lines
        self.temp_df_low = self.df_sinus_pattern_rows.loc[self.df_sinus_pattern_rows.loc[:, 'nb_repet_or_last_patt_num'] < self.nb_repet_min,'line':'nb_repet_or_last_patt_num':C_NB_REPET_OR_LAST_PATT_NUM_COLUMN]
        self.temp_df_high = self.df_sinus_pattern_rows.loc[self.df_sinus_pattern_rows.loc[:, 'nb_repet_or_last_patt_num'] > self.nb_repet_max,'line':'nb_repet_or_last_patt_num':C_NB_REPET_OR_LAST_PATT_NUM_COLUMN]

        if not self.temp_df_low.empty:
            raise SinusPatternsError("[Sinus Pattern Error]: nb_repet_or_last_patt_num(s) < min in line(s) below: \n", self.temp_df_low.values)
            
        if not self.temp_df_high.empty:
            raise SinusPatternsError("[Sinus Pattern Error]: nb_repet_or_last_patt_num(s) > max in line(s) below: \n", self.temp_df_high.values)
    
    def checkNbOfRepetisInteger(self):
        # nb_repet must always be an integer        
        for i in range(self.df_sinus_pattern_rows.shape[0]):
            if not isInteger(self.df_sinus_pattern_rows.iloc[i,C_NB_REPET_OR_LAST_PATT_NUM_COLUMN]):
                raise SinusPatternsError("[Sinus Pattern Error]: nb of repet is not an integer in line: ", self.df_sinus_pattern_rows.iloc[i,C_LINE_COLUMN])
    
    def checkMandatoryOrPointlessParameters(self):
        # check mandatory parameters are mentioned
        # check pointless parameters for sinus patterns are missing
        sinus_pattern_mask = np.array([True, True, True, True, True, False, True, True, True, False, True, True, False, False])
                
        for i in range(self.df_sinus_pattern_rows.shape[0]):
            sinus_parameter_presence = np.array(self.df_sinus_pattern_rows.iloc[i,:].notna())
            if not np.array_equal(sinus_pattern_mask, sinus_parameter_presence):
                raise SinusPatternsError("[Sinus Pattern Error]: mandatory parameter missing or pointless parameter specified in line: ", self.df_sinus_pattern_rows.iloc[i,C_LINE_COLUMN])
                  
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
                           