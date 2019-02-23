# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.common import *
from checks.checkDATDUT import *
from checks.checkPatterns import *
from error.datdutErrors import *

class CheckBangBangPatterns(CheckPatterns):
    "check bangbang patterns from DAT DUT file"
    
    def __init__(self, data_frame, fu_type):
        CheckPatterns.__init__(self, data_frame, fu_type)
        
        # Select bangbang pattern rows
        self.df_bangbang_pattern_rows = self.df_pattern_rows[self.df_pattern_rows.type == "bangbang"]
        
        # Threshold file
        if self.fu_type == 'SR':
            self.threshold_file = C_THRESHOLD_DIR + C_SR_BANGBANG_THRESHOLD_FILE
        elif self.fu_type == 'LL':
            self.threshold_file = C_THRESHOLD_DIR + C_LL_BANGBANG_THRESHOLD_FILE
        elif self.fu_type == 'UL':
            self.threshold_file = C_THRESHOLD_DIR + C_UL_BANGBANG_THRESHOLD_FILE
        else:
            raise BangBangPatternsError("[Bangbang Pattern Error]: Unknown FU type: ", self.fu_type)
            
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
    
    def checkBangBangPatternIDsUnique(self):
        self.temp_df = self.df_bangbang_pattern_rows.loc[:,'id']
        
        if not self.temp_df.is_unique:
            self.temp_df = self.df_bangbang_pattern_rows.loc[:, 'line':'id':C_ID_COLUMN]
            raise BangBangPatternsError("[BangBang Pattern Error]: BangBang patterns id's are not unique, see below: \n", self.temp_df.values)

    def checkDelay(self):
        # get lines where:
        #   - delay_or_step_duration is out of range
        # then return line and delay_or_step_duration columns for those lines
        self.temp_df_low = self.df_bangbang_pattern_rows.loc[self.df_bangbang_pattern_rows.loc[:, 'delay_or_step_duration'] < self.delay_min,'line':'delay_or_step_duration':C_DELAY_OR_STEP_DURATION_COLUMN]
        self.temp_df_high = self.df_bangbang_pattern_rows.loc[self.df_bangbang_pattern_rows.loc[:, 'delay_or_step_duration'] > self.delay_max,'line':'delay_or_step_duration':C_DELAY_OR_STEP_DURATION_COLUMN]

        if not self.temp_df_low.empty:
            raise BangBangPatternsError("[Bangbang Pattern Error]: delay_or_step_duration(s) < min in line(s) below: \n", self.temp_df_low.values)
            
        if not self.temp_df_high.empty:
            raise BangBangPatternsError("[Bangbang Pattern Error]: delay_or_step_duration(s) > max in line(s) below: \n", self.temp_df_high.values)
            
    def checkOffset(self):
        # get lines where:
        #   - offset is out of range
        # then return line and offset columns for those lines
        self.temp_df_low = self.df_bangbang_pattern_rows.loc[self.df_bangbang_pattern_rows.loc[:, 'offset'] < self.pos_init_min,'line':'offset':C_OFFSET_COLUMN]
        self.temp_df_high = self.df_bangbang_pattern_rows.loc[self.df_bangbang_pattern_rows.loc[:, 'offset'] > self.pos_init_max,'line':'offset':C_OFFSET_COLUMN]

        if not self.temp_df_low.empty:
            raise BangBangPatternsError("[Bangbang Pattern Error]: pos init < min in line(s) below: \n", self.temp_df_low.values)
            
        if not self.temp_df_high.empty:
            raise BangBangPatternsError("[Bangbang Pattern Error]: pos init > max in line(s) below: \n", self.temp_df_high.values)
            
    def checkPosTarget(self):
        # get lines where:
        #   - ampl_or_stepinc_or_finalpos1 is out of range
        # then return line and delay_or_step_duration columns for those lines
        self.temp_df_low = self.df_bangbang_pattern_rows.loc[self.df_bangbang_pattern_rows.loc[:, 'ampl_or_stepinc_or_finalpos1'] < self.pos_target_min,'line':'ampl_or_stepinc_or_finalpos1':C_AMPL_OR_STEP_INC_OR_FINAL_POS1_COLUMN]
        self.temp_df_high = self.df_bangbang_pattern_rows.loc[self.df_bangbang_pattern_rows.loc[:, 'ampl_or_stepinc_or_finalpos1'] > self.pos_target_max,'line':'ampl_or_stepinc_or_finalpos1':C_AMPL_OR_STEP_INC_OR_FINAL_POS1_COLUMN]

        if not self.temp_df_low.empty:
            raise BangBangPatternsError("[Bangbang Pattern Error]: pos target < min in line(s) below: \n", self.temp_df_low.values)
            
        if not self.temp_df_high.empty:
            raise BangBangPatternsError("[Bangbang Pattern Error]: pos target > max in line(s) below: \n", self.temp_df_high.values)
    
    def checkSlope(self):
        # get lines where:
        #   - slope is out of range
        # then return line and slope columns for those lines
        self.temp_df_low = self.df_bangbang_pattern_rows.loc[self.df_bangbang_pattern_rows.loc[:, 'slope'] < self.slope_value_min,'line':'slope':C_SLOPE_COLUMN]
        self.temp_df_high = self.df_bangbang_pattern_rows.loc[self.df_bangbang_pattern_rows.loc[:, 'slope'] > self.slope_value_max,'line':'slope':C_SLOPE_COLUMN]

        if not self.temp_df_low.empty:
            raise BangBangPatternsError("[Bangbang Pattern Error]: slope < min in line(s) below: \n", self.temp_df_low.values)
            
        if not self.temp_df_high.empty:
            raise BangBangPatternsError("[Bangbang Pattern Error]: slope > max in line(s) below: \n", self.temp_df_high.values)
            
    def checkMandatoryOrPointlessParameters(self):
        # check mandatory parameters are mentioned
        # check pointless parameters for bangbang patterns are missing
        bangbang_pattern_mask = np.array([True, True, True, True, True, False, True, True, True, False, False, False, True, False])
                
        for i in range(self.df_bangbang_pattern_rows.shape[0]):
            bangbang_parameter_presence = np.array(self.df_bangbang_pattern_rows.iloc[i,:].notna())
            if not np.array_equal(bangbang_pattern_mask, bangbang_parameter_presence):
                raise BangBangPatternsError("[Bangbang Pattern Error]: mandatory parameter missing or pointless parameter specified in line: ", self.df_bangbang_pattern_rows.iloc[i,C_LINE_COLUMN])

    def setBangBangPatternThreshold(self):
        with open (self.threshold_file,'r',encoding='utf8') as self.threshold_file_handler:                
            # Creation of df_threshold data frame:
            self.df_threshold = pd.read_csv(self.threshold_file, sep=C_SEPARATOR, comment=C_COMMENT, header = 0, skip_blank_lines=True)
