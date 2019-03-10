# -*- coding: utf-8 -*-
from pathlib import Path
from utils.common import *
from checks.checkInit import *
from checks.checkSinusPatterns import *
from checks.checkSquarePatterns import *
from checks.checkTrapezoidPatterns import *
from checks.checkBangBangPatterns import *
from checks.checkBlocs import *
from checks.checkID import *
from checks.checkFdir import *
from error.datdutErrors import *

p_datdut_dir = Path(C_DAT_DUT_DIR)

# for each dut file in the directory
for dat_dut_file in p_datdut_dir.glob('*.csv'):
    displayFileName(dat_dut_file.name)
    b_id_error_flag = False
    line_number = 0
        
    # opens and checks one file:
    with open (C_DAT_DUT_DIR + dat_dut_file.name,'r',encoding='utf8') as file_handler:
        # read and check each line of the file
        while True:
            line = file_handler.readline()
            line_number = line_number + 1
            
            # end of file
            if not line:
                break
            
            # do nothing for commentary, blank lines, and first line:
            if line.startswith(C_COMMENT) or len(line.strip()) == 0 or line_number == 1: 
                continue
            else:
                line = line.replace('\n','')
                liste = line.split(C_SEPARATOR)

                # Checks on the structure of line
                try:
                    # Object instanciation
                    init_checker = CheckInit(liste, line_number, getFUType(dat_dut_file.name))
                    # First checks
                    init_checker.checkInit()
                # main error: unable to determine the FU => move to next file
                except FilePrefixError:
                    print('Unable to set the FU type => no additional check for this file\n')
                    break
                # important error: line is inconsistent => move to next line
                except InitialChecksError as e:
                    print(e.args[0] + 'line ' + str(e.args[1]) + ' => no additional check for this line\n')
                    b_id_error_flag = True
                    continue
                # main characteristics are ok => check the line
                else:
                    # Check patterns
                    if init_checker.getDefinition() == 'PATTERN':
                        # Check sinus pattern
                        if init_checker.getType() == 'SINUS':
                            try:
                                sinus_pattern_checker = CheckSinusPatterns(init_checker)
                                sinus_pattern_checker.checkSinusPattern()
                            except SinusPatternsError as e:
                                print(e.args[0])
                        # Check square pattern
                        elif init_checker.getType() == 'SQUARE':
                            try:
                                square_pattern_checker = CheckSquarePatterns(init_checker)
                                square_pattern_checker.checkSquarePattern()
                            except SquarePatternsError as e:
                                print(e.args[0])
                        # Check bangbang pattern
                        elif init_checker.getType() == 'BANGBANG':
                            try:
                                bangbang_pattern_checker = CheckBangBangPatterns(init_checker)
                                bangbang_pattern_checker.checkBangBangPattern()
                            except BangBangPatternsError as e:
                                print(e.args[0])
                        # Check trapezoid pattern
                        elif init_checker.getType() == 'TRAPEZOID':
                            try:
                                trapezoid_pattern_checker = CheckTrapezoidPatterns(init_checker)
                                trapezoid_pattern_checker.checkTrapezoidPattern()
                            except TrapezoidPatternsError as e:
                                print(e.args[0])
                    # Check blocs
                    elif init_checker.getDefinition() == 'BLOC':
                            try:
                                bloc_checker = CheckBlocs(init_checker)
                                bloc_checker.checkBloc()
                            except BlocError as e:
                                print(e.args[0])
                    # Check fdir
                    elif init_checker.getDefinition() == 'FDIR':
                            try:
                                fdir_checker = CheckFDIR(init_checker)
                                fdir_checker.checkFdir()
                            except FdirError as e:
                                print(e.args[0])
        # if no error during checks of ids:
        if not b_id_error_flag:
            try:
                id_checker = CheckID(C_DAT_DUT_DIR + dat_dut_file.name)
                id_checker.checkIDs()
            except IDsError as e:
                print(e.args[0])

# print("\nStrike any key to quit...")
# input()
