# -*- coding: utf-8 -*-

from pathlib import Path
from utils.common import *
from checks.checkInit import *
from checks.checkSinusPatterns import *
from checks.checkSquarePatterns import *
from checks.checkTrapezoidPatterns import *
from checks.checkBangBangPatterns import *
# from checks.checkBlocs import *
from error.datdutErrors import *

p_datdut_dir = Path(C_DAT_DUT_DIR)

l_sinus_pattern_ids = []
l_square_pattern_ids = []
l_bangbang_pattern_ids = []
l_trapezoid_pattern_ids = []

for dat_dut_file in p_datdut_dir.glob('*.csv'):
    displayFileName(dat_dut_file.name)
    
    # emptying list of ids before checking new file
    l_sinus_pattern_ids.clear()
    l_square_pattern_ids.clear()
    l_bangbang_pattern_ids.clear()
    l_trapezoid_pattern_ids.clear()
    
    with open (C_DAT_DUT_DIR + dat_dut_file.name,'r',encoding='utf8') as file_handler:
        line_number = 0
        
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
                except FilePrefixError:
                    print('Unable to set the FU type => no additional check for this file\n')
                    break
                except InitialChecksError as e:
                    print(e.args[0] + 'line ' + str(e.args[1]) + ' => no additional check for this line\n')
                    continue
                else:
                    # Check patterns
                    if init_checker.getDefinition() == 'PATTERN':
                        # Check sinus pattern
                        if init_checker.getType() == 'SINUS':
                            try:
                                sinus_pattern_checker = CheckSinusPatterns(init_checker, l_sinus_pattern_ids)
                                sinus_pattern_checker.checkSinusPattern()
                            except SinusPatternsError as e:
                                print(e.args[0])
                        # Check square pattern
                        elif init_checker.getType() == 'SQUARE':
                            try:
                                square_pattern_checker = CheckSquarePatterns(init_checker, l_square_pattern_ids)
                                square_pattern_checker.checkSquarePattern()
                            except SquarePatternsError as e:
                                print(e.args[0])
                        # Check bangbang pattern
                        elif init_checker.getType() == 'BANGBANG':
                            try:
                                bangbang_pattern_checker = CheckBangBangPatterns(init_checker, l_bangbang_pattern_ids)
                                bangbang_pattern_checker.checkBangBangPattern()
                            except BangBangPatternsError as e:
                                print(e.args[0])
                        # Check trapezoid pattern
                        elif init_checker.getType() == 'TRAPEZOID':
                            try:
                                trapezoid_pattern_checker = CheckTrapezoidPatterns(init_checker, l_trapezoid_pattern_ids)
                                trapezoid_pattern_checker.checkTrapezoidPattern()
                            except TrapezoidPatternsError as e:
                                print(e.args[0])

#             if not pattern_check_error:
#                 # no error during pattern checks => bloc checks
#                 try:
#                     # Checks of Bloc rows of DAT DUT file
#                     bloc_checker.checkBlocIDsUnique()
#                     bloc_checker.checkFirstPattNumisInteger()
#                     bloc_checker.checkLastPattNumisInteger()
#                     bloc_checker.checkSeqNum()
#                     bloc_checker.checkAxis()
#                     bloc_checker.checkFirstAndLastSinusPatternNum(sinus_pattern_checker)
#                     bloc_checker.checkFirstAndLastSquarePatternNum(square_pattern_checker)
#                     bloc_checker.checkFirstAndLastTrapezoidPatternNum(trapezoid_pattern_checker)
#                     bloc_checker.checkFirstAndLastBangbangPatternNum(bangbang_pattern_checker)
#                     bloc_checker.checkMandatoryOrPointlessParameters()
#                 except BlocError as e:
#                     print(e.args[0], end = "")
#                     [print(exception_info, end = "") for exception_info in e.args[1]]
#                     print('\n', end = "")
#                 else:
#                     print("[OK] No error in " + dat_dut_file.name)

# print("\nStrike any key to quit...")
# input()
