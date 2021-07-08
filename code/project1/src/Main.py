# Example code that creates plots directly in report
# Code is an implementation of a genetic algorithm
import random
from matplotlib import pyplot as plt
from matplotlib import lines
import matplotlib.pyplot as plt
import numpy as np

from .Compile_latex import Compile_latex
from .Plot_to_tex import Plot_to_tex as plt_tex
from .Export_code_to_latex import export_code_to_latex

# define global variables for genetic algorithm example
string_length = 100
mutation_chance= 1.0/string_length
max_iterations = 1500

class Main:
    
    def __init__(self):
        pass
        
    def export_code_to_latex(self, project_nr):
        export_code_to_latex('main.tex', project_nr)
    
    def compile_latex_report(self,project_nr):
        '''compiles latex code to pdf'''
        compile_latex =Compile_latex(project_nr ,'main.tex')
            
    def addTwo(self,x):
        ''' adds two to the incoming integer and returns the result of the computation.'''
        return x+2

if __name__ == '__main__':
    # initialize main class
    main = Main()