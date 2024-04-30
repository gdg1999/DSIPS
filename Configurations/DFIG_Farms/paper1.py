# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 16:04:29 2023

@author: Gregory_Guo
"""

from Algo import System_Build as SB
from Tools import Model_Analysis
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use( ['science',"grid","ieee"])

color_dict = {
    "classic":[(205/255,92/255,92/255),(60/255,179/255,113/255),(65/255,105/255,225/255)],
    "千里江山":[(117/255,159/255,107/255),(189/255,144/255,43/255),(70/255,141/255,165/255)],
    "琉璃":[(145/255,187/255,221/255),(33/255,65/255,107/255),(172/255,75/255,71/255)],
    "天青":[(70/255,128/255,139/255),(143/255,209/255,225/255),(194/255,225/255,230/255)],
    "玄泽":[(143/255,110/255,103/255),(220/255,169/255,104/255),(56/255,5/255,9/255)]
    }


Block_num = 13
Algebra_num = 10

# print("Now configure the files1...\n")
# ### Algorithm Parameters
# Time_windows = 0.01       # [s] simulation time
# Shift_windows = 0.1      # [s] simulation time

# m = r"C:\Users\29639\Desktop\研二上研究\论文二：Equivalent Modeling for Wind Farms via Physical-informed Sparse Regression\paper1\data\System_stable.csv"  # files root
# source = ('PowerFactory', m)
# windows_num = 1
# print("Configure1 Finished...\n")

# # System generation
# Stable = SB.System('Stable', Block_num, Algebra_num, source, 
#              windows_num, Time_windows, Shift_windows)

# train_list = [1]
# print(f"Now train the model with list {train_list[0]} to {train_list[-1]}\n")
# Stable.Block_generation(train_list, train_list)
# print("Finished, close the Simulink...\n")

# # Other processing
# print("Now error analysis:\n")
# for num in range(Block_num + Algebra_num):
#     Stable.Blocks[num].Error_analysis()  # Error Analysis


m = r"C:\Users\29639\Desktop\研二上研究\论文二：Equivalent Modeling for Wind Farms via Physical-informed Sparse Regression\paper1\data\System_stable.csv"
data_stable = pd.read_csv(m)

Ptotal_predicted1 = data_stable['Ptotal'].to_numpy()
Ptotal_real1 = Ptotal_predicted1

Qtotal_predicted1 = data_stable['Qtotal'].to_numpy()
Qtotal_real1 = Qtotal_predicted1

PCC_x_predicted1 = data_stable['PCCUx_'].to_numpy()
PCC_x_real1 = PCC_x_predicted1

PCC_y_predicted1 = data_stable['PCCUy_'].to_numpy()
PCC_y_real1 = PCC_y_predicted1

################################################################################################

print("Now configure the files2...\n")
### Algorithm Parameters
Time_windows = 0.3       # [s] simulation time
Shift_windows = 0.1      # [s] simulation time

m = r"C:\Users\29639\Desktop\研二上研究\论文二：Equivalent Modeling for Wind Farms via Physical-informed Sparse Regression\paper1\data\System_fault2ing.csv"  # files root
source = ('PowerFactory', m)
windows_num = 1
print("Configure2 Finished...\n")

# System generation
fault1ing = SB.System('fault1ing', Block_num, Algebra_num, source, 
             windows_num, Time_windows, Shift_windows)

train_list = [1]
print(f"Now train the model with list {train_list[0]} to {train_list[-1]}\n")
fault1ing.Block_generation(train_list, train_list)

# Other processing
print("Now error analysis:\n")
for num in range(Block_num + Algebra_num):
    fault1ing.Blocks[num].Error_analysis()  # Error Analysis

Length = int(0.3 * 1e4 - 2)
win_num = 1

b_num = 12 - 1
train_num = 1
PCC_x_y_predicted2 = eval(f'fault1ing.Blocks[{b_num}].identified').simulate(eval(f'fault1ing.Blocks[{b_num}].train[{train_num-1}]')[0, :],
                                                            t = fault1ing.t_test[0:Length+1].reshape(-1),
                                                            u = eval(f'fault1ing.Blocks[{b_num}].input_dot_data[{train_num-1}]')[0:Length+1, :])
PCC_x_y_real2 = eval(f'fault1ing.Blocks[{b_num}].train[{train_num-1}]')[0:Length, :]

b_num = 22 - 1
train_num = 1
Ptotal_predicted2 = eval(f'fault1ing.Blocks[{b_num}].identified').predict(eval(f'fault1ing.Blocks[{b_num}].train[{train_num-1}]')[0:Length,:])
Ptotal_real2 = eval(f'fault1ing.Blocks[{b_num}].input_dot_data[{train_num-1}]')[0:Length , 0]
b_num = 23 - 1
train_num = 1
Qtotal_predicted2 = eval(f'fault1ing.Blocks[{b_num}].identified').predict(eval(f'fault1ing.Blocks[{b_num}].train[{train_num-1}]')[0:Length,:])
Qtotal_real2 = eval(f'fault1ing.Blocks[{b_num}].input_dot_data[{train_num-1}]')[0:Length , 0]


################################################################################################

print("Now configure the files3...\n")
### Algorithm Parameters
Time_windows = 0.7       # [s] simulation time
Shift_windows = 0.2      # [s] simulation time

m = r"C:\Users\29639\Desktop\研二上研究\论文二：Equivalent Modeling for Wind Farms via Physical-informed Sparse Regression\paper1\data\System_fault2ed_small.csv"  # files root
source = ('PowerFactory', m)
windows_num = 1
print("Configure3 Finished...\n")

# System generation
fault1ed_large = SB.System('fault1ed_large', Block_num, Algebra_num, source, 
             windows_num, Time_windows, Shift_windows)

train_list = [1]
print(f"Now train the model with list {train_list[0]} to {train_list[-1]}\n")
fault1ed_large.Block_generation(train_list, train_list)

# Other processing
print("Now error analysis:\n")
for num in range(Block_num + Algebra_num):
    fault1ed_large.Blocks[num].Error_analysis()  # Error Analysis
    
print("Now draw the picture:\n")
Length = int(0.7 * 1e4 - 2)
win_num = 1

fault1ed_large.Figure_plot(Length, win_num)
fault1ing.Figure_paper_R(Length, [1,3,5,8,2,4,6,9], 1, [2,4])



Length = int(0.7 * 1e4 - 2)
win_num = 1

b_num = 12 - 1
train_num = 1
PCC_x_y_predicted3 = eval(f'fault1ed_large.Blocks[{b_num}].identified').simulate(eval(f'fault1ed_large.Blocks[{b_num}].train[{train_num-1}]')[0, :],
                                                            t = fault1ed_large.t_test[0:Length+1].reshape(-1),
                                                            u = eval(f'fault1ed_large.Blocks[{b_num}].input_dot_data[{train_num-1}]')[0:Length+1, :])
PCC_x_y_real3 = eval(f'fault1ed_large.Blocks[{b_num}].train[{train_num-1}]')[0:Length, :]

b_num = 22 - 1
train_num = 1
Ptotal_predicted3 = eval(f'fault1ed_large.Blocks[{b_num}].identified').predict(eval(f'fault1ed_large.Blocks[{b_num}].train[{train_num-1}]')[0:Length,:])
Ptotal_real3 = eval(f'fault1ed_large.Blocks[{b_num}].input_dot_data[{train_num-1}]')[0:Length , 0]

b_num = 23 - 1
train_num = 1
Qtotal_predicted3 = eval(f'fault1ed_large.Blocks[{b_num}].identified').predict(eval(f'fault1ed_large.Blocks[{b_num}].train[{train_num-1}]')[0:Length,:])
Qtotal_real3 = eval(f'fault1ed_large.Blocks[{b_num}].input_dot_data[{train_num-1}]')[0:Length , 0]

## combine all of the data

Ptotal_real = np.concatenate([Ptotal_real1, Ptotal_real2, Ptotal_real3])
Ptotal_predicted = np.concatenate([Ptotal_predicted1, np.squeeze(Ptotal_predicted2), np.squeeze(Ptotal_predicted3)])

Qtotal_real = np.concatenate([Qtotal_real1, Qtotal_real2, Qtotal_real3])
Qtotal_predicted = np.concatenate([Qtotal_predicted1, np.squeeze(Qtotal_predicted2), np.squeeze(Qtotal_predicted3)])

PCC_x_real = np.concatenate([PCC_x_real1, PCC_x_y_real2[:,0], PCC_x_y_real3[:,0]])
PCC_x_predicted = np.concatenate([PCC_x_predicted1, PCC_x_y_predicted2[:,0], PCC_x_y_predicted3[:,0]])

PCC_y_real = np.concatenate([PCC_y_real1, PCC_x_y_real2[:,1], PCC_x_y_real3[:,1]])
PCC_y_predicted = np.concatenate([PCC_y_predicted1, PCC_x_y_predicted2[:,1], PCC_x_y_predicted3[:,1]])


tmin = 1
tmax = int(1.2*10000)

# 生成时间序列
time_interval = 1e-4
time_ = np.arange(0, len(Ptotal_real) * time_interval, time_interval)

plt.plot(time_[tmin:tmax], Ptotal_real[tmin:tmax])
plt.plot(time_[tmin:tmax], Ptotal_predicted[tmin:tmax])

plt.plot(time_[tmin:tmax], Qtotal_real[tmin:tmax])
plt.plot(time_[tmin:tmax], Qtotal_predicted[tmin:tmax])

plt.plot(time_[tmin:tmax], PCC_x_real[tmin:tmax])
plt.plot(time_[tmin:tmax], PCC_x_predicted[tmin:tmax])

plt.plot(time_[tmin:tmax], PCC_y_real[tmin:tmax])
plt.plot(time_[tmin:tmax], PCC_y_predicted[tmin:tmax])

# dqo transform for Uabc
def dq0_transform(ud, uq, t):

    # Transformation matrix
    T = np.array([
        [np.cos(2*np.pi*50*t), np.sin(2*np.pi*50*t)],
        [np.cos(2*np.pi*50*t-(2*np.pi/3)), np.sin(2*np.pi*50*t-(2*np.pi/3))],
        [np.cos(2*np.pi*50*t+(2*np.pi/3)), np.sin(2*np.pi*50*t)+(2*np.pi/3)]
    ])

    # Input vector
    abc_vector = np.sqrt(2/3)*T@np.array([[ud],[uq]])

    # Extract components
    ua = abc_vector[0]
    ub = abc_vector[1]
    uc = abc_vector[2]

    return ua, ub, uc

# calculate the amplitude of U
def Uamp(ud, uq):
    
    temp = ud**2 + uq**2
    U = np.sqrt(temp)/(230000*(np.sqrt(2)/np.sqrt(3)))-0.146
    
    return U
    


Ua_real = []
Ub_real = []
Uc_real = []

for t in range(len(time_)):
    ua, ub, uc = dq0_transform(PCC_x_real[t], PCC_y_real[t], time_[t])
    Ua_real.append(ua.tolist()[0])
    Ub_real.append(ub.tolist()[0])
    Uc_real.append(uc.tolist()[0])

Ua_predicted = []
Ub_predicted = []
Uc_predicted = []

for t in range(len(time_)-1):
    ua, ub, uc = dq0_transform(PCC_x_predicted[t], PCC_y_predicted[t], time_[t])
    Ua_predicted.append(ua.tolist()[0])
    Ub_predicted.append(ub.tolist()[0])
    Uc_predicted.append(uc.tolist()[0])
    

AU_real = []

for t in range(len(time_)):
    AU = Uamp(PCC_x_real[t], PCC_y_real[t])
    AU_real.append(AU)


AU_predicted = []

for t in range(len(time_)-1):
    AU = Uamp(PCC_x_predicted[t], PCC_y_predicted[t])
    AU_predicted.append(AU)

plt.plot(time_[tmin:tmax], AU_real[tmin:tmax])
plt.plot(time_[tmin:tmax], AU_predicted[tmin:tmax])
  
plt.plot(time_[tmin:tmax], Ua_real[tmin:tmax])
plt.plot(time_[tmin:tmax], Ua_predicted[tmin:tmax])

plt.plot(time_[tmin:tmax], Ub_predicted[tmin:tmax])
plt.plot(time_[tmin:tmax], Ub_real[tmin:tmax])

plt.plot(time_[tmin:tmax], Uc_real[tmin:tmax])
plt.plot(time_[tmin:tmax], Uc_predicted[tmin:tmax])

#### generate subplot
def generate_subplots(rows, cols, subplot_data, Length):
    xmin = 0.5*Length*1e-4
    xmax = Length*1e-4
    fig, axs = plt.subplots(rows, cols, figsize=(10, 11), sharex=True, layout='constrained')
    for ax, Data in zip(axs.flat, subplot_data):
        x, y, title, color, linestyle, linewidth, xlabel, ylabel = Data
        # ax.set_title(title)
        ax.set_ylabel(ylabel,fontsize=25)
        ax.tick_params('y', labelsize=23)
        ax.tick_params('x', labelsize=23)
        ax.ticklabel_format(style='sci', scilimits=(-1,2),axis='y')
        ax.yaxis.get_offset_text().set_fontsize(23)
        # ax.set_xlabel("t(s)",fontsize=22)
        # ax.axvspan(xmin=xmin,xmax=xmax,facecolor=color_dict["琉璃"][0],alpha=0.2)
        ax.axvline(x=0.014*Length*1e-4, ls='-.')
        ax.axvline(x=0.44*Length*1e-4, ls='-.')
        ax.set_xlim(0.005, xmax)
        label_ = ['Distributed','Aggregation']
        for len_y in range(len(y)):
            ax.plot(x, y[len_y],
                    color=color[len_y],
                    linestyle=linestyle[len_y],
                    linewidth=linewidth[len_y],
                    label=label_[len_y])
        axs[0].legend(fontsize=25, frameon=False,loc = 'lower right')

        fig.supxlabel('Time(s)',fontsize=25)
        fig.tight_layout()
        # plt.savefig ( "test.svg", format = "svg")
        # fig.supylabel('XLAgg',fontsize=20)

color = [color_dict["classic"][2],color_dict["classic"][0],color_dict["天青"][0],color_dict["玄泽"][0]]
linetype = ['-','--','-.','-.']
linewidth = [3,3,2,2]
subplot_data = [(time_[tmin:tmax], [AU_real[tmin:tmax], AU_real[tmin:tmax]], 'Subplot 1', color, linetype, linewidth, 'x',  'Voltage amplitude (p.u.)'),
                (time_[tmin:tmax], [Ptotal_real[tmin:tmax], Ptotal_predicted[tmin:tmax]], 'Subplot 2', color, linetype, linewidth, 'x', 'Active power (p.u.)'),
                (time_[tmin:tmax], [Qtotal_real[tmin:tmax], Qtotal_predicted[tmin:tmax]], 'Subplot 3', color, linetype, linewidth, 'x', 'Reactive power (p.u.)')]

generate_subplots(3, 1, subplot_data, Length)

begin = 50
gap = 500
linewidth = [2,2,2,2]
subplot_data = [(time_[begin:begin+gap], [AU_real[begin:begin+gap], AU_real[begin:begin+gap]], 'Subplot 1', color, linetype, linewidth, 'x',  'Voltage amplitude (p.u.)'),
                (time_[begin:begin+gap], [Ptotal_real[begin:begin+gap], Ptotal_predicted[begin:begin+gap]], 'Subplot 2', color, linetype, linewidth, 'x', 'Active power (p.u.)'),
                (time_[begin:begin+gap], [Qtotal_real[begin:begin+gap], Qtotal_predicted[begin:begin+gap]], 'Subplot 3', color, linetype, linewidth, 'x', 'Reactive power (p.u.)')]
generate_subplots(3, 1, subplot_data, gap)

### for linearization, damp analysis
# DFIG_ana = Model_Analysis.Analysis(DFIG, ['UD','UQ'], ['Usd'])
fault1ed_large_ana = Model_Analysis.Analysis(fault1ed_large, ['UD_averaged', 'UQ_averaged', 'Wind_averaged'], ['TL_averaged','Te_averaged'])
# DFIG_ana = Model_Analysis.Analysis(DFIG, ['UD1', 'UQ1', 'UD2', 'UQ2'], ['P_right', 'Qright', 'P_left', 'Qleft'])
# DFIG_ana = Model_Analysis.Analysis(DFIG, ['S1UD', 'S1UQ', 'S2UD', 'S2UQ'], ['P_right', 'Qright', 'P_left', 'Qleft'])
fault1ed_large_ana.Jacobian_mat()
ret = fault1ed_large_ana.Damp_analysis()
filter_poles = fault1ed_large_ana.Plot_range_poles(ret[2], [-20,5], [-100,100])


#### fourier transfrom from matlab, used for small disturbance
from scipy.io import loadmat

# 指定.mat文件的路径
mat_f = r"C:\Users\29639\Desktop\研二上研究\论文二：Equivalent Modeling for Wind Farms via Physical-informed Sparse Regression\paper1\data\f_2.mat"  # files root
mat_P1 = r"C:\Users\29639\Desktop\研二上研究\论文二：Equivalent Modeling for Wind Farms via Physical-informed Sparse Regression\paper1\data\P1_2.mat"  # files root
mat_TT = r"C:\Users\29639\Desktop\研二上研究\论文二：Equivalent Modeling for Wind Farms via Physical-informed Sparse Regression\paper1\data\TT.mat"  # files root
mat_PP = r"C:\Users\29639\Desktop\研二上研究\论文二：Equivalent Modeling for Wind Farms via Physical-informed Sparse Regression\paper1\data\pp.mat"  # files root

# 使用loadmat函数加载.mat文件
mat_f = loadmat(mat_f)
mat_P1 = loadmat(mat_P1)
mat_TT = loadmat(mat_TT)
mat_PP = loadmat(mat_PP)
# mat_data现在是一个字典，包含.mat文件中的所有变量
# 你可以通过变量名来访问具体的数据
variable_name = 'f'
f = mat_f[variable_name]

variable_name = 'P1'
P1 = mat_P1[variable_name]

variable_name = 'tt'
TT = mat_TT[variable_name]

variable_name = 'PP'
PP = mat_PP[variable_name]

# 现在，your_data包含了.mat文件中名为'your_variable_name'的变量的数据

plt.plot(np.transpose(f)[1:100], P1[1:100]) 
plt.plot(TT, PP)

fig, axs = plt.subplots(2, 1, figsize=(10, 6), layout='constrained')
axs[0].plot(TT, PP, color=color_dict["classic"][2], linestyle='-', linewidth=3)
axs[1].plot(np.transpose(f)[1:550], 2*P1[1:550], color=color_dict["classic"][0], linestyle='-', linewidth=3) 

axs[0].set_xlabel("Times (s)",fontsize=25)
axs[1].set_xlabel("Frequency (Hz)",fontsize=25)

axs[0].set_ylabel('Active power (p.u.)',fontsize=22)
axs[1].set_ylabel("Power spectral density",fontsize=22)

axs[0].tick_params('y', labelsize=23)
axs[0].tick_params('x', labelsize=23)
axs[1].tick_params('y', labelsize=23)
axs[1].tick_params('x', labelsize=23)
fig.tight_layout()
