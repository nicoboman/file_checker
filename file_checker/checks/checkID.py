'''
Created on 7 mars 2019

@author: nicolas
'''
import numpy as np

class CheckID(object):
    '''
    global checks on IDs
    '''


    def __init__(self, file):
        '''
        Constructor
        '''
        self.df = np.genfromtxt(file, dtype='str', comments='#', delimiter=',', skip_header=1, autostrip=True, encoding='utf-8')
        print(self.df)
        