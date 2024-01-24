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
sys_inputs = ['UD', 'UQ', 'Wind', 'w_ref', 'Vbus', 'ird_ref', 'igq_ref']
# Outputs: 
sys_outputs = ['DFIG_Ix', 'DFIG_Iy', 'Te', 'Prsc', 'Pgsc']

# Block1 --> Asynchronous Machine
states1 = ['Ird', 'Irq', 'Isd', 'Isq']
inputs1 = ['Urd', 'Urq', 'Usd', 'Usq', 'pwm']
constraints_assign1 = [('Ird','Urq',0),
                        ('Ird','Usq',0),
                        ('Irq','Urd',0),
                        ('Irq','Usd',0),
                        ('Isd','Urq',0),
                        ('Isd','Usq',0),
                        ('Isq','Urd',0),
                        ('Isq','Usd',0)]
# constraints_assign1 = []
constraints_combi1 = []
bias1 = False
Type1 = 'B'
Ident1 = 'L'

# Block2 --> Grid Filter
states2 = ['pigd', 'pigq']
inputs2 = ['Usdg', 'Usqg', 'Vrefd', 'Vrefq']     
constraints_assign2 = []
constraints_combi2 = []
bias2 = False
Type2 = 'B'
Ident2 = 'L'

# Block3 --> Swing Equations
states3 = ['pwm']
inputs3 = ['Te', 'TL']
constraints_assign3 = [('pwm', 'pwm', 0)]
constraints_combi3 = []
bias3 = False
Type3 = 'B'
Ident3 = 'L'

# Block4 --> Capacitor
states4 = ['pVdc']
inputs4 = ['Prsc', 'Pgsc']    
constraints_assign4 = [('pVdc', 'pVdc', 0)]
constraints_combi4 = [('pVdc','Prsc','pVdc','Pgsc', 0)]
bias4 = False
Type4 = 'B'
Ident4 = 'L'

# Block5 --> RSC
states5 = ['pPhira', 'pPhirb', 'pPhirc']
inputs5 = ['Ird', 'Irq', 'pwm', 'w_ref', 'ird_ref']
# inputs5 = ['Ird', 'Irq', 'pwm', 'Usdg', 'Usqg']
constraints_assign5 = [('pPhirc','pPhira',0),
                       ('pPhirc','pPhirb',0),
                       ('pPhirc','pPhirc',0),
                       ('pPhirc','ird_ref',0),
                       ('pPhira','pPhira',0),
                       ('pPhira','pPhirb',0),
                       ('pPhira','Irq',0),
                       ('pPhira','pwm',0),
                       ('pPhira','w_ref',0),
                       ('pPhirb','pPhira',0),
                       ('pPhirb','pPhirb',0),
                       ('pPhirb','ird_ref',0)]
constraints_combi5 = []
# bias5 = True
bias5 = False
Type5 = 'B'
Ident5 = 'L'

# Block6 --> GSC
states6 = ['pPhiga', 'pPhigb', 'pPhigc']
inputs6 = ['pVdc', 'pigd', 'pigq', 'Vbus', 'igq_ref']
# inputs6 = ['pVdc', 'pigd', 'pigq']
constraints_assign6 = [('pPhiga','pPhiga',0),
                       ('pPhiga','pPhigb',0),
                       ('pPhiga','pPhigc',0),
                       ('pPhiga','Vbus',0),
                       ('pPhiga','pVdc',0),
                       ('pPhiga','pigd',0),
                       ('pPhigb','igq_ref',0),
                       ('pPhigc','igq_ref',0),
                       ('pPhigc','pPhiga',0)]
constraints_combi6 = []
bias6 = False
Type6 = 'B'
Ident6 = 'L'

# Block7 --> Axis
states7 = ['pTurbine_w', 'pshaft_w']
inputs7 = ['pwm', 'Wind']
constraints_assign7 = []
constraints_combi7 = []
bias7 = False
Type7 = 'B'
Ident7 = 'L'

# Block8 --> PLL_rsc
states8 = ['ptheta_pll', 'pRPLL_PI']
inputs8 = ['UD', 'UQ']
constraints_assign8 = [('pRPLL_PI', 'pRPLL_PI', 0),
                       ('ptheta_pll', 'pRPLL_PI', 1)]
constraints_combi8 = []
bias8 = False
Type8 = 'B'
Ident8 = 'L'

# Block9 --> PLL_gsc
states9 = ['pGPLL_PI', 'gtheta_pll']
inputs9 = ['UD', 'UQ'] 
constraints_assign9 = [('pGPLL_PI', 'pGPLL_PI', 0),
                       ('gtheta_pll', 'pGPLL_PI', 1)]
constraints_combi9 = []
bias9 = False
Type9 = 'B'
Ident9 = 'L'


# Algebraic --> TL
states10 = ['pTurbine_w', 'pshaft_w', 'pwm']
dot10_x = ['TL']
constraints_assign10 = []
constraints_combi10 = []
bias10 = False
Type10 = 'A'
# Ident14 = 'L'
Ident10 = 'L'

# Algebraic --> Te
states11 = ['Ird', 'Irq', 'Isd', 'Isq']
dot11_x = ['Te']
constraints_assign11 = []
constraints_combi11 = []
bias11 = False
Type11 = 'A'
Ident11 = 'L'
# Ident15 = 'P2'

# Algebraic --> Prsc
states12 = ['Ird', 'Irq', 'Urd', 'Urq']
dot12_x = ['Prsc']
constraints_assign12 = []
constraints_combi12 = []
bias12 = False
Type12 = 'A'
Ident12 = 'L'
# Ident16 = 'P2'

# Algebraic --> Pgsc
states13 = ['pigd', 'pigq', 'Usdg', 'Usqg']
dot13_x = ['Pgsc']
constraints_assign13 = []
constraints_combi13 = []
bias13 = False
Type13 = 'A'
Ident13 = 'L'
# Ident17 = 'P2'

# Algebraic --> Usd, Usq
states14 = ['UD', 'UQ', 'ptheta_pll_pi']
dot14_x = ['Usd', 'Usq']
constraints_assign14 = [('Usq','ptheta_pll_pi',0)]
constraints_combi14 = []
bias14 = False
Type14 = 'A'
Ident14 = 'L'

# Algebraic --> Usdg, Usqg
states15 = ['UD', 'UQ', 'gtheta_pll']
dot15_x = ['Usdg', 'Usqg']
constraints_assign15 = [('Usdg','gtheta_pll',0)]
constraints_combi15 = []
bias15 = False
Type15 = 'A'
Ident15 = 'L'

# Algebraic --> Vrefd, Vrefq
states16 = ['pigd', 'pigq', 'pPhiga', 'pPhigb', 'pPhigc', 'pVdc', 'Usdg', 'Usqg', 'Vbus', 'igq_ref']
dot16_x = ['Vrefd', 'Vrefq']
constraints_assign16 = [('Vrefd', 'igq_ref', 0),
                        ('Vrefd', 'pPhiga', 0),
                        ('Vrefd', 'Usqg', 0),
                        ('Vrefq', 'Vbus', 0)]
constraints_combi16 = []
bias16 = False
Type16 = 'A'
Ident16 = 'L'

# Algebraic --> Vrefq
states17 = ['Ird', 'Irq', 'pPhira', 'pPhirb', 'pPhirc', 'pwm', 'w_ref', 'ird_ref']
dot17_x = ['Urd', 'Urq']
constraints_assign17 = [('Urq', 'ird_ref', 0),
                        ('Urq', 'pPhira', 0),
                        ('Urd', 'w_ref', 0),
                        ('Urd', 'pwm', 0),
                        ('Urd', 'pPhirc', 0),
                        ('Urd', 'pPhirb', 0),
                        ('Urd', 'pPhira', 1),
                        ('Urq', 'pPhirb', 1)]
constraints_combi17 = [('Urd', 'Ird', 'Urd', 'ird_ref', 0)]
bias17 = False
Type17 = 'A'
Ident17 = 'L'

# Algebraic --> P_total
states18 = ['DFIG_Lx', 'DFIG_Ly', 'PCCUx_', 'PCCUy_']
dot18_x = ['Ptotal']
constraints_assign18 = []
constraints_combi18 = []
bias18 = False
Type18 = 'A'
Ident18 = 'L'

# Algebraic --> P_total
states19 = ['DFIG_Lx', 'DFIG_Ly', 'PCCUx_', 'PCCUy_']
dot19_x = ['Qtotal']
constraints_assign19 = []
constraints_combi19 = []
bias19 = False
Type19 = 'A'
Ident19 = 'L'

# Algebraic --> Ix
states20 = ['Ird_ro', 'pigd_ro']
dot20_x = ['DFIG_Ix']
constraints_assign20 = [('DFIG_Ix','Ird_ro',1),
                        ('DFIG_Ix','pigd_ro',1)]
constraints_combi20 = []
bias20 = False
Type20 = 'A'
Ident20 = 'L'

# Algebraic --> Iy
states21 = ['Irq_ro', 'pigq_ro']
dot21_x = ['DFIG_Iy']
constraints_assign21 = [('DFIG_Iy','Irq_ro',1),
                        ('DFIG_Iy','pigq_ro',1)]
constraints_combi21 = []
bias21 = False
Type21 = 'A'
Ident21 = 'L'

# Algebraic --> Usd, Usq
states22 = ['Isd', 'Isq', 'ptheta_pll_pi']
dot22_x = ['Ird_ro', 'Irq_ro']
constraints_assign22 = []
constraints_combi22 = []
bias22 = False
Type22 = 'A'
Ident22 = 'L'

# Algebraic --> Usdg, Usqg
states23 = ['pigd', 'pigq', 'gtheta_pll']
dot23_x = ['pigd_ro', 'pigq_ro']
constraints_assign23 = []
constraints_combi23 = []
bias23 = False
Type23 = 'A'
Ident23 = 'L'

# Algebraic --> Usdg, Usqg
states24 = ['ptheta_pll']
dot24_x = ['ptheta_pll_pi']
constraints_assign24 = []
constraints_combi24 = []
bias24 = True
Type24 = 'A'
Ident24 = 'L'

