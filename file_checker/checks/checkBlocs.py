# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.common import *
from checks.checkDATDUT import *
from error.datdutErrors import *

class CheckBlocs(CheckDATDUT):
    "check blocs from DAT DUT file"
    
    def __init__(self, data_frame, fu_type):
        CheckDATDUT.__init__(self, data_frame, fu_type)
        
        # Select bloc rows
        self.df_bloc_rows = self.df_dat_dut[self.df_dat_dut.definition == "bloc"]
        
        # Select sinus bloc rows
        self.df_sinus_bloc_rows = self.df_bloc_rows[self.df_bloc_rows.type == "sinus"]

        # Select square bloc rows
        self.df_square_bloc_rows = self.df_bloc_rows[self.df_bloc_rows.type == "square"]
        
        # Select trapezoid bloc rows
        self.df_trapezoid_bloc_rows = self.df_bloc_rows[self.df_bloc_rows.type == "trapezoid"]

        # Select bangbang bloc rows
        self.df_bangbang_bloc_rows = self.df_bloc_rows[self.df_bloc_rows.type == "bangbang"]
        
        # List of position of first pattern num and last pattern num in DAT DUT file for bloc definition
        self.l_pattern_ids_columns = [C_NB_ITEM_OR_FIRST_PATT_NUM, C_NB_REPET_OR_LAST_PATT_NUM_COLUMN]
        
    def checkBlocIDsUnique(self):
        self.temp_df = self.df_bloc_rows.loc[:,'id']
        
        if not self.temp_df.is_unique:
            self.temp_df = self.df_bloc_rows.loc[:, 'line':'id':C_ID_COLUMN]
            raise BlocError("[Bloc Error]: Bloc id's are not unique, see below: \n", self.temp_df.values)
    
    def checkFirstPattNumisInteger(self):
        # first pattern number must always be an integer        
        for i in range(self.df_bloc_rows.shape[0]):
            if not isInteger(self.df_bloc_rows.iloc[i,C_NB_ITEM_OR_FIRST_PATT_NUM]):
                raise BlocError("[Bloc Error]: first pattern number is not an integer in line: ", self.df_bloc_rows.iloc[i,C_LINE_COLUMN])
            
    def checkLastPattNumisInteger(self):
        # last pattern number must always be an integer        
        for i in range(self.df_bloc_rows.shape[0]):
            if not isInteger(self.df_bloc_rows.iloc[i,C_NB_REPET_OR_LAST_PATT_NUM_COLUMN]):
                raise BlocError("[Bloc Error]: last pattern number is not an integer in line: ", self.df_bloc_rows.iloc[i,C_LINE_COLUMN])
    
    def checkSeqNum(self):
        # get lines where:
        #   - id column <= 0
        # then return line and id columns for those lines
        self.temp_df = self.df_bloc_rows.loc[(self.df_bloc_rows.loc[:, 'id'] <= 0),'line':'id':C_ID_COLUMN]
        
        if not self.temp_df.empty:
            raise BlocError("[Bloc Error]: seq num <= 0 in line(s) below: ", self.temp_df.values)
            
    def checkAxis(self):
        # get lines where:
        #   - axis column != "U"
        # AND where:
        # - axis column != "V"
        # AND where:
        # - axis column != "+U+V"
        # AND where:
        # - axis column != "+U-V"
        # then return line and axis columns for those lines
        self.temp_df = self.df_bloc_rows.loc[(self.df_dat_dut.loc[:, 'axis'] != 'U')
                        & (self.df_bloc_rows.loc[:, 'axis'] != 'V')
                        & (self.df_bloc_rows.loc[:, 'axis'] != '+U+V')
                        & (self.df_bloc_rows.loc[:, 'axis'] != '+U-V'),
                        'line':'axis':C_AXIS_COLUMN]
    
        if not self.temp_df.empty:
            raise BlocError("[Bloc Error]: Unknown axis in line(s) below: ", self.temp_df.values)
            
    # In blocs, check if all first and last sinus pattern id's are defined
    def checkFirstAndLastSinusPatternNum(self, sinus_patt_rows):
        b_is_defined = False

        for pattern_id in self.l_pattern_ids_columns:
            for i in range(self.df_sinus_bloc_rows.shape[0]):
                b_is_defined = False
                
                for j in range(sinus_patt_rows.df_sinus_pattern_rows.shape[0]):
                    if (self.df_sinus_bloc_rows.iloc[i,pattern_id] == sinus_patt_rows.df_sinus_pattern_rows.iloc[j,C_ID_COLUMN]):
                        b_is_defined = True
                        break
                
                if not b_is_defined:
                    raise BlocError("[Bloc Error]: Undefined sinus pattern number - line: ", 
                                    [self.df_sinus_bloc_rows.iloc[i,C_LINE_COLUMN], 
                                    " sinus pattern id: ", 
                                    self.df_sinus_bloc_rows.iloc[i,pattern_id]])

    # In blocs, check if all first and last square pattern id's are defined
    def checkFirstAndLastSquarePatternNum(self, square_patt_rows):
        b_is_defined = False
        
        for pattern_id in self.l_pattern_ids_columns:
            for i in range(self.df_square_bloc_rows.shape[0]):
                b_is_defined = False
                
                for j in range(square_patt_rows.df_square_pattern_rows.shape[0]):
                    if (self.df_square_bloc_rows.iloc[i,pattern_id] == square_patt_rows.df_square_pattern_rows.iloc[j,C_ID_COLUMN]):
                        b_is_defined = True
                        break
                
                if not b_is_defined:
                    raise BlocError("[Bloc Error]: Undefined square pattern number - line: ", 
                                    [self.df_square_bloc_rows.iloc[i,C_LINE_COLUMN], 
                                    " square pattern id: ", 
                                    self.df_square_bloc_rows.iloc[i,pattern_id]])


    # In blocs, check if all first and last trapezoid pattern id's are defined
    def checkFirstAndLastTrapezoidPatternNum(self, trapezoid_patt_rows):
        b_is_defined = False
        
        for pattern_id in self.l_pattern_ids_columns:
            for i in range(self.df_trapezoid_bloc_rows.shape[0]):
                b_is_defined = False
                
                for j in range(trapezoid_patt_rows.df_trapezoid_pattern_rows.shape[0]):
                    if (self.df_trapezoid_bloc_rows.iloc[i,pattern_id] == trapezoid_patt_rows.df_trapezoid_pattern_rows.iloc[j,C_ID_COLUMN]):
                        b_is_defined = True
                        break
                
                if not b_is_defined:
                    raise BlocError("[Bloc Error]: Undefined trapezoid pattern number - line: ", 
                                    [self.df_trapezoid_bloc_rows.iloc[i,C_LINE_COLUMN], 
                                    " trapezoid pattern id: ", 
                                    self.df_trapezoid_bloc_rows.iloc[i,pattern_id]])

    # In blocs, check if all first and last bangbang pattern id's are defined
    def checkFirstAndLastBangbangPatternNum(self, bangbang_patt_rows):
        b_is_defined = False
        
        for pattern_id in self.l_pattern_ids_columns:
            for i in range(self.df_bangbang_bloc_rows.shape[0]):
                b_is_defined = False
                
                for j in range(bangbang_patt_rows.df_bangbang_pattern_rows.shape[0]):
                    if (self.df_bangbang_bloc_rows.iloc[i,pattern_id] == bangbang_patt_rows.df_bangbang_pattern_rows.iloc[j,C_ID_COLUMN]):
                        b_is_defined = True
                        break
                
                if not b_is_defined:
                    raise BlocError("[Bloc Error]: Undefined bangbang pattern number - line: ", 
                                    [self.df_bangbang_bloc_rows.iloc[i,C_LINE_COLUMN], 
                                    " bangbang pattern id: ", 
                                    self.df_bangbang_bloc_rows.iloc[i,pattern_id]])


    def checkMandatoryOrPointlessParameters(self):
        # check mandatory parameters are mentioned
        # check pointless parameters for bloc are missing
        bloc_mask = np.array([True, True, True, True, True, True, False, False, False, False, True, True, False, False])
                
        for i in range(self.df_bloc_rows.shape[0]):
            bloc_parameter_presence = np.array(self.df_bloc_rows.iloc[i,:].notna())
            if not np.array_equal(bloc_mask, bloc_parameter_presence):
                raise BlocError("[Bloc Error]: mandatory parameter missing or pointless parameter specified in line: ", [self.df_bloc_rows.iloc[i,C_LINE_COLUMN]])
