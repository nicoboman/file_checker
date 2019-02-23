# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.common import *
from checks.checkDATDUT import *
from checks.checkPatterns import *
from error.datdutErrors import *

class CheckSquarePatterns(CheckPatterns):
    "check square patterns from DAT DUT file"
    
    def __init__(self, data_frame, fu_type):
        CheckPatterns.__init__(self, data_frame, fu_type)
        
        # Select square pattern rows
        self.df_square_pattern_rows = self.df_pattern_rows[self.df_pattern_rows.type == "square"]
        
        # Threshold file
        if self.fu_type == 'SR':
            self.threshold_file = C_THRESHOLD_DIR + C_SR_SQUARE_THRESHOLD_FILE
        elif self.fu_type == 'LL':
            self.threshold_file = C_THRESHOLD_DIR + C_LL_SQUARE_THRESHOLD_FILE
        elif self.fu_type == 'UL':
            self.threshold_file = C_THRESHOLD_DIR + C_UL_SQUARE_THRESHOLD_FILE
        else:
            raise SquarePatternsError("[Square Pattern Error]: Unknown FU type: ", self.fu_type)
            
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
    
    def checkSquarePatternIDsUnique(self):
        self.temp_df = self.df_square_pattern_rows.loc[:,'id']
        
        if not self.temp_df.is_unique:
            self.temp_df = self.df_square_pattern_rows.loc[:, 'line':'id':C_ID_COLUMN]
            raise SquarePatternsError("[Square Pattern Error]: Square patterns id's are not unique, see below: \n", self.temp_df.values)

    def checkNbOfSteps(self):
        # get lines where:
        #   - nb_item_or_first_patt_num column  < min
        #   - nb_item_or_first_patt_num column > max
        # then return line and nb_repet_or_last_patt_num columns for those lines            
        self.temp_df_low = self.df_square_pattern_rows.loc[self.df_square_pattern_rows.loc[:, 'nb_item_or_first_patt_num'] < self.nb_steps_min,'line':'nb_item_or_first_patt_num':C_NB_ITEM_OR_FIRST_PATT_NUM]
        self.temp_df_high = self.df_square_pattern_rows.loc[self.df_square_pattern_rows.loc[:, 'nb_item_or_first_patt_num'] > self.nb_steps_max,'line':'nb_item_or_first_patt_num':C_NB_ITEM_OR_FIRST_PATT_NUM]

        if not self.temp_df_low.empty:
            raise SquarePatternsError("[Square Pattern Error]: nb steps < min in line(s) below: \n", self.temp_df_low.values)
            
        if not self.temp_df_high.empty:
            raise SquarePatternsError("[Square Pattern Error]: nb steps > max in line(s) below: \n", self.temp_df_high.values)

    def checkNbOfStepsisInteger(self):
        # nb_steps must always be an integer        
        for i in range(self.df_square_pattern_rows.shape[0]):
            if not isInteger(self.df_square_pattern_rows.iloc[i,C_NB_ITEM_OR_FIRST_PATT_NUM]):
                raise SquarePatternsError("[Square Pattern Error]: nb of repet is not an integer in line: ", self.df_square_pattern_rows.iloc[i,C_LINE_COLUMN])
    
    def checkNbOfStepsIsEven(self):
        # get lines where:
        #   - nb_item_or_first_patt_num column % 2 != 0
        # then return line and nb_item_or_first_patt_num columns for those lines
        self.temp_df = self.df_square_pattern_rows.loc[(self.df_square_pattern_rows.loc[:, 'nb_item_or_first_patt_num']%2 != 0),'line':'nb_item_or_first_patt_num':C_NB_ITEM_OR_FIRST_PATT_NUM]
        
        if not self.temp_df.empty:
            raise SquarePatternsError("[Square Pattern Error]: nb of steps is not even in line(s) below: \n", self.temp_df.values)

    def checkStepDuration(self):
        # get lines where:
        #   - delay_or_step_duration column < min
        #   - delay_or_step_duration column > max
        # then return line and delay_or_step_duration columns for those lines
        self.temp_df_low = self.df_square_pattern_rows.loc[self.df_square_pattern_rows.loc[:, 'delay_or_step_duration'] < self.step_duration_min,'line':'delay_or_step_duration':C_DELAY_OR_STEP_DURATION_COLUMN]
        self.temp_df_high = self.df_square_pattern_rows.loc[self.df_square_pattern_rows.loc[:, 'delay_or_step_duration'] > self.step_duration_max,'line':'delay_or_step_duration':C_DELAY_OR_STEP_DURATION_COLUMN]

        if not self.temp_df_low.empty:
            raise SquarePatternsError("[Square Pattern Error]: step duration < min in line(s) below: \n", self.temp_df_low.values)
            
        if not self.temp_df_high.empty:
            raise SquarePatternsError("[Square Pattern Error]: step duration > max in line(s) below: \n", self.temp_df_high.values)

    def checkIncrement(self):
        # get lines where:
        #   - ampl_or_stepinc_or_finalpos1 column < min
        #   - ampl_or_stepinc_or_finalpos1 column > max        
        # then return line and ampl_or_stepinc_or_finalpos1 columns for those lines        
        self.temp_df_low = self.df_square_pattern_rows.loc[self.df_square_pattern_rows.loc[:, 'ampl_or_stepinc_or_finalpos1'] < self.step_increment_min,'line':'ampl_or_stepinc_or_finalpos1':C_AMPL_OR_STEP_INC_OR_FINAL_POS1_COLUMN]
        self.temp_df_high = self.df_square_pattern_rows.loc[self.df_square_pattern_rows.loc[:, 'ampl_or_stepinc_or_finalpos1'] > self.step_increment_max,'line':'ampl_or_stepinc_or_finalpos1':C_AMPL_OR_STEP_INC_OR_FINAL_POS1_COLUMN]

        if not self.temp_df_low.empty:
            raise SquarePatternsError("[Square Pattern Error]: increment < min in line(s) below: \n", self.temp_df_low.values)
            
        if not self.temp_df_high.empty:
            raise SquarePatternsError("[Square Pattern Error]: increment > max in line(s) below: \n", self.temp_df_high.values)
    
    def checkMandatoryOrPointlessParameters(self):
        # check mandatory parameters are mentioned
        # check pointless parameters for square patterns are missing
        square_pattern_mask = np.array([True, True, True, True, True, False, True, True, True, False, True, False, False, False])
                
        for i in range(self.df_square_pattern_rows.shape[0]):
            square_parameter_presence = np.array(self.df_square_pattern_rows.iloc[i,:].notna())
            if not np.array_equal(square_pattern_mask, square_parameter_presence):
                raise SquarePatternsError("[Square Pattern Error]: mandatory parameter missing or pointless parameter specified in line: ", self.df_square_pattern_rows.iloc[i,C_LINE_COLUMN])

    def checkOffset(self):
        # get lines where:
        #   - offset < min
        #   - offset > max
        # then return line and offset column for those lines            
        self.temp_df_low = self.df_square_pattern_rows.loc[self.df_square_pattern_rows.loc[:, 'offset'] < self.offset_min,'line':'offset':C_OFFSET_COLUMN]
        self.temp_df_high = self.df_square_pattern_rows.loc[self.df_square_pattern_rows.loc[:, 'offset'] > self.offset_max,'line':'offset':C_OFFSET_COLUMN]

        if not self.temp_df_low.empty:
            raise SquarePatternsError("[Square Pattern Error]: offset < min in line(s) below: \n", self.temp_df_low.values)
            
        if not self.temp_df_high.empty:
            raise SquarePatternsError("[Square Pattern Error]: offset > max in line(s) below: \n", self.temp_df_high.values)
    
    def setSquarePatternThreshold(self):
        with open (self.threshold_file,'r',encoding='utf8') as self.threshold_file_handler:                
            # Creation of df_threshold data frame:
            self.df_threshold = pd.read_csv(self.threshold_file, sep=C_SEPARATOR, comment=C_COMMENT, header = 0, skip_blank_lines=True)
