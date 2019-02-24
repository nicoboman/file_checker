# -*- coding: utf-8 -*-
import pandas as pd
from utils.common import *
from error.datdutErrors import *
from checks.checkDATDUT import *

class CheckPatterns():
    "check patterns from DAT DUT file"
    
    def __init__(self, data_frame, fu_type):
        CheckDATDUT.__init__(self, data_frame, fu_type)
        
        # Select pattern rows
        self.df_pattern_rows = self.df_dat_dut[self.df_dat_dut.definition == "pattern"]
    
    def check600HzCommand(self):
        # get lines where:
        #   - is_600Hz_cmd column != True
        # AND where:
        # - is_600Hz_cmd column != False
        # then return line and is_600Hz_cmd columns for those lines
        self.temp_df = self.df_pattern_rows.loc[(self.df_pattern_rows.loc[:, 'is_600Hz_cmd'] != True) 
                        & (self.df_pattern_rows.loc[:, 'is_600Hz_cmd'] != False),
                        'line':'is_600Hz_cmd':C_IS_600HZ_CMD_COLUMN]
        
        # /!\ TODO: investigations à mener
        # si on positionne une valeur dans le champs is_600Hz_cmd d'une ligne bloc
        # alors cette fonction détecte une erreur... pourquoi...??
        # alors que le traitement est effectué sur self.temp_df issue de self.df_pattern_rows qui filtre sur les lignes 'pattern'
        
        if not self.temp_df.empty:
            print(self.df_pattern_rows.loc[:,'is_600Hz_cmd'])
            raise PatternsError("[Pattern Error]: Unknown is_600Hz_cmd(s) in line(s) below:\n", self.temp_df.values)
