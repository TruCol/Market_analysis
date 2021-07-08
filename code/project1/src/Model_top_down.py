# The bottom up model that computes the TAM and TSM
import random
from matplotlib import pyplot as plt
from matplotlib import lines
import matplotlib.pyplot as plt
import numpy as np

from .Plot_to_tex import Plot_to_tex as plt_tex


class Model_bottom_up:
    
    def __init__(self):
        pass
                
    def addTwo(self,x):
        ''' adds two to the incoming integer and returns the result of the computation.'''
        return x+2