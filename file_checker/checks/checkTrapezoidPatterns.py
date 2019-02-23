# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.common import *
from checks.checkDATDUT import *
from checks.checkPatterns import *
from error.datdutErrors import *

class CheckTrapezoidPatterns(CheckPatterns):
    "check trapezoid patterns from DAT DUT file"
    
    def __init__(self, data_frame, fu_type):
        CheckPatterns.__init__(self, data_frame, fu_type)
        
        # Select trapezoid pattern rows
        self.df_trapezoid_pattern_rows = self.df_pattern_rows[self.df_pattern_rows.type == "trapezoid"]
        
        # Threshold file
        if self.fu_type == 'SR':
            self.threshold_file = C_THRESHOLD_DIR + C_SR_TRAPEZOID_THRESHOLD_FILE
        elif self.fu_type == 'LL':
            self.threshold_file = C_THRESHOLD_DIR + C_LL_TRAPEZOID_THRESHOLD_FILE
        elif self.fu_type == 'UL':
            self.threshold_file = C_THRESHOLD_DIR + C_UL_TRAPEZOID_THRESHOLD_FILE
        else:
            raise TrapezoidPatternsError("[Trapezoid Pattern Error]: Unknown FU type: ", self.fu_type)
            
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
    
    def checkTrapezoidPatternIDsUnique(self):
        self.temp_df = self.df_trapezoid_pattern_rows.loc[:,'id']
        
        if not self.temp_df.is_unique:
            self.temp_df = self.df_trapezoid_pattern_rows.loc[:, 'line':'id':C_ID_COLUMN]
            raise TrapezoidPatternsError("[Trapezoid Pattern Error]: Trapezoid patterns id's are not unique, see below: \n", self.temp_df.values)

    def checkSlope(self):
        # get lines where:
        #   - slope < min
        #   - slope > max   
        # then return line and delay_or_step_duration columns for those lines
        self.temp_df_low = self.df_trapezoid_pattern_rows.loc[self.df_trapezoid_pattern_rows.loc[:, 'slope'] < self.slope_value_min,'line':'slope':C_SLOPE_COLUMN]
        self.temp_df_high = self.df_trapezoid_pattern_rows.loc[self.df_trapezoid_pattern_rows.loc[:, 'slope'] > self.slope_value_max,'line':'slope':C_SLOPE_COLUMN]

        if not self.temp_df_low.empty:
            raise TrapezoidPatternsError("[Trapezoid Pattern Error]: slope < min in line(s) below: \n", self.temp_df_low.values)
            
        if not self.temp_df_high.empty:
            raise TrapezoidPatternsError("[Trapezoid Pattern Error]: slope > max in line(s) below: \n", self.temp_df_high.values)

    def checkStepDuration(self):
        # get lines where:
        #   - delay_or_step_duration < min
        #   - delay_or_step_duration > max   
        # then return line and delay_or_step_duration columns for those lines
        self.temp_df_low = self.df_trapezoid_pattern_rows.loc[self.df_trapezoid_pattern_rows.loc[:, 'delay_or_step_duration'] < self.step_duration_min,'line':'delay_or_step_duration':C_DELAY_OR_STEP_DURATION_COLUMN]
        self.temp_df_high = self.df_trapezoid_pattern_rows.loc[self.df_trapezoid_pattern_rows.loc[:, 'delay_or_step_duration'] > self.step_duration_max,'line':'delay_or_step_duration':C_DELAY_OR_STEP_DURATION_COLUMN]

        if not self.temp_df_low.empty:
            raise TrapezoidPatternsError("[Trapezoid Pattern Error]: step duration < min in line(s) below: \n", self.temp_df_low.values)
            
        if not self.temp_df_high.empty:
            raise TrapezoidPatternsError("[Trapezoid Pattern Error]: step duration > max in line(s) below: \n", self.temp_df_high.values)

    def checkIntervalDuration(self):
        # get lines where:
        #   - interval_duration < min
        #   - interval_duration > max
        # then return line and interval_duration columns for those lines            
        self.temp_df_low = self.df_trapezoid_pattern_rows.loc[self.df_trapezoid_pattern_rows.loc[:, 'interval_duration'] < self.inter_gap_duration_min,'line':'interval_duration':C_INTERVAL_DURATION_COLUMN]
        self.temp_df_high = self.df_trapezoid_pattern_rows.loc[self.df_trapezoid_pattern_rows.loc[:, 'interval_duration'] > self.inter_gap_duration_max,'line':'interval_duration':C_INTERVAL_DURATION_COLUMN]

        if not self.temp_df_low.empty:
            raise TrapezoidPatternsError("[Trapezoid Pattern Error]: interval duration < min in line(s) below: \n", self.temp_df_low.values)
            
        if not self.temp_df_high.empty:
            raise TrapezoidPatternsError("[Trapezoid Pattern Error]: interval duration > max in line(s) below: \n", self.temp_df_high.values)

    def checkMandatoryOrPointlessParameters(self):
        # check mandatory parameters are mentioned
        # check pointless parameters for trapezoid patterns are missing
        trapezoid_pattern_mask = np.array([True, True, True, True, True, False, True, True, True, True, False, False, True, True])
                
        for i in range(self.df_trapezoid_pattern_rows.shape[0]):
            trapezoid_parameter_presence = np.array(self.df_trapezoid_pattern_rows.iloc[i,:].notna())
            if not np.array_equal(trapezoid_pattern_mask, trapezoid_parameter_presence):
                raise TrapezoidPatternsError("[Trapezoid Pattern Error]: mandatory parameter missing or pointless parameter specified in line: ", self.df_trapezoid_pattern_rows.iloc[i,C_LINE_COLUMN])

    def checkPosInit(self):
        # get lines where:
        #   - pos init < min
        #   - pos init > max
        # then return line and offset column for those lines            
        self.temp_df_low = self.df_trapezoid_pattern_rows.loc[self.df_trapezoid_pattern_rows.loc[:, 'offset'] < self.pos_init_min,'line':'offset':C_OFFSET_COLUMN]
        self.temp_df_high = self.df_trapezoid_pattern_rows.loc[self.df_trapezoid_pattern_rows.loc[:, 'offset'] > self.pos_init_max,'line':'offset':C_OFFSET_COLUMN]

        if not self.temp_df_low.empty:
            raise TrapezoidPatternsError("[Trapezoid Pattern Error]: pos init < min in line(s) below: \n", self.temp_df_low.values)
            
        if not self.temp_df_high.empty:
            raise TrapezoidPatternsError("[Trapezoid Pattern Error]: pos init > max in line(s) below: \n", self.temp_df_high.values)
            
    def checkPosTarget(self, target):
        # get lines where:
        #   - pos target i (i=1 or 2) < min
        #   - pos target i (i=1 or 2) > max
        # then return line and ampl_or_stepinc_or_finalpos1 or finalpos2 column for those lines        
        if target == 1:
            field_name = 'ampl_or_stepinc_or_finalpos1'
            val_min = self.pos_target1_min
            val_max = self.pos_target1_max
            column = C_AMPL_OR_STEP_INC_OR_FINAL_POS1_COLUMN
        elif target == 2:
            field_name = 'finalpos2'
            val_min = self.pos_target2_min
            val_max = self.pos_target2_max
            column = C_FINAL_POS2_COLUMN
        else:
            raise TrapezoidPatternsError("[Trapezoid Pattern Error]: Unknown target position (must be 1 or 2)", None)
        
        self.temp_df_low = self.df_trapezoid_pattern_rows.loc[self.df_trapezoid_pattern_rows.loc[:, field_name] < val_min,'line':field_name:column]
        self.temp_df_high = self.df_trapezoid_pattern_rows.loc[self.df_trapezoid_pattern_rows.loc[:, field_name] > val_max,'line':field_name:column]

        if not self.temp_df_low.empty:
            raise TrapezoidPatternsError("[Trapezoid Pattern Error]: pos target < min in line(s) below: \n", self.temp_df_low.values)
            
        if not self.temp_df_high.empty:
            raise TrapezoidPatternsError("[Trapezoid Pattern Error]: pos target > max in line(s) below: \n", self.temp_df_high.values)

    def setTrapezoidPatternThreshold(self):
        with open (self.threshold_file,'r',encoding='utf8') as self.threshold_file_handler:                
            # Creation of df_threshold data frame:
            self.df_threshold = pd.read_csv(self.threshold_file, sep=C_SEPARATOR, comment=C_COMMENT, header = 0, skip_blank_lines=True)
