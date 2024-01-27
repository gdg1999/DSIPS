# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 14:43:20 2023

@author: Gregory_Guo
"""

"""
DFIG_HVDC Configuration files
state order specify the order of the equation
"""

sys_inputs = ['S1UD', 'S1UQ', 'S2UD', 'S2UQ']
sys_outputs = ['P_right', 'Qright', 'P_left', 'Qleft']


# Block1 --> Electrical left
states1 = ['Icd1', 'Icq1']
inputs1 = ['Usd1', 'Usq1', 'Ucd1', 'Ucq1']
constraints_assign1 = []
constraints_combi1 = []
bias1 = False
Type1 = 'B'
Ident1 = 'L'

# Block2 --> Electrical right
states2 = ['Icd2', 'Icq2']
inputs2 = ['Usd2', 'Usq2', 'Ucd2', 'Ucq2']     
constraints_assign2 = []
constraints_combi2 = []
bias2 = False
Type2 = 'B'
Ident2 = 'L'

# Block3 --> Capacitor left
states3 = ['pVdc1']
inputs3 = ['P_left', 'id1']
constraints_assign3 = []
constraints_combi3 = []
bias3 = False
Type3 = 'B'
Ident3 = 'L'

# Block4 --> Capacitor right
states4 = ['pVdc2']
inputs4 = ['P_right', 'id2']     
constraints_assign4 = []
constraints_combi4 = []
bias4 = True
Type4 = 'B'
Ident4 = 'L'

# Block5 --> Transimission line
states5 = ['pId_dc']
inputs5 = ['Vleft', 'Vright']
constraints_assign5 = []
constraints_combi5 = []
bias5 = False
Type5 = 'B'
Ident5 = 'L'

# Block6 --> Control left
states6 = ['pPhia1', 'pPhib1', 'pPhic1', 'pPhid1']
inputs6 = ['Icd1', 'Icq1', 'pVdc1', 'Qleft']
constraints_assign6 = []
constraints_combi6 = []
bias6 = True
Type6 = 'B'
Ident6 = 'L'

# Block7 --> Control right
states7 = ['pPhia2', 'pPhib2', 'pPhic2', 'pPhid2']
inputs7 = ['Icd2', 'Icq2', 'Pright', 'Qright']
constraints_assign7 = []
constraints_combi7 = []
bias7 = True
Type7 = 'B'
Ident7 = 'L'

# Block8 --> PLL_left
states8 = ['pLPLL_PI', 'pLPLL_THETA']
inputs8 = ['Usd1', 'Usq1']
constraints_assign8 = []
constraints_combi8 = []
bias8 = True
Type8 = 'B'
Ident8 = 'L'

# Block9 --> PLL_right
states9 = ['pHRPLL_PI', 'pRPLL_THETA']
inputs9 = ['Usd2', 'Usq2'] 
constraints_assign9 = []
constraints_combi9 = []
bias9 = False
Type9 = 'B'
Ident9 = 'L'

# for transmission line
# DFIG_C
states10 = ['UD', 'UQ']
inputs10 = ['DFIG_Ix', 'DFIG_Iy', 'DFIG_Lx', 'DFIG_Ly']
constraints_assign10 = []
constraints_combi10 = []
bias10 = False
Type10 = 'B'
Ident10 = 'L'
# DFIG_L
states11 = ['DFIG_Lx', 'DFIG_Ly']
inputs11 = ['UD', 'UQ', 'PCCUx', 'PCCUy']
constraints_assign11 = []
constraints_combi11 = []
bias11 = False
Type11 = 'B'
Ident11 = 'L'
# PCC
states12 = ['PCCUx', 'PCCUy']
inputs12 = ['DFIG_Lx', 'DFIG_Ly', 'HVDC_Lx1', 'HVDC_Ly1', 'infL_x', 'infL_y']
constraints_assign12 = []
constraints_combi12 = []
bias12 = False
Type12 = 'B'
Ident12 = 'L'
# inf_L
states13 = ['infL_x', 'infL_y']
inputs13 = ['S1UD', 'S1UQ', 'PCCUx', 'PCCUy']
constraints_assign13 = []
constraints_combi13 = []
bias13 = False
Type13 = 'B'
Ident13 = 'L'
# HVDC_C
states14 = ['UD2', 'UQ2']
inputs14 = ['HVDC_Lx2', 'HVDC_Ly2', 'HVDC_Lx', 'HVDC_Ly']
constraints_assign14 = []
constraints_combi14 = []
bias14 = False
Type14 = 'B'
Ident14 = 'L'
# HVDC_L
states15 = ['HVDC_Lx', 'HVDC_Ly']
inputs15 = ['S2UD', 'S2UQ', 'UD2', 'UD2']
constraints_assign15 = []
constraints_combi15 = []
bias15 = False
Type15 = 'B'
Ident15 = 'L'


# DFIG
# Block1 --> Asynchronous Machine
states16 = ['Ird', 'Irq', 'Isd', 'Isq']
inputs16 = ['Urd', 'Urq', 'Usd', 'Usq']
constraints_assign16 = []
constraints_combi16 = []
bias16 = False
Type16 = 'B'
Ident16 = 'L'

# Block2 --> Grid Filter
states17 = ['pigd', 'pigq']
inputs17 = ['Usdg', 'Usqg', 'Vrefd', 'Vrefq']     
constraints_assign17 = []
constraints_combi17 = []
bias17 = False
Type17 = 'B'
Ident17 = 'L'

# Block3 --> Swing Equations
states18 = ['pwm']
inputs18 = ['Te', 'TL']
constraints_assign18 = []
constraints_combi18 = []
bias18 = False
Type18 = 'B'
Ident18 = 'L'

# Block4 --> Capacitor
states19 = ['pVdc']
inputs19 = ['Prsc', 'Pgsc']     
constraints_assign19 = []
constraints_combi19 = []
bias19 = True
Type19 = 'B'
Ident19 = 'L'

# Block5 --> RSC
states20 = ['pPhira', 'pPhirb', 'pPhirc']
inputs20 = ['Ird', 'Irq', 'pwm']
constraints_assign20 = []
constraints_combi20 = []
bias20 = True
Type20 = 'B'
Ident20 = 'L'

# Block6 --> GSC
states21 = ['pPhiga', 'pPhigb', 'pPhigc']
inputs21 = ['pVdc', 'pigd', 'pigq']
constraints_assign21 = []
constraints_combi21 = []
bias21 = True
Type21 = 'B'
Ident21 = 'L'

# Block7 --> Axis
states22 = ['pTurbine_w', 'pshaft_w']
inputs22 = ['pwm', 'Wind']
constraints_assign22 = []
constraints_combi22 = []
bias22 = False
Type22 = 'B'
Ident22 = 'L'

# Block8 --> PLL_rsc
states23 = ['pRPLL_PI', 'ptheta_pll']
inputs23 = ['UD', 'UQ']
constraints_assign23 = []
constraints_combi23 = []
bias23 = True
Type23 = 'B'
Ident23 = 'L'

# Block9 --> PLL_gsc
states24 = ['pGPLL_PI', 'gtheta_pll']
inputs24 = ['UD', 'UQ'] 
constraints_assign24 = []
constraints_combi24 = []
bias24 = False
Type24 = 'B'
Ident24 = 'L'

# Algebraic --> TL
states25 = ['pTurbine_w', 'pshaft_w', 'pwm']
dot25_x = ['TL']
constraints_assign25 = []
constraints_combi25 = []
bias25 = False
Type25 = 'A'
Ident25 = 'L'

# Algebraic --> Te
states26 = ['Ird', 'Irq', 'Isd', 'Isq']
dot26_x = ['Te']
constraints_assign26 = []
constraints_combi26 = []
bias26 = False
Type26 = 'A'
Ident26 = 'L'

# Algebraic --> Prsc
states27 = ['Ird', 'Irq', 'Urd', 'Urq']
dot27_x = ['Prsc']
constraints_assign27 = []
constraints_combi27 = []
bias27 = False
Type27 = 'A'
Ident27 = 'L'

# Algebraic --> Pgsc
states28 = ['pigd', 'pigq', 'Usdg', 'Usqg']
dot28_x = ['Pgsc']
constraints_assign28 = []
constraints_combi28 = []
bias28 = False
Type28 = 'A'
Ident28 = 'L'

# Algebraic --> Usd, Usq
states29 = ['UD', 'UQ', 'ptheta_pll']
dot29_x = ['Usd', 'Usq']
constraints_assign29 = []
constraints_combi29 = []
bias29 = True
Type29 = 'A'
Ident29 = 'L'

# Algebraic --> Usdg, Usqg
states30 = ['UD', 'UQ', 'gtheta_pll']
dot30_x = ['Usdg', 'Usqg']
constraints_assign30 = []
constraints_combi30 = []
bias30 = False
Type30 = 'A'
Ident30 = 'L'

# Algebraic --> Vrefd, Vrefq
states31= ['pigd', 'pigq', 'pPhiga', 'pPhigb', 'pPhigc', 'pVdc', 'Usdg', 'Usqg']
dot31_x = ['Vrefd', 'Vrefq']
constraints_assign31 = []
constraints_combi31 = []
bias31 = True
Type31 = 'A'
Ident31 = 'L'

# Algebraic --> Vrefq
states32= ['Ird', 'Irq', 'pPhira', 'pPhirb', 'pPhirc', 'pwm']
dot32_x = ['Urd', 'Urq']
constraints_assign32 = []
constraints_combi32 = []
bias32 = True
Type32 = 'A'
Ident32 = 'L'


# HVDC
# Algebraic --> P_right
states33 = ['Icd2', 'Icq2', 'Ucd2', 'Ucq2']
dot33_x = ['P_right']
constraints_assign33 = []
constraints_combi33 = []
bias33 = False
Type33 = 'A'
Ident33 = 'L'

# Algebraic --> Pright
states34 = ['Icd2', 'Icq2', 'Usd2', 'Usq2']
dot34_x = ['Pright']
constraints_assign34 = []
constraints_combi34 = []
bias34 = False
Type34 = 'A'
Ident34 = 'L'

# Algebraic --> Q_right
states35 = ['Icd2', 'Icq2', 'Usd2', 'Usq2']
dot35_x = ['Qright']
constraints_assign35 = []
constraints_combi35 = []
bias35 = False
Type35 = 'A'
Ident35 = 'L'

# Algebraic --> P_left
states36 = ['Icd1', 'Icq1', 'Ucd1', 'Ucq1']
dot36_x = ['P_left']
constraints_assign36 = []
constraints_combi36 = []
bias36 = False
Type36 = 'A'
Ident36 = 'L'

# Algebraic --> Q_left
states37 = ['Icd1', 'Icq1', 'Usd1', 'Usq1']
dot37_x = ['Qleft']
constraints_assign37 = []
constraints_combi37 = []
bias37 = False
Type37 = 'A'
Ident37 = 'L'

# Algebraic --> Usdq1_pll
states38 = ['UD1', 'UQ1', 'pLPLL_THETA']
dot38_x = ['Usd1', 'Usq1']
constraints_assign38 = []
constraints_combi38 = []
bias38 = True
Type38 = 'A'
Ident38 = 'L'

# Algebraic --> Usdq2_pll
states39 = ['UD2', 'UQ2', 'pRPLL_THETA']
dot39_x = ['Usd2', 'Usq2']
constraints_assign39 = []
constraints_combi39 = []
bias39 = False
Type39 = 'A'
Ident39 = 'L'

# Algebraic --> Ucdq1_ref
states40 = ['Icd1', 'Icq1', 'pPhia1', 'pPhib1', 'pPhic1', 'pPhid1', 'pVdc1', 'Qleft', 'Usd1', 'Usq1']
dot40_x = ['Ucd1', 'Ucq1']
constraints_assign40 = []
constraints_combi40 = []
bias40 = True
Type40 = 'A'
Ident40 = 'L'

# Algebraic --> Ucdq2_ref
states41 = ['Icd2', 'Icq2', 'pPhia2', 'pPhib2', 'pPhic2', 'pPhid2', 'Pright', 'Qright', 'Usd2', 'Usq2']
dot41_x = ['Ucd2', 'Ucq2']
constraints_assign41 = []
constraints_combi41 = []
bias41 = True
Type41 = 'A'
Ident41 = 'L'


# # Algebraic --> Q_right
# states12 = ['Icd2', 'Icq2', 'Usd2', 'Usq2']
# dot12_x = ['Qright']
# constraints_assign12 = []
# constraints_combi12 = []
# bias12 = False
# Type12 = 'A'

# # Algebraic --> P_left
# states13 = ['Icd1', 'Icq1', 'Ucd1', 'Ucq1']
# dot13_x = ['P_left']
# constraints_assign13 = []
# constraints_combi13 = []
# bias13 = False
# Type13 = 'A'

# # Algebraic --> Q_left
# states14 = ['Icd1', 'Icq1', 'Usd1', 'Usq1']
# dot14_x = ['Qleft']
# constraints_assign14 = []
# constraints_combi14 = []
# bias14 = False
# Type14 = 'A'

# # Algebraic --> Usdq1_pll
# states15 = ['UD1', 'UQ1', 'pLPLL_THETA']
# dot15_x = ['Usd1', 'Usq1']
# constraints_assign15 = []
# constraints_combi15 = []
# bias15 = True
# Type15 = 'A'

# # Algebraic --> Usdq2_pll
# states16= ['UD2', 'UQ2', 'pRPLL_THETA']
# dot16_x = ['Usd2', 'Usq2']
# constraints_assign16 = []
# constraints_combi16 = []
# bias16 = False
# Type16 = 'A'

# # Algebraic --> Ucdq1_ref
# states17= ['Icd1', 'Icq1', 'pPhia1', 'pPhib1', 'pPhic1', 'pPhid1', 'pVdc1', 'Qleft', 'Usd1', 'Usq1']
# dot17_x = ['Ucd1', 'Ucq1']
# constraints_assign17 = []
# constraints_combi17 = []
# bias17 = True
# Type17 = 'A'

# # Algebraic --> Ucdq2_ref
# states18= ['Icd2', 'Icq2', 'pPhia2', 'pPhib2', 'pPhic2', 'pPhid2', 'Pright', 'Qright', 'Usd2', 'Usq2']
# dot18_x = ['Ucd2', 'Ucq2']
# constraints_assign18 = []
# constraints_combi18 = []
# bias18 = True
# Type18 = 'A'
