# -*- coding: utf-8 -*-
import pandas as pd
from pathlib import Path
from utils.common import *
from error.datdutErrors import *

class DataFrameCreator:
    "create data frame from DATDUT file"
    
    def __init__(self, dat_dut_file):
        if not Path(dat_dut_file).exists():
            raise DataFrameCreatorError("[DataFrame Creator Error]: datdut file does not exist.")
            
        if Path(C_DAT_DUT_FILE_NAME_TEMP).exists():
            raise DataFrameCreatorError("[DataFrame Creator Error]: temporary file already exists")
            
        self.dat_dut_file = dat_dut_file
        
    def createDataFrame(self):
        with open (self.dat_dut_file,'r',encoding='utf8') as self.dat_dut_file_handler:
            with open (C_DAT_DUT_FILE_NAME_TEMP,'w+',encoding='utf8') as self.dat_dut_file_tmp_handler:
                self.createLineNumberedDATDUTFile()
                
            # Creation of df_dat_dut data frame:
            self.df_dat_dut = pd.read_csv(C_DAT_DUT_FILE_NAME_TEMP, sep=C_SEPARATOR, comment=C_COMMENT, header = 0, skip_blank_lines=True)

        # remove temporary datdut file
        Path(C_DAT_DUT_FILE_NAME_TEMP).unlink()
    
    def getDataFrame(self):
        return self.df_dat_dut

    def createLineNumberedDATDUTFile(self):
        numberOfLines = 0
        
        for line in self.dat_dut_file_handler:
            numberOfLines += 1
            if numberOfLines == 1:
                newstring = "line" + C_SEPARATOR + line
                self.dat_dut_file_tmp_handler.write(newstring)
            elif line[0] == '\n':
                self.dat_dut_file_tmp_handler.write('\n')
            elif line[0] == '#':
                self.dat_dut_file_tmp_handler.write(line)
            else:
                newstring = str(numberOfLines) + C_SEPARATOR + line
                self.dat_dut_file_tmp_handler.write(newstring)
