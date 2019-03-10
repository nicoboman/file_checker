'''
Created on 7 mars 2019

@author: nicolas
'''
import numpy as np
from utils.common import *
from error.datdutErrors import *

class CheckID(object):
    '''
    global checks on IDs
    '''

    def __init__(self, file):
        '''
        Constructor
        '''
        self.df = np.genfromtxt(file, dtype='str', comments='#', delimiter=',', skip_header=1, autostrip=True, encoding='utf-8')
        self.tab_pattern_rows = self.df[self.df[:,0] == 'PATTERN',:]
        self.error_list = []
        self.error_string = ''
        
    def checkIDs(self):
        self.checkSinusPatternIDs()
        self.checkSquarePatternIDs()
        self.checkBangBangPatternIDs()
        self.checkTrapezoidPatternIDs()
        
        # raises an error if necessary:
        if len(self.error_list):
            while self.error_list:
                try:
                    self.error_string = self.error_string + self.error_list.pop(0) + '\n'
                except IndexError:
                    break
            
            raise IDsError(self.error_string)
        
    def isUniqueIDs(self, tab):
        self.tab_unique = np.unique(tab)
        self.is_unique = False
        
        if self.tab_unique.size == tab.size:
            self.is_unique = True
        else:
            self.is_unique = False
            
        return self.is_unique

    def checkSinusPatternIDs(self):
        self.tab_sinus_pattern_rows = self.tab_pattern_rows[self.tab_pattern_rows[:,1] == 'SINUS',:]
        self.number_of_rows, self.number_of_columns = self.tab_sinus_pattern_rows.shape
        
        if self.number_of_rows <= 1:
            print('No sinus pattern or just 1 sinus pattern defined => no check of ids unicity...')
        else:
            self.tab_sinus_pattern_ids = self.tab_sinus_pattern_rows[:,2]
            
            if not self.isUniqueIDs(self.tab_sinus_pattern_ids):
                self.error_list.append('Sinus pattern ID\'s are not unique')
    
    def checkSquarePatternIDs(self):
        self.tab_square_pattern_rows = self.tab_pattern_rows[self.tab_pattern_rows[:,1] == 'SQUARE',:]
        self.number_of_rows, self.number_of_columns = self.tab_square_pattern_rows.shape
        
        if self.number_of_rows <= 1:
            print('No square pattern or just 1 square pattern defined => no check of ids unicity...')
        else:
            self.tab_square_pattern_ids = self.tab_square_pattern_rows[:,2]
            
            if not self.isUniqueIDs(self.tab_square_pattern_ids):
                self.error_list.append('Square pattern ID\'s are not unique')

    def checkBangBangPatternIDs(self):
        self.tab_bangbang_pattern_rows = self.tab_pattern_rows[self.tab_pattern_rows[:,1] == 'BANGBANG',:]
        self.number_of_rows, self.number_of_columns = self.tab_bangbang_pattern_rows.shape
        
        if self.number_of_rows <= 1:
            print('No bangbang pattern or just 1 bangbang pattern defined => no check of ids unicity...')
        else:
            self.tab_bangbang_pattern_ids = self.tab_bangbang_pattern_rows[:,2]
            
            if not self.isUniqueIDs(self.tab_bangbang_pattern_ids):
                self.error_list.append('Bangbang pattern ID\'s are not unique')
                
    def checkTrapezoidPatternIDs(self):
        self.tab_trapezoid_pattern_rows = self.tab_pattern_rows[self.tab_pattern_rows[:,1] == 'TRAPEZOID',:]
        self.number_of_rows, self.number_of_columns = self.tab_trapezoid_pattern_rows.shape
        
        if self.number_of_rows <= 1:
            print('No trapezoid pattern or just 1 trapezoid pattern defined => no check of ids unicity...')
        else:
            self.tab_trapezoid_pattern_ids = self.tab_trapezoid_pattern_rows[:,2]
            
            if not self.isUniqueIDs(self.tab_trapezoid_pattern_ids):
                self.error_list.append('Trapezoid pattern ID\'s are not unique')
