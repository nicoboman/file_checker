# -*- coding: utf-8 -*-
class FilePrefixError(Exception):
    "error in prefix of csv file"    
    pass

class DataFrameCreatorError(Exception):
    "errors for creation of DataFrame from DAT DUT file"    
    pass

class CommonError(Exception):
    "errors for common check from DAT DUT file"    
    pass

class PatternsError(Exception):
    "errors for patterns check from DAT DUT file"    
    pass

class SinusPatternsError(Exception):
    "errors for sinus patterns check from DAT DUT file"    
    pass

class SquarePatternsError(Exception):
    "errors for square patterns check from DAT DUT file"    
    pass

class TrapezoidPatternsError(Exception):
    "errors for trapezoid patterns check from DAT DUT file"    
    pass

class BangBangPatternsError(Exception):
    "errors for bangbang patterns check from DAT DUT file"    
    pass

class BlocError(Exception):
    "errors for bloc check from DAT DUT file"    
    pass

