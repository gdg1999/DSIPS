# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 09:39:55 2024

@author: Gregory_Guo
"""

"""
GFL Configuration files
state order specify the order of the equation
"""

# inputs:
sys_inputs = ['v_d', 'v_q', 'ang_r', 'i_d_r', 'i_q_r']
# Outputs: 
sys_outputs = ['i_d', 'i_q', 'w', 'theta']

# Block1 --> di_d = (v_d - R*i_d + w*Lf*i_q - e_d)/Lf
states1 = ['i_d']
inputs1 = ['v_d', 'i_q', 'e_d', 'w']
constraints_assign1 = [('i_d','i_d', -7.5398),
                       ('i_d','v_d', 7539.821999999999)]
constraints_combi1 = [('i_d','v_d','i_d','e_d',0)]
bias1 = False
Type1 = 'B'
Ident1 = 'L'

# Block2 --> di_q = (v_q - R*i_q - w*Lf*i_d - e_q)/Lf
states2 = ['i_q']
inputs2 = ['v_q', 'i_d', 'e_q', 'w']
constraints_assign2 = [('i_q','i_q', -7.5398),
                       ('i_q','v_q', 7539.821999999999)]
constraints_combi2 = [('i_q','v_q','i_q','e_q',0)]
bias2 = False
Type2 = 'B'
Ident2 = 'L'

# Block3 --> di_d_i = -(i_d_r - i_d)*ki_i_dq
states3 = ['i_d_i']
inputs3 = ['i_d_r', 'i_d'] 
constraints_assign3 = [('i_d_i','i_d_i',0),
                       ('i_d_i','i_d_r',-81.8129),
                       ('i_d_i','i_d',81.8129)]
# constraints_combi3 = [('i_d_i','i_d_r','i_d_i','i_d',0)]
constraints_combi3 = []
bias3 = False
Type3 = 'B'
Ident3 = 'L'

# Block4 --> di_q_i = -(i_q_r - i_q)*ki_i_dq
states4 = ['i_q_i']
inputs4 = ['i_q_r', 'i_q']
constraints_assign4 = [('i_q_i','i_q_i',0)]
# constraints_combi4 = [('i_q_i','i_q_r','i_q_i','i_q',0)]
constraints_combi4 = []
bias4 = False
Type4 = 'B'
Ident4 = 'L'

# Block5 --> dw_pll_i = e_ang*ki_pll
states5 = ['w_pll_i']
inputs5 = ['v_q', 'ang_r']
constraints_assign5 = []
constraints_combi5 = [('w_pll_i','v_q','w_pll_i','ang_r',0)]
bias5 = False
Type5 = 'B'
Ident5 = 'L'

# Block6 --> dw = (w_pll_i + e_ang*kp_pll - w)/tau_pll   e_ang = v_q - ang_r;
states6 = ['w']
inputs6 = ['v_q', 'ang_r', 'w_pll_i']
constraints_assign6 = [('w','w_pll_i',1884.955592153876),
                       ('w','w',-1884.955592153876)]
constraints_combi6 = [('w','v_q','w','ang_r',0)]
bias6 = False
Type6 = 'B'
Ident6 = 'L'

# Block7 --> dtheta = w
states7 = ['theta']
inputs7 = ['w']
constraints_assign7 = [('theta','w',1),
                       ('theta','theta',0)]
constraints_combi7 = []
bias7 = False
Type7 = 'B'
Ident7 = 'L'

# Algebraic --> e_d = -(i_d_r - i_d)*kp_i_dq + i_d_i
states8 = ['i_d_r', 'i_d', 'i_d_i']
dot8_x = ['e_d']
constraints_assign8 = []
# constraints_assign8 = []
constraints_combi8 = [('e_d','i_d_r','e_d','i_d',0)]
bias8 = False
Type8 = 'A'
Ident8 = 'L'

# Algebraic --> e_q = -(i_q_r - i_q)*kp_i_dq + i_q_i
states9 = ['i_q_r', 'i_q', 'i_q_i']
dot9_x = ['e_q']
constraints_assign9 = []
# constraints_assign9 = []
constraints_combi9 = [('e_q','i_q_r','e_q','i_q',0)]
bias9 = False
Type9 = 'A'
Ident9 = 'L'

# outputs
# Algebraic --> i_d
states10 = ['i_d']
dot10_x = ['i_d']
constraints_assign10 = []
constraints_combi10 = []
bias10 = False
Type10 = 'A'
Ident10 = 'L'

# Algebraic --> i_q
states11 = ['i_q']
dot11_x = ['i_q']
constraints_assign11 = []
constraints_combi11 = []
bias11 = False
Type11 = 'A'
Ident11 = 'L'

# Algebraic --> omega
states12 = ['w']
dot12_x = ['w']
constraints_assign12 = []
constraints_combi12 = []
bias12 = False
Type12 = 'A'
Ident12 = 'L'

# Algebraic --> theta
states13 = ['theta']
dot13_x = ['theta']
constraints_assign13 = []
constraints_combi13 = []
bias13 = False
Type13 = 'A'
Ident13 = 'L'

