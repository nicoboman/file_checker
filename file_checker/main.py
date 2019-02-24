# -*- coding: utf-8 -*-

from pathlib import Path
from utils.common import *
# from checks.checkDATDUT import *
# from checks.checkPatterns import *
# from checks.checkSinusPatterns import *
# from checks.checkSquarePatterns import *
# from checks.checkTrapezoidPatterns import *
# from checks.checkBangBangPatterns import *
# from checks.checkBlocs import *
from error.datdutErrors import *

p_datdut_dir = Path(C_DAT_DUT_DIR)

for dat_dut_file in p_datdut_dir.glob('*.csv'):
    displayFileName(dat_dut_file.name)
    
    with open (C_DAT_DUT_DIR + dat_dut_file.name,'r',encoding='utf8') as file_handler:
        # read of first line:
        line = file_handler.readline()
        line_number = 1 
        
        while line:
            line = file_handler.readline()
            line_number = line_number + 1
            # do nothing for commentary or blank lines:
            if line.startswith(C_COMMENT) or len(line.strip()) == 0:
                continue
            else:
                liste = line.split(C_SEPARATOR)
                # delete last character (jump to next line character)
                del(liste[-1])
                
                # Checks on the structure of line
                try:
                    # elementary checks on the structure of line, definition and type
                    if len(liste) != C_NB_OF_FIELD:
                        raise InitialChecksError("[Initial Checks Error]: invalid number of fields in line: ", line_number)
                    elif liste[C_DEFINITION_COLUMN] not in ['pattern', 'bloc']:
                        raise InitialChecksError("[Initial Checks Error]: invalid definition in line: ", line_number)
                    elif liste[C_TYPE_COLUMN] not in ['sinus', 'square', 'trapezoid', 'bangbang']:
                        raise InitialChecksError("[Initial Checks Error]: invalid type in line: ", line_number)
                except (InitialChecksError) as e:
                    print(e.args[0], e.args[1], '=> no additionnal check for this line')


        



    
#     pattern_check_error = False
    
#     try:
#         # Reading and analyzing each line of file
#         with open (dat_dut_file.name,'r',encoding='utf8') as file_handler:
#             line = file_handler.readline()

#     except DataFrameCreatorError as e:
#         print(e.args[0])
#     else:
#         # no error during creation of dataframe => common cheks
#         try:
#             # Objects instanciation
#             fu_type = getFUType(dat_dut_file.name)
#             common_checker = CheckDATDUT(df, fu_type)
#             pattern_checker = CheckPatterns(df, fu_type)
#             sinus_pattern_checker = CheckSinusPatterns(df, fu_type)
#             square_pattern_checker = CheckSquarePatterns(df, fu_type)
#             trapezoid_pattern_checker = CheckTrapezoidPatterns(df, fu_type)
#             bangbang_pattern_checker = CheckBangBangPatterns(df, fu_type)
#             bloc_checker = CheckBlocs(df, fu_type)
#         
#             # Common checks of DAT DUT file
#             common_checker.checkDefinitionColumn()
#             common_checker.checkTypeColumn()
#             common_checker.checkIDColumn()
#             common_checker.checkIDisInteger()
#         except (CommonError, FilePrefixError) as e:
#             print(e.args[0], e.args[1])
#         else:            
#             # no error during common checks => pattern checks
#             try:
#                 # Checks of Pattern rows of DAT DUT file
#                 pattern_checker.check600HzCommand()
#             except PatternsError as e:
#                 print(e.args[0], e.args[1])
#             
#             try:
#                 # Specific checks for sinus patterns
#                 sinus_pattern_checker.setSinusPatternThreshold()
#                 sinus_pattern_checker.checkSinusPatternIDsUnique()
#                 sinus_pattern_checker.checkAmplitude()
#                 sinus_pattern_checker.checkNbOfPoints()
#                 sinus_pattern_checker.checkNbOfPointsisInteger()
#                 sinus_pattern_checker.checkNbOfRepet()
#                 sinus_pattern_checker.checkNbOfRepetisInteger()
#                 sinus_pattern_checker.checkMandatoryOrPointlessParameters()
#                 sinus_pattern_checker.checkSinusDelay()
#                 sinus_pattern_checker.checkOffset()
#             except SinusPatternsError as e:
#                 print(e.args[0], e.args[1])
#                 pattern_check_error = True
#             
#             try:
#                 # Specific checks for square patterns
#                 square_pattern_checker.checkSquarePatternIDsUnique()
#                 square_pattern_checker.checkNbOfSteps()
#                 square_pattern_checker.checkNbOfStepsisInteger()
#                 square_pattern_checker.checkNbOfStepsIsEven()
#                 square_pattern_checker.checkStepDuration()
#                 square_pattern_checker.checkIncrement()
#                 square_pattern_checker.checkMandatoryOrPointlessParameters()
#                 square_pattern_checker.checkOffset()
#             except SquarePatternsError as e:
#                 print(e.args[0], e.args[1])
#                 pattern_check_error = True
#             
#             try:
#                 # Specific checks for trapezoid patterns
#                 trapezoid_pattern_checker.checkTrapezoidPatternIDsUnique()
#                 trapezoid_pattern_checker.checkSlope()
#                 trapezoid_pattern_checker.checkStepDuration()
#                 trapezoid_pattern_checker.checkIntervalDuration()
#                 trapezoid_pattern_checker.checkMandatoryOrPointlessParameters()
#                 trapezoid_pattern_checker.checkPosInit()
#                 trapezoid_pattern_checker.checkPosTarget(1)
#                 trapezoid_pattern_checker.checkPosTarget(2)
#             except TrapezoidPatternsError as e:
#                 print(e.args[0], e.args[1])
#                 pattern_check_error = True
#             
#             try:
#                 # Specific checks for bangbang patterns
#                 bangbang_pattern_checker.checkDelay()
#                 bangbang_pattern_checker.checkOffset()
#                 bangbang_pattern_checker.checkPosTarget()
#                 bangbang_pattern_checker.checkBangBangPatternIDsUnique()
#                 bangbang_pattern_checker.checkSlope()
#                 bangbang_pattern_checker.checkMandatoryOrPointlessParameters()
#             except BangBangPatternsError as e:
#                 print(e.args[0], e.args[1])
#                 pattern_check_error = True
#                 
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
