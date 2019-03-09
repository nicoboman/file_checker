# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.common import *
from error.datdutErrors import *

class CheckBlocs():
    "check blocs of dut file"
    
    def __init__(self, obj_init):
        self.liste = obj_init.getListe()
        self.line_number = obj_init.getLineNumber()
        self.error_list = []
        self.error_string = ''
            
    def checkBloc(self):
        self.checkMandatoryOrPointlessParameters()
        self.checkIsNumber()

        # if an error occured during check of manadatory parameters
        # do not proceed the other checks (no point doing it because maybe parameter is not defined):
        if len(self.error_list):
            self.error_list.append('line ' + str(self.line_number) + ' error in type/structure of parameters => no additionnal check for this line')
        else:
            self.checkAxis()
#             self.checkBlocIDsUnique()
#             self.checkFirstAndLastSinusPatternNum(sinus_pattern_checker)
#             self.checkFirstAndLastSquarePatternNum(square_pattern_checker)
#             self.checkFirstAndLastTrapezoidPatternNum(trapezoid_pattern_checker)
#             self.checkFirstAndLastBangbangPatternNum(bangbang_pattern_checker)

        # raises an error if necessary:
        if len(self.error_list):
            while self.error_list:
                try:
                    self.error_string = self.error_string + self.error_list.pop(0) + '\n'
                except IndexError:
                    break
            
            raise BlocError(self.error_string)

    def checkIsNumber(self):
        if not isNumber(self.liste[C_DELAY_OR_STEP_DURATION_COLUMN]):
            self.error_list.append('line ' + str(self.line_number) + ' delay is not a number')

        if not isNumber(self.liste[C_NB_ITEM_OR_FIRST_PATT_NUM]):
            self.error_list.append('line ' + str(self.line_number) + ' first pattern is not a number')

        if not isNumber(self.liste[C_NB_REPET_OR_LAST_PATT_NUM_COLUMN]):
            self.error_list.append('line ' + str(self.line_number) + ' delay is not a number')
                
    def checkAxis(self):
        if self.liste[C_AXIS_COLUMN] not in ['U', 'V', '+U-V', '-U+V']:
            self.error_list.append('line ' + str(self.line_number) + ' invalid axis')
            
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
        # check pointless parameters for square patterns are missing
        bloc_pattern_mask = np.array([True, True, True, True, True, False, False, False, True, True, False, False, False])
                
        # structure of the processed line
        bloc_pattern_presence = np.array(list(map(lambda x: True if len(x) > 0 else False, self.liste)), dtype = bool)
        
        # compare the two of them
        if not np.array_equal(bloc_pattern_mask, bloc_pattern_presence):
            self.error_list.append('line ' + str(self.line_number) + ' mandatory parameter absent or pointless parameter')
