'''
Created on 7 mars 2019

@author: nicolas
'''
import numpy as np
from utils.common import *

class CheckID(object):
    '''
    global checks on IDs
    '''


    def __init__(self, file):
        '''
        Constructor
        '''
        self.df = np.genfromtxt(file, dtype='str', comments='#', delimiter=',', skip_header=1, autostrip=True, encoding='utf-8')
#         print(self.df)
        
    def checkSinusIDs(self):
        tab_definition = self.df[:,0:3]
        number_of_rows, number_of_columns = self.df.shape
        
        print(tab_definition)
        b = tab_definition[tab_definition[:,0] == 'PATTERN',:]
        print(b)
        c = b[b[:,1] == 'SINUS',:]
        print(c)
        d = c[:,2]
        print(d)
        
        e = np.unique(d)
        
        print(e)
        print(e.size)

        if e.size == d.size:
            print('OK')
        else:
            print('NOK..!!')

        
#         cond_list = [tab_definition[:,0] == 'PATTERN']
#         choice_list = [tab_definition]
#         b = np.select(cond_list,choice_list)
#         print(b)
#         

        