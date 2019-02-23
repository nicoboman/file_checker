# -*- coding: utf-8 -*-
import pandas as pd
from utils.common import *
from error.datdutErrors import *

class CheckDATDUT:
    "read and check DAT_DUT file"
    
    def __init__(self, data_frame, fu_type):
        self.df_dat_dut = data_frame
        
        # SR, LL or UL
        self.fu_type = fu_type

    def checkDefinitionColumn(self):
        # get lines where:
        #   - definition column != pattern
        # AND where:
        # - definition column != bloc
        # then return line and definition columns for those lines
        self.temp_df = self.df_dat_dut.loc[(self.df_dat_dut.loc[:, 'definition'] != 'pattern') 
                        & (self.df_dat_dut.loc[:, 'definition'] != 'bloc'),
                        'line':'definition']
        
        if not self.temp_df.empty:
            raise CommonError("[DATDUT Error]: Unknown definition(s) in line(s) below: \n", self.temp_df.values)
            
    def checkTypeColumn(self):
        # get lines where:
        #   - type column != sinus
        # AND where:
        # - type column != square
        # AND where:
        # - type column != bangbang
        # AND where:
        # - type column != trapezoid
        # then return line and type columns for those lines
        self.temp_df = self.df_dat_dut.loc[(self.df_dat_dut.loc[:, 'type'] != 'sinus')
                        & (self.df_dat_dut.loc[:, 'type'] != 'square')
                        & (self.df_dat_dut.loc[:, 'type'] != 'bangbang')
                        & (self.df_dat_dut.loc[:, 'type'] != 'trapezoid'),
                        'line':'type':2]
    
        if not self.temp_df.empty:
            raise CommonError("[DATDUT Error]: Unknown type(s) in line(s) below: \n", self.temp_df.values)
                
    def checkIDColumn(self):
        # get lines where:
        #   - id < 0
        # then return line and id columns for those lines
        self.temp_df = self.df_dat_dut.loc[(self.df_dat_dut.loc[:, 'id'] < 0),'line':'id':C_ID_COLUMN]

        if not self.temp_df.empty:
            raise CommonError("[DATDUT Error]: id(s) < 0 in line(s) below: \n", self.temp_df.values)
    
    def checkIDisInteger(self):
        # id must always be an integer        
        for i in range(self.df_dat_dut.shape[0]):
            if not isInteger(self.df_dat_dut.iloc[i,C_ID_COLUMN]):
                raise CommonError("[DATDUT Error]: ID is not an integer in line: ", self.df_dat_dut.iloc[i,C_LINE_COLUMN])
