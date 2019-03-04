from error.datdutErrors import *

# Files and directories:
C_DAT_DUT_DIR='.\\datdutfiles\\'
C_DAT_DUT_FILE_NAME_TEMP=C_DAT_DUT_DIR + 'dat_dut_file_temp.csv'
C_THRESHOLD_DIR='.\\property\\'

# UL
C_UL_SINUS_THRESHOLD_FILE = "ul_sinus_pattern.properties"
C_UL_SQUARE_THRESHOLD_FILE = "ul_square_pattern.properties"
C_UL_TRAPEZOID_THRESHOLD_FILE = "ul_trapezoid_pattern.properties"
C_UL_BANGBANG_THRESHOLD_FILE = "ul_bangbang_pattern.properties"

# SR
C_SR_SINUS_THRESHOLD_FILE = "sr_sinus_pattern.properties"
C_SR_SQUARE_THRESHOLD_FILE = "sr_square_pattern.properties"
C_SR_TRAPEZOID_THRESHOLD_FILE = "sr_trapezoid_pattern.properties"
C_SR_BANGBANG_THRESHOLD_FILE = "sr_bangbang_pattern.properties"

# LL
C_LL_SINUS_THRESHOLD_FILE = "ll_sinus_pattern.properties"
C_LL_SQUARE_THRESHOLD_FILE = "ll_square_pattern.properties"
C_LL_TRAPEZOID_THRESHOLD_FILE = "ll_trapezoid_pattern.properties"
C_LL_BANGBANG_THRESHOLD_FILE = "ll_bangbang_pattern.properties"

# CSV File structure:

C_SEPARATOR=','
C_COMMENT='#'
C_NB_OF_FIELD = 13
C_EXIT_SUCCESS=0
C_EXIT_FAILURE=1
C_LINE_COLUMN=0
C_DEFINITION_COLUMN=0
C_TYPE_COLUMN=1
C_ID_COLUMN=2
C_DELAY_OR_STEP_DURATION_COLUMN=3
C_AXIS_COLUMN=5
C_OFFSET_COLUMN=5
C_IS_600HZ_CMD_COLUMN=6
C_AMPL_OR_STEP_INC_OR_FINAL_POS1_COLUMN=7
C_FINAL_POS2_COLUMN=10
C_NB_ITEM_OR_FIRST_PATT_NUM = 8
C_NB_REPET_OR_LAST_PATT_NUM_COLUMN=9
C_SLOPE_COLUMN=11
C_INTERVAL_DURATION_COLUMN=12

# Miscellaneous:
def isInteger(number):
    b_is_integer = False
    
    if number - int(number):
        b_is_integer = False
    else:
        b_is_integer = True
    
    return b_is_integer

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def displayFileName(file_name):
    print('\n' + "-" * len(file_name))
    print(file_name)
    print("-" * len(file_name))
    
def getFUType(file_name):
    fu_type = 'undef'
    fu_type = file_name[0:2]
    if fu_type != 'SR' and fu_type != 'LL' and fu_type != 'UL':
        raise FilePrefixError("error in prefix of csv file - must be SR_, LL_ or UL_", None)
        
    return fu_type
        