# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 13:19:21 2023

@author: Gregory_Guo
"""

"""
DFIG Configuration files
state order specify the order of the equation
"""

# inputs: UD UQ Wind
sys_inputs = ['DFIG_Ix', 'DFIG_Iy']
# Outputs: 
sys_outputs = ['UD', 'UQ']

# for transmission line
# DFIG_C
states1 = ['UD', 'UQ']
inputs1 = ['DFIG_Ix', 'DFIG_Iy', 'DFIG_Lx', 'DFIG_Ly']
constraints_assign1 = []
constraints_combi1 = []
bias1 = False
Type1 = 'B'
Ident1 = 'L'
# DFIG_L
states2 = ['DFIG_Lx', 'DFIG_Ly']
inputs2 = ['UD', 'UQ', 'PCCUx_', 'PCCUy_']
constraints_assign2 = []
constraints_combi2 = []
bias2 = False
Type2 = 'B'
Ident2 = 'L'
# PCC1
states3 = ['PCCUx_', 'PCCUy_']
inputs3 = ['DFIG_Lx', 'DFIG_Ly', 'infL_x', 'infL_y']  #, 'HVDC_Lx1', 'HVDC_Ly1'
constraints_assign3 = []
constraints_combi3 = []
bias3 = False
Type3 = 'B'
Ident3 = 'L'
# inf_L
states4 = ['infL_x', 'infL_y']
inputs4 = ['S1UD_', 'S1UQ_', 'PCCUx_', 'PCCUy_']
constraints_assign4 = []
constraints_combi4 = []
bias4 = False
Type4 = 'B'
Ident4 = 'L'

# Algebraic --> UD
states5 = ['UD']
dot5_x = ['UD']
constraints_assign5 = []
constraints_combi5 = []
bias5 = False
Type5 = 'A'
Ident5 = 'L'

# Algebraic --> 'UD'
states6 = ['UQ']
dot6_x = ['UQ']
constraints_assign6 = []
constraints_combi6 = []
bias6 = False
Type6 = 'A'
Ident6 = 'L'

