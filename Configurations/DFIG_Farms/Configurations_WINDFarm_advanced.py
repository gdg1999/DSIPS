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
sys_inputs = ['UD_averaged', 'UQ_averaged', 'Wind_averaged']
sys_outputs = ['UD_averaged', 'UQ_averaged', 'Wind_averaged']
# Outputs: 


# Block1 --> Asynchronous Machine
states1 = ['Ird_averaged', 'Irq_averaged', 'Isd_averaged', 'Isq_averaged']
inputs1 = ['Urd_averaged', 'Urq_averaged', 'Usd_averaged', 'Usq_averaged']
constraints_assign1 = []
constraints_combi1 = []
bias1 = False
Type1 = 'B'
Ident1 = 'L'

# Block2 --> Grid Filter
states2 = ['pigd_averaged', 'pigq_averaged']
inputs2 = ['Usdg_averaged', 'Usqg_averaged', 'Vrefd_averaged', 'Vrefq_averaged']     
constraints_assign2 = []
constraints_combi2 = []
bias2 = False
Type2 = 'B'
Ident2 = 'L'

# Block3 --> Swing Equations
states3 = ['pwm_averaged']
inputs3 = ['Te_averaged', 'TL_averaged']
constraints_assign3 = []
constraints_combi3 = []
bias3 = False
Type3 = 'B'
Ident3 = 'L'

# Block4 --> Capacitor
states4 = ['pVdc_averaged']
inputs4 = ['Prsc_averaged', 'Pgsc_averaged']     
constraints_assign4 = [('pVdc_averaged','x0_dot',1),
                        ('pVdc_averaged','x0x0_dot',-1),
                        ('pVdc_averaged','x0',0),
                        ('pVdc_averaged','u0_dot',0),
                        ('pVdc_averaged','u1_dot',0),
                        ('pVdc_averaged','u0x0_dot',0),
                        ('pVdc_averaged','u1x0_dot',0),
                        ('pVdc_averaged','x0u1_dot',0)]
constraints_combi4 = [('pVdc_averaged','u0','pVdc_averaged','u1', 0)]
# constraints_assign4 = []
# constraints_combi4 = []
bias4 = True
Type4 = 'B'
# Ident4 = 'L'
Ident4 = 'I'

# Block5 --> RSC
states5 = ['pPhira_averaged', 'pPhirb_averaged', 'pPhirc_averaged']
inputs5 = ['Ird_averaged', 'Irq_averaged', 'pwm_averaged', 'Usdg_averaged', 'Usqg_averaged']
constraints_assign5 = []
constraints_combi5 = []
bias5 = True
Type5 = 'B'
Ident5 = 'L'

# Block6 --> GSC
states6 = ['pPhiga_averaged', 'pPhigb_averaged', 'pPhigc_averaged']
inputs6 = ['pVdc_averaged', 'pigd_averaged', 'pigq_averaged']
constraints_assign6 = []
constraints_combi6 = []
bias6 = True
Type6 = 'B'
Ident6 = 'L'

# Block7 --> Axis
states7 = ['pTurbine_w_averaged', 'pshaft_w_averaged']
inputs7 = ['pwm_averaged', 'Wind_averaged']
constraints_assign7 = []
constraints_combi7 = []
bias7 = False
Type7 = 'B'
Ident7 = 'L'

# Block8 --> PLL_rsc
states8 = ['rtheta_pll_averaged', 'pRPLL_PI_averaged']
inputs8 = ['UD_averaged', 'UQ_averaged']
# constraints_assign8 = [('rtheta_pll_averaged','u0',0),
#                         ('rtheta_pll_averaged','u1',0),
#                         ('rtheta_pll_averaged','x1',1),
#                         ('rtheta_pll_averaged','x0 sin(1 x0)',0),
#                         ('rtheta_pll_averaged','x0 cos(1 x0)',0),
#                         ('rtheta_pll_averaged','x0 sin(1 x1)',0),
#                         ('rtheta_pll_averaged','x0 cos(1 x1)',0),
#                         ('pRPLL_PI_averaged','x0',0),
#                         ('pRPLL_PI_averaged','u0',0),
#                         ('pRPLL_PI_averaged','u1',0),
#                         ('pRPLL_PI_averaged','x0 sin(1 x0)',0),
#                         ('pRPLL_PI_averaged','x0 cos(1 x0)',0),
#                         ('pRPLL_PI_averaged','x0 sin(1 x1)',0),
#                         ('pRPLL_PI_averaged','x0 cos(1 x1)',0),
#   ]
constraints_assign8 = [('rtheta_pll_averaged','u0',0),
                        ('rtheta_pll_averaged','u1',0),
                        ('rtheta_pll_averaged','x1',1),
                        ('rtheta_pll_averaged','x1 sin(1 x0)',0),
                        ('rtheta_pll_averaged','x1 cos(1 x0)',0),
                        ('pRPLL_PI_averaged','x1',0),
                        ('pRPLL_PI_averaged','u0',0),
                        ('pRPLL_PI_averaged','u1',0),
                        ('pRPLL_PI_averaged','x1 sin(1 x0)',0),
                        ('pRPLL_PI_averaged','x1 cos(1 x0)',0)]
# constraints_assign8 = []
constraints_combi8 = []
# constraints_combi8 = [('rtheta_pll_averaged','u0 cos(1 x0)','rtheta_pll_averaged','u1 sin(1 x0)', 0),
#                       ('pRPLL_PI_averaged','u0 cos(1 x0)','pRPLL_PI_averaged','u1 sin(1 x0)', 0)]
bias8 = True
Type8 = 'B'
# Ident8 = 'L'
Ident8 = 'S'

# Block9 --> PLL_gsc
states9 = ['pGPLL_PI_averaged', 'gtheta_pll_averaged']
inputs9 = ['UD_averaged', 'UQ_averaged'] 
constraints_assign9 = []
constraints_combi9 = []
bias9 = False
Type9 = 'B'
# Ident9 = 'L'
Ident9 = 'S'



# for transmission line
# DFIG_C
states10 = ['UD_averaged', 'UQ_averaged']
inputs10 = ['DFIG_Ix_averaged', 'DFIG_Iy_averaged', 'DFIG_Lx_averaged', 'DFIG_Ly_averaged']
constraints_assign10 = []
constraints_combi10 = []
bias10 = False
Type10 = 'B'
Ident10 = 'L'
# DFIG_L
states11 = ['DFIG_Lx_averaged', 'DFIG_Ly_averaged']
inputs11 = ['UD_averaged', 'UQ_averaged', 'PCCUx_', 'PCCUy_']
constraints_assign11 = []
constraints_combi11 = []
bias11 = False
Type11 = 'B'
Ident11 = 'L'
# PCC1
states12 = ['PCCUx_', 'PCCUy_']
inputs12 = ['DFIG_Lx_total', 'DFIG_Ly_total', 'infL_x', 'infL_y']  #, 'HVDC_Lx1', 'HVDC_Ly1'
constraints_assign12 = []
constraints_combi12 = []
bias12 = False
Type12 = 'B'
Ident12 = 'L'
# inf_L
states13 = ['infL_x', 'infL_y']
inputs13 = ['S1UD_', 'S1UQ_', 'PCCUx_', 'PCCUy_']
constraints_assign13 = []
constraints_combi13 = []
bias13 = False
Type13 = 'B'
Ident13 = 'L'


# Algebraic --> TL
states14 = ['pTurbine_w_averaged', 'pshaft_w_averaged', 'pwm_averaged']
dot14_x = ['TL_averaged']
constraints_assign14 = []
constraints_combi14 = []
bias14 = False
Type14 = 'A'
# Ident14 = 'L'
Ident14 = 'L'

# Algebraic --> Te
states15 = ['Ird_averaged', 'Irq_averaged', 'Isd_averaged', 'Isq_averaged']
dot15_x = ['Te_averaged']
constraints_assign15 = []
constraints_combi15 = []
bias15 = False
Type15 = 'A'
Ident15 = 'L'
# Ident15 = 'P2'

# Algebraic --> Prsc
states16 = ['Ird_averaged', 'Irq_averaged', 'Urd_averaged', 'Urq_averaged']
dot16_x = ['Prsc_averaged']
constraints_assign16 = []
constraints_combi16 = []
bias16 = False
Type16 = 'A'
Ident16 = 'L'
# Ident16 = 'P2'

# Algebraic --> Pgsc
states17 = ['pigd_averaged', 'pigq_averaged', 'Usdg_averaged', 'Usqg_averaged']
dot17_x = ['Pgsc_averaged']
constraints_assign17 = []
constraints_combi17 = []
bias17 = False
Type17 = 'A'
Ident17 = 'L'
# Ident17 = 'P2'

# Algebraic --> Usd, Usq
states18 = ['UD_averaged', 'UQ_averaged', 'rtheta_pll_averaged']
dot18_x = ['Usd_averaged', 'Usq_averaged']
constraints_assign18 = []
constraints_combi18 = []
bias18 = True
Type18 = 'A'
Ident18 = 'L'

# Algebraic --> Usdg, Usqg
states19 = ['UD_averaged', 'UQ_averaged', 'gtheta_pll_averaged']
dot19_x = ['Usdg_averaged', 'Usqg_averaged']
constraints_assign19 = []
constraints_combi19 = []
bias19 = False
Type19 = 'A'
Ident19 = 'L'

# Algebraic --> Vrefd, Vrefq
states20 = ['pigd_averaged', 'pigq_averaged', 'pPhiga_averaged', 'pPhigb_averaged', 'pPhigc_averaged', 'pVdc_averaged', 'Usdg_averaged', 'Usqg_averaged']
dot20_x = ['Vrefd_averaged', 'Vrefq_averaged']
constraints_assign20 = []
constraints_combi20 = []
bias20 = True
Type20 = 'A'
Ident20 = 'L'

# Algebraic --> Vrefq
states21 = ['Ird_averaged', 'Irq_averaged', 'pPhira_averaged', 'pPhirb_averaged', 'pPhirc_averaged', 'pwm_averaged']
dot21_x = ['Urd_averaged', 'Urq_averaged']
constraints_assign21 = []
constraints_combi21 = []
bias21 = True
Type21 = 'A'
Ident21 = 'L'

# Algebraic --> P_total
states22 = ['DFIG_Lx_total', 'DFIG_Ly_total', 'PCCUx_', 'PCCUy_']
dot22_x = ['Ptotal']
constraints_assign22 = []
constraints_combi22 = []
bias22 = True
Type22 = 'A'
Ident22 = 'L'

# Algebraic --> P_total
states23 = ['DFIG_Lx_total', 'DFIG_Ly_total', 'PCCUx_', 'PCCUy_']
dot23_x = ['Qtotal']
constraints_assign23 = []
constraints_combi23 = []
bias23 = True
Type23 = 'A'
Ident23 = 'L'

