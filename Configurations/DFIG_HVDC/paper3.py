# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 16:50:48 2023

@author: Gregory_Guo
"""

"""
This is the Program for DFIG System model identification
based on DATA driven methods called SINDy

The whole procedures are divided into three parts:
    data collection for x dot
    library construction
    constraint and optimization

each part has its own defined function
which is easy to reuse for different blocks

more advanced function of the program
1.noise for the initial data, so necessary to use appropriate difference method
2.auto-encoder for high dimension states
3.constraints for each physical blocks, so proper optimization method is used
4.model coefficient return to form the whole system model
5.data obtained from Matlab in real time so that can update the model lively

problem exists
1.block6 and 8 don't work well
2.cannot solve noisy data
3.missing the function of auto encoder
"""

from Algo import System_Build as SB
from Tools import Model_Analysis
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import control as ct
from scipy import io
plt.style.use( ['science',"grid","ieee"])

color_dict = {
    "classic":[(205/255,92/255,92/255),(60/255,179/255,113/255),(65/255,105/255,225/255)],
    "千里江山":[(117/255,159/255,107/255),(189/255,144/255,43/255),(70/255,141/255,165/255)],
    "琉璃":[(145/255,187/255,221/255),(33/255,65/255,107/255),(172/255,75/255,71/255)],
    "天青":[(70/255,128/255,139/255),(143/255,209/255,225/255),(194/255,225/255,230/255)],
    "玄泽":[(143/255,110/255,103/255),(220/255,169/255,104/255),(56/255,5/255,9/255)]
    }


########################################################
#################   DFIG operation   ##################
########################################################

Block_num = 24
Algebra_num = 17

# print("Now configure the files1...\n")
### Algorithm Parameters
Time_windows = 0.2       # [s] simulation time
Shift_windows = 0.09      # [s] simulation time

m = r"C:\Users\29639\Desktop\研二上研究\上海会议\coding\System_DFIG_HVDC.csv"  # files root
source = ('PowerFactory', m)
windows_num = 3
print("Configure1 Finished...\n")

# System generation
first1 = SB.System('first1', Block_num, Algebra_num, source, 
             windows_num, Time_windows, Shift_windows)

train_list = [1]
print(f"Now train the model with list {train_list[0]} to {train_list[-1]}\n")
first1.Block_generation(train_list, train_list)

# Other processing
print("Now error analysis:\n")
for num in range(Block_num + Algebra_num):
    first1.Blocks[num].Error_analysis()  # Error Analysis


first1_ana = Model_Analysis.Analysis(first1, ['S1UD', 'S1UQ', 'S2UD', 'S2UQ'], ['P_right', 'Qright', 'P_left', 'Qleft'])
first1_ana.Jacobian_mat()
ret = first1_ana.Damp_analysis()
filter_poles = first1_ana.Plot_range_poles(ret[2], [-5,0], [-500,500])


A = first1_ana.state_space.A

B = first1_ana.state_space.B

C = first1_ana.state_space.C

D = first1_ana.state_space.D


mat_file_A = 'A.mat'
mat_file_B = 'B.mat'
mat_file_C = 'C.mat'
mat_file_D = 'D.mat'

io.savemat(mat_file_A, {'A': A})
io.savemat(mat_file_B, {'B': B})
io.savemat(mat_file_C, {'C': C})
io.savemat(mat_file_D, {'D': D})

ct.bode(ct.ss(A,B,C,D)[0,0], dB=True, Hz =True)

print("Now coefficient analysis:\n")

block_num_dominant = [1,2,3,6,7,8,9,10,11,12,13]
# train_series = [[1],[1,2],[1,2,3],[5]]
train_series = [[1]]
# block_num_dominant = [1,2]
first1_ana.Coefficient_analysis(block_num_dominant, train_series)

print("Now draw the picture:\n")
Length = int(0.02 * 1e5 - 1)
win_num = 1

first1.Figure_plot(Length, win_num)

first1.Figure_paper_X(Length, [14,15,33,34], 1, [2,2])
first1.Figure_paper_R(Length, [1,3,5,7], 1, [2,2])

first1.Figure_paper_X(Length, [2,1], 1, [1,2])
first1.Figure_paper_R(Length, [1,2], 1, [2,1])


















