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
        self.tab_pattern_rows = self.df[self.df[:,C_DEFINITION_COLUMN] == 'PATTERN',:]
        self.tab_bloc_rows = self.df[self.df[:,C_DEFINITION_COLUMN] == 'BLOC',:]
        self.error_list = []
        self.error_string = ''
        
    def checkIDs(self):
        self.checkSinusPatternIDs()
        self.checkSquarePatternIDs()
        self.checkBangBangPatternIDs()
        self.checkTrapezoidPatternIDs()
        self.checkBlocIDs()
        self.checkSinusPatternsIDsInSinusBloc()
        self.checkSquarePatternsIDsInSquareBloc()
        self.checkBangBangPatternsIDsInBangBangBloc()
        self.checkTrapezoidPatternsIDsInBangBangBloc()
        
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
        self.tab_sinus_pattern_rows = self.tab_pattern_rows[self.tab_pattern_rows[:,C_TYPE_COLUMN] == 'SINUS',:]
        self.number_of_rows, self.number_of_columns = self.tab_sinus_pattern_rows.shape
        
        if self.number_of_rows <= 1:
            print('No sinus pattern or just 1 sinus pattern defined => no check of ids unicity...')
        else:
            self.tab_sinus_pattern_ids = self.tab_sinus_pattern_rows[:,2]
            
            if not self.isUniqueIDs(self.tab_sinus_pattern_ids):
                self.error_list.append('Sinus pattern ID\'s are not unique')
    
    def checkSquarePatternIDs(self):
        self.tab_square_pattern_rows = self.tab_pattern_rows[self.tab_pattern_rows[:,C_TYPE_COLUMN] == 'SQUARE',:]
        self.number_of_rows, self.number_of_columns = self.tab_square_pattern_rows.shape
        
        if self.number_of_rows <= 1:
            print('No square pattern or just 1 square pattern defined => no check of ids unicity...')
        else:
            self.tab_square_pattern_ids = self.tab_square_pattern_rows[:,C_ID_COLUMN]
            
            if not self.isUniqueIDs(self.tab_square_pattern_ids):
                self.error_list.append('Square pattern ID\'s are not unique')

    def checkBangBangPatternIDs(self):
        self.tab_bangbang_pattern_rows = self.tab_pattern_rows[self.tab_pattern_rows[:,C_TYPE_COLUMN] == 'BANGBANG',:]
        self.number_of_rows, self.number_of_columns = self.tab_bangbang_pattern_rows.shape
        
        if self.number_of_rows <= 1:
            print('No bangbang pattern or just 1 bangbang pattern defined => no check of ids unicity...')
        else:
            self.tab_bangbang_pattern_ids = self.tab_bangbang_pattern_rows[:,C_ID_COLUMN]
            
            if not self.isUniqueIDs(self.tab_bangbang_pattern_ids):
                self.error_list.append('Bangbang pattern ID\'s are not unique')
                
    def checkTrapezoidPatternIDs(self):
        self.tab_trapezoid_pattern_rows = self.tab_pattern_rows[self.tab_pattern_rows[:,C_TYPE_COLUMN] == 'TRAPEZOID',:]
        self.number_of_rows, self.number_of_columns = self.tab_trapezoid_pattern_rows.shape
        
        if self.number_of_rows <= 1:
            print('No trapezoid pattern or just 1 trapezoid pattern defined => no check of ids unicity...')
        else:
            self.tab_trapezoid_pattern_ids = self.tab_trapezoid_pattern_rows[:,C_ID_COLUMN]
            
            if not self.isUniqueIDs(self.tab_trapezoid_pattern_ids):
                self.error_list.append('Trapezoid pattern ID\'s are not unique')
                
    def checkBlocIDs(self):
        self.number_of_rows, self.number_of_columns = self.tab_bloc_rows.shape
        
        if self.number_of_rows == 1:
            print('Just 1 bloc defined => no check of id unicity...')
        else:
            self.tab_bloc_ids = self.tab_bloc_rows[:,C_ID_COLUMN]
            
            if not self.isUniqueIDs(self.tab_bloc_ids):
                self.error_list.append('Bloc pattern ID\'s are not unique')
                
    def checkSinusPatternsIDsInSinusBloc(self):
        self.sinus_bloc_row = self.tab_bloc_rows[self.tab_bloc_rows[:,C_TYPE_COLUMN] == 'SINUS',:]
        self.first_pattern = self.sinus_bloc_row[0,C_NB_ITEM_OR_FIRST_PATT_NUM]
        self.last_pattern = self.sinus_bloc_row[0,C_NB_REPET_OR_LAST_PATT_NUM_COLUMN]
        
        if not self.first_pattern in self.tab_sinus_pattern_ids:
            self.error_list.append('First sinus pattern in sinus bloc is not defined')

        if not self.last_pattern in self.tab_sinus_pattern_ids:
            self.error_list.append('Last sinus pattern in sinus bloc is not defined')

    def checkSquarePatternsIDsInSquareBloc(self):
        self.square_bloc_row = self.tab_bloc_rows[self.tab_bloc_rows[:,C_TYPE_COLUMN] == 'SQUARE',:]
        self.first_pattern = self.square_bloc_row[0,C_NB_ITEM_OR_FIRST_PATT_NUM]
        self.last_pattern = self.square_bloc_row[0,C_NB_REPET_OR_LAST_PATT_NUM_COLUMN]
        
        if not self.first_pattern in self.tab_square_pattern_ids:
            self.error_list.append('First square pattern in square bloc is not defined')

        if not self.last_pattern in self.tab_sinus_pattern_ids:
            self.error_list.append('Last square pattern in square bloc is not defined')
        
    def checkBangBangPatternsIDsInBangBangBloc(self):
        self.bangbang_bloc_row = self.tab_bloc_rows[self.tab_bloc_rows[:,C_TYPE_COLUMN] == 'BANGBANG',:]
        self.first_pattern = self.bangbang_bloc_row[0,C_NB_ITEM_OR_FIRST_PATT_NUM]
        self.last_pattern = self.bangbang_bloc_row[0,C_NB_REPET_OR_LAST_PATT_NUM_COLUMN]
        
        if not self.first_pattern in self.tab_bangbang_pattern_ids:
            self.error_list.append('First bangbang pattern in bangbang bloc is not defined')

        if not self.last_pattern in self.tab_sinus_pattern_ids:
            self.error_list.append('Last bangbang pattern in bangbang bloc is not defined')

    def checkTrapezoidPatternsIDsInBangBangBloc(self):
        self.trapezoid_bloc_row = self.tab_bloc_rows[self.tab_bloc_rows[:,C_TYPE_COLUMN] == 'TRAPEZOID',:]
        self.first_pattern = self.trapezoid_bloc_row[0,C_NB_ITEM_OR_FIRST_PATT_NUM]
        self.last_pattern = self.trapezoid_bloc_row[0,C_NB_REPET_OR_LAST_PATT_NUM_COLUMN]
        
        if not self.first_pattern in self.tab_trapezoid_pattern_ids:
            self.error_list.append('First trapezoid pattern in trapezoid bloc is not defined')

        if not self.last_pattern in self.tab_sinus_pattern_ids:
            self.error_list.append('Last trapezoid pattern in trapezoid bloc is not defined')
