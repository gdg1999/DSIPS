# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 08:47:05 2023

@author: Gregory_Guo
"""

"""
Main Function for Paper: Online Linear Model Identification of Inverter-based
System for Stability Evaluation with Transient Data
and Model-informed Constraints
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

Block_num = 9
Algebra_num = 15

### Algorithm Parameters
Time_windows = 0.10       # [s] simulation time
Shift_windows = 0.09      # [s] simulation time

m = r"C:\Users\29639\Desktop\研二上研究\论文三\code\System_input_change100.csv"  # files root
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


DFIG_ana1 = Model_Analysis.Analysis(first1, ['UD','UQ'], ['DFIG_Ix','DFIG_Iy'])
DFIG_ana1.Jacobian_mat()
ret = DFIG_ana1.Damp_analysis()
filter_poles = DFIG_ana1.Plot_range_poles(ret[2], [-20,40], [-100,100])

A = DFIG_ana1.state_space.A

B = DFIG_ana1.state_space.B

C = DFIG_ana1.state_space.C

D = DFIG_ana1.state_space.D


mat_file_A = 'A.mat'
mat_file_B = 'B.mat'
mat_file_C = 'C.mat'
mat_file_D = 'D.mat'

io.savemat(mat_file_A, {'A': A})
io.savemat(mat_file_B, {'B': B})
io.savemat(mat_file_C, {'C': C})
io.savemat(mat_file_D, {'D': D})

ct.bode(ct.ss(A,B,C,D)[0,0], dB=True, Hz =True)

Length = int(0.1 * 1e5 - 1)
win_num = 1

# print("Now coefficient analysis:\n")

# block_num_dominant = [1,2,4]
# # train_series = [[1],[1,2],[1,2,3],[5]]
train_series = [[1],[2],[3]]
block_num_dominant = [3,4]
first1.Coefficient_analysis(block_num_dominant, train_series)

# first1.Figure_plot(Length, win_num)
# first1.Figure_paper_R(Length, [1,4,8,16], 1, [2,2])
# first1.Figure_paper_R(Length, [1,2,3,4,5,6,7,8,9], 1, [3,3])
# first1.Figure_paper_X(Length, [14,15,16,17,18,19,20,21,22], 1, [3,3])
# first1.Figure_paper_X(Length, [23,24,25,26,27], 1, [3,2])

########################################################
#################   grid operation   ##################
########################################################

Block_num = 4
Algebra_num = 2

### Algorithm Parameters
Time_windows = 0.1       # [s] simulation time
Shift_windows = 0.21      # [s] simulation time

m = r"C:\Users\29639\Desktop\研二上研究\论文三\code\System_input_change1.csv"  # files root
source = ('PowerFactory', m)
windows_num = 1
print("Configure2 Finished...\n")

# System generation
grid = SB.System('grid', Block_num, Algebra_num, source, 
             windows_num, Time_windows, Shift_windows)

train_list = [1]
print(f"Now train the model with list {train_list[0]} to {train_list[-1]}\n")
grid.Block_generation(train_list, train_list)

# Other processing
print("Now error analysis:\n")
for num in range(Block_num + Algebra_num):
    grid.Blocks[num].Error_analysis()  # Error Analysis


Grid_ana1 = Model_Analysis.Analysis(grid, ['DFIG_Ix','DFIG_Iy'], ['UD','UQ'])
Grid_ana1.Jacobian_mat()
ret = Grid_ana1.Damp_analysis()
# Gridfilter_poles = Grid_ana1.Plot_range_poles(ret[2], [-20,40], [-100,100])

AGrid = Grid_ana1.state_space.A

BGrid = Grid_ana1.state_space.B

CGrid = Grid_ana1.state_space.C

DGrid = Grid_ana1.state_space.D


mat_file_A = 'AGrid.mat'
mat_file_B = 'BGrid.mat'
mat_file_C = 'CGrid.mat'
mat_file_D = 'DGrid.mat'

io.savemat(mat_file_A, {'AGrid': AGrid})
io.savemat(mat_file_B, {'BGrid': BGrid})
io.savemat(mat_file_C, {'CGrid': CGrid})
io.savemat(mat_file_D, {'DGrid': DGrid})

########################################################
#################   GFL operation   ##################
########################################################

Block_num = 7
Algebra_num = 6

### Algorithm Parameters
Time_windows = 0.12       # [s] simulation time
Shift_windows = 0.02      # [s] simulation time

m = r"C:\Users\29639\Desktop\研二上研究\论文三\code\GFL_input.csv"  # files root
source = ('PowerFactory', m)
windows_num = 2
print("Configure3 Finished...\n")

# System generation
GFL = SB.System('GFL', Block_num, Algebra_num, source, 
             windows_num, Time_windows, Shift_windows)

train_list = [1,2]
print(f"Now train the model with list {train_list[0]} to {train_list[-1]}\n")
GFL.Block_generation(train_list, train_list)

# Other processing
print("Now error analysis:\n")
for num in range(Block_num + Algebra_num):
    GFL.Blocks[num].Error_analysis()  # Error Analysis

GFLAna = Model_Analysis.Analysis(GFL, ['v_d', 'v_q'], ['i_d', 'i_q'])
GFLAna.Jacobian_mat()
ret = GFLAna.Damp_analysis()


AGFL = GFLAna.state_space.A

BGFL = GFLAna.state_space.B

CGFL = GFLAna.state_space.C

DGFL = GFLAna.state_space.D


mat_file_A = 'AGFL.mat'
mat_file_B = 'BGFL.mat'
mat_file_C = 'CGFL.mat'
mat_file_D = 'DGFL.mat'

io.savemat(mat_file_A, {'AGFL': AGFL})
io.savemat(mat_file_B, {'BGFL': BGFL})
io.savemat(mat_file_C, {'CGFL': CGFL})
io.savemat(mat_file_D, {'DGFL': DGFL})

Length = int(0.1 * 3e4 - 1)
win_num = 1
GFL.Figure_plot(Length, win_num)


########################################################
#################   GFM1 operation   ##################
########################################################

Block_num = 13
Algebra_num = 10

### Algorithm Parameters
Time_windows = 0.10       # [s] simulation time
Shift_windows = 0.02      # [s] simulation time

m = r"C:\Users\29639\Desktop\研二上研究\论文三\code\GFM1_input.csv"  # files root
source = ('PowerFactory', m)
windows_num = 2
print("Configure4 Finished...\n")


# System generation
GFM1 = SB.System('GFM1', Block_num, Algebra_num, source, 
             windows_num, Time_windows, Shift_windows)

train_list = [1,2]
print(f"Now train the model with list {train_list[0]} to {train_list[-1]}\n")
GFM1.Block_generation(train_list, train_list)

# Other processing
print("Now error analysis:\n")
for num in range(Block_num + Algebra_num):
    GFM1.Blocks[num].Error_analysis()  # Error Analysis

GFM1Ana = Model_Analysis.Analysis(GFM1, ['v_gd', 'v_gq'], ['i_od', 'i_oq'])
GFM1Ana.Jacobian_mat()
ret = GFM1Ana.Damp_analysis()


AGFM1 = GFM1Ana.state_space.A

BGFM1 = GFM1Ana.state_space.B

CGFM1 = GFM1Ana.state_space.C

DGFM1 = GFM1Ana.state_space.D


mat_file_A = 'AGFM1.mat'
mat_file_B = 'BGFM1.mat'
mat_file_C = 'CGFM1.mat'
mat_file_D = 'DGFM1.mat'

io.savemat(mat_file_A, {'AGFM1': AGFM1})
io.savemat(mat_file_B, {'BGFM1': BGFM1})
io.savemat(mat_file_C, {'CGFM1': CGFM1})
io.savemat(mat_file_D, {'DGFM1': DGFM1})

Length = int(0.1 * 3e4 - 1)
win_num = 1
GFM1.Figure_plot(Length, win_num)


########################################################
#################   GFM2 operation   ##################
########################################################

Block_num = 13
Algebra_num = 10

### Algorithm Parameters
Time_windows = 0.12       # [s] simulation time
Shift_windows = 0.02      # [s] simulation time

m = r"C:\Users\29639\Desktop\研二上研究\论文三\code\GFM2.csv"  # files root
source = ('PowerFactory', m)
windows_num = 2
print("Configure5 Finished...\n")


# System generation
GFM2 = SB.System('GFM2', Block_num, Algebra_num, source, 
             windows_num, Time_windows, Shift_windows)

train_list = [1,2]
print(f"Now train the model with list {train_list[0]} to {train_list[-1]}\n")
GFM2.Block_generation(train_list, train_list)

# Other processing
print("Now error analysis:\n")
for num in range(Block_num + Algebra_num):
    GFM2.Blocks[num].Error_analysis()  # Error Analysis

GFM2Ana = Model_Analysis.Analysis(GFM2, ['v_gd', 'v_gq'], ['i_od', 'i_oq'])
GFM2Ana.Jacobian_mat()
ret = GFM2Ana.Damp_analysis()
filter_poles = GFM2Ana.Plot_range_poles(ret[2], [-100,20], [-100,100])

AGFM2 = GFM2Ana.state_space.A

BGFM2 = GFM2Ana.state_space.B

CGFM2 = GFM2Ana.state_space.C

DGFM2 = GFM2Ana.state_space.D


mat_file_A = 'AGFM2.mat'
mat_file_B = 'BGFM2.mat'
mat_file_C = 'CGFM2.mat'
mat_file_D = 'DGFM2.mat'

io.savemat(mat_file_A, {'AGFM2': AGFM2})
io.savemat(mat_file_B, {'BGFM2': BGFM2})
io.savemat(mat_file_C, {'CGFM2': CGFM2})
io.savemat(mat_file_D, {'DGFM2': DGFM2})

Length = int(0.1 * 3e4 - 1)
win_num = 1
GFM2.Figure_plot(Length, win_num)
