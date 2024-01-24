# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 09:40:21 2024

@author: Gregory_Guo
"""

"""
GFM Configuration files
state order specify the order of the equation
"""

# inputs: UD UQ Wind
sys_inputs = ['v_gd', 'v_gq', 'P0', 'Q0']
# Outputs: 
sys_outputs = ['i_od', 'i_oq', 'w', 'theta']

# Block1 --> di_ld = (v_od - e_d - Rf*i_ld + w*Lf*i_lq)/Lf
states1 = ['i_ld']
inputs1 = ['v_od', 'e_d', 'i_lq', 'w']
constraints_assign1 = [('i_ld','i_lq',376.99112)]
constraints_combi1 = [('i_ld','v_od','i_ld','e_d',0)]
bias1 = False
Type1 = 'B'
Ident1 = 'L'

# Block2 --> di_lq = (v_oq - e_q - Rf*i_lq - w*Lf*i_ld)/Lf
states2 = ['i_lq']
inputs2 = ['v_oq', 'e_q', 'i_ld', 'w']
constraints_assign2 = [('i_lq','i_ld',-376.99112)]
constraints_combi2 = [('i_lq','v_oq','i_lq','e_q',0)]
bias2 = False
Type2 = 'B'
Ident2 = 'L'

# Block3 --> di_ld_i = -error_i_ld*ki_i_ldq
states3 = ['i_ld_i']
inputs3 = ['i_ld_r', 'i_ld']
constraints_assign3 = [('i_ld_i','i_ld_i',0)]
constraints_combi3 = [('i_ld_i','i_ld_r','i_ld_i','i_ld',0)]
bias3 = False
Type3 = 'B'
Ident3 = 'L'

# Block4 --> di_lq_i = -error_i_lq*ki_i_ldq
states4 = ['i_lq_i']
inputs4 = ['i_lq_r', 'i_lq']
constraints_assign4 = [('i_lq_i','i_lq_i',0)]
constraints_combi4 = [('i_lq_i','i_lq_r','i_lq_i','i_lq',0)]
bias4 = False
Type4 = 'B'
Ident4 = 'L'

# Block5 --> dv_od = (-(i_ld - i_od) + w*Cf*v_oq)/Cf
states5 = ['v_od']
inputs5 = ['i_ld', 'i_od', 'v_oq', 'w']
constraints_assign5 = [('v_od','v_od',0),
                       ('v_od','v_oq',376.99112)]
constraints_combi5 = [('v_od','i_ld','v_od','i_od',0)]
bias5 = False
Type5 = 'B'
Ident5 = 'L'

# Block6 --> dv_oq = (-(i_lq - i_oq) - w*Cf*v_od)/Cf
states6 = ['v_oq']
inputs6 = ['i_lq', 'i_oq', 'v_od', 'w']
constraints_assign6 = [('v_oq','v_oq',0),
                       ('v_oq','v_od',-376.99112)]
constraints_combi6 = [('v_oq','i_lq','v_oq','i_oq',0)]
bias6 = False
Type6 = 'B'
Ident6 = 'L'

# Block7 --> dv_od_i = error_v_od*ki_v_odq
states7 = ['v_od_i']
inputs7 = ['error_v_od']
constraints_assign7 = [('v_od_i','v_od_i',0)]
constraints_combi7 = []
bias7 = False
Type7 = 'B'
Ident7 = 'L'

# Block8 --> dv_oq_i = error_v_oq*ki_v_odq
states8 = ['v_oq_i']
inputs8 = ['error_v_oq']
constraints_assign8 = [('v_oq_i','v_oq_i',0)]
constraints_combi8 = []
bias8 = False
Type8 = 'B'
Ident8 = 'L'

# Block9 --> di_od = (v_gd - v_od - Rc*i_od + w*Lc*i_oq)/Lc
states9 = ['i_od']
inputs9 = ['i_oq', 'v_od', 'v_gd', 'w']
constraints_assign9 = [('i_od','v_gd', 37699.11),
                       ('i_od','w', 0),
                       ('i_od','i_oq', 376.99112)]
constraints_combi9 = [('i_od','v_od','i_od','v_gd',0)]
bias9 = False
Type9 = 'B'
Ident9 = 'L'

# Block10 --> di_oq = (v_gq - v_oq - Rc*i_oq - w*Lc*i_od)/Lc
states10 = ['i_oq']
inputs10 = ['i_od', 'v_oq', 'v_gq', 'w']
constraints_assign10 = [('i_oq','v_gq', 37699.11),
                        ('i_oq','w', 0),
                        ('i_oq','i_od', -376.99112)]
constraints_combi10 = [('i_oq','v_oq','i_oq','v_gq',0)]
bias10 = False
Type10 = 'B'
Ident10 = 'L'

# Block11 --> dv_od_r = (obj.v_od_r(constant) + Dv*(Q0 - q) - v_od_r)*wf
states11 = ['v_od_r']
inputs11 = ['i_od', 'i_oq']
# inputs11 = ['q', 'Q0']
# constraints_assign11 = [('v_od_r','v_od_r', -10*3.1415926),
#                         ('v_od_r','Q0', 0.05*10*3.1415926)]  # 0.05->0.06
# constraints_combi11 = [('v_od_r','Q0','v_od_r','q',0)]
# bias11 = True
constraints_assign11 = []
constraints_combi11 = []
bias11 = False
Type11 = 'B'
Ident11 = 'L'

# Block12 --> dw = (W0 + Dw*(P0 - p) - w)*wf
states12 = ['w']
# inputs12 = ['p', 'P0']
inputs12 = ['i_od', 'i_oq']
constraints_assign12 = []
# constraints_assign12 = [('w','w',-31.41593)]
constraints_combi12 = []
# bias12 = True
bias12 = False
Type12 = 'B'
Ident12 = 'L'

# Block13 --> dtheta = w
states13 = ['theta']
inputs13 = ['w']
constraints_assign13 = [('theta','w',1),
                        ('theta','theta',0)]
constraints_combi13 = []
bias13 = False
Type13 = 'B'
Ident13 = 'L'

# Algebraic --> p = (v_od*i_od + v_oq*i_oq)*(-1)
states14 = ['v_od', 'v_oq', 'i_od', 'i_oq']
dot14_x = ['p']
constraints_assign14 = []
constraints_combi14 = []
bias14 = False
Type14 = 'A'
Ident14 = 'L'

# Algebraic --> q = (-v_od*i_oq + v_oq*i_od)*(-1)
states15 = ['v_od', 'v_oq', 'i_od', 'i_oq']
dot15_x = ['q']
constraints_assign15 = []
constraints_combi15 = []
bias15 = False
Type15 = 'A'
Ident15 = 'L'

# Algebraic --> e_d = -error_i_ld*kp_i_ldq + i_ld_i; error_i_ld = i_ld_r-i_ld;  
states16 = ['i_ld_r', 'i_ld', 'i_ld_i']
dot16_x = ['e_d']
constraints_assign16 = []
constraints_combi16 = []
bias16 = False
Type16 = 'A'
Ident16 = 'L'

# Algebraic --> e_q = -error_i_lq*kp_i_ldq + i_lq_i; error_i_lq = i_lq_r-i_lq;
states17 = ['i_lq_r', 'i_lq', 'i_lq_i']
dot17_x = ['e_q']
constraints_assign17 = []
constraints_combi17 = []
bias17 = False
Type17 = 'A'
Ident17 = 'L'

# Algebraic --> i_ld_r = -(error_v_od*kp_v_odq + v_od_i)
states18 = ['error_v_od', 'v_od_i']
dot18_x = ['i_ld_r']
constraints_assign18 = []
constraints_combi18 = []
bias18 = False
Type18 = 'A'
Ident18 = 'L'

# Algebraic --> i_lq_r = -(error_v_oq*kp_v_odq + v_oq_i)
states19 = ['error_v_oq', 'v_oq_i']
dot19_x = ['i_lq_r']
constraints_assign19 = []
constraints_combi19 = []
bias19 = False
Type19 = 'A'
Ident19 = 'L'

# Algebraic --> error_v_od = v_od_r - v_od - (i_od*Rov-i_oq*Xov)*(-1)
states20 = ['v_od_r', 'v_od', 'i_od', 'i_oq']
dot20_x = ['error_v_od']
constraints_assign20 = [('error_v_od', 'i_od', 0)] # Rov->0.01
# constraints_assign20 = [('error_v_od', 'i_od', 0.01),
#                         ('error_v_od', 'i_oq', 0),
#                         ('error_v_od', 'v_od_r', 1)]
constraints_combi20 = [('error_v_od','v_od_r','error_v_od','v_od',0)]
bias20 = False
Type20 = 'A'
Ident20 = 'L'

# Algebraic --> error_v_oq = v_oq_r - v_oq - (i_oq*Rov+i_od*Xov)*(-1)
states21 = ['v_oq_r', 'v_oq', 'i_od', 'i_oq']
dot21_x = ['error_v_oq']
constraints_assign21 = [('error_v_oq', 'i_oq', 0)]
# constraints_assign21 = [('error_v_oq', 'i_oq', 0.01),
#                         ('error_v_oq', 'v_oq_r', 1)]
constraints_combi21 = [('error_v_oq','v_oq_r','error_v_oq','v_oq',0)]
bias21 = False
Type21 = 'A'
Ident21 = 'L'

# Algebraic --> i_od = i_od
states22 = ['i_od']
dot22_x = ['i_od']
constraints_assign22 = []
constraints_combi22 = []
bias22 = False
Type22 = 'A'
Ident22 = 'L'

# Algebraic --> i_oq = i_oq
states23 = ['i_oq']
dot23_x = ['i_oq']
constraints_assign23 = []
constraints_combi23 = []
bias23 = False
Type23 = 'A'
Ident23 = 'L'

