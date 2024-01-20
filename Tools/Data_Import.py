# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 16:57:52 2023

@author: Gregory_Guo
"""

"""
Including the functions interface for various common software

"""

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error


def Matlab_import(m, windows_num, Time_windows, Shift_windows, sim_step, states, inputs, add_noise):
    """
    to generate the x_train_i of ith Time Windows
    and u_train_i of ith Time Windows
    input windows_num to assign the point you wanna generate
    input Time_windows and Shift_windows to designate settings
    states is a list including your states name
    and inputs is a list including your inputs name
    
    # Block1 --> Asynchronous Machine
    states1 = ['Ird', 'Irq', 'Isd', 'Isq']
    inputs1 = ['Urd', 'Urq', 'Usd', 'Usq']     # order fixed
    (x1_train1,u1_train1) = Data_Generation(1, Time_windows, Shift_windows, sim_step, states1, inputs1, True)
    (x1_train2,u1_train2) = Data_Generation(2, Time_windows, Shift_windows, sim_step, states1, inputs1, True)
    (x1_train3,u1_train3) = Data_Generation(3, Time_windows, Shift_windows, sim_step, states1, inputs1, True)
    (x1_train4,u1_train4) = Data_Generation(4, Time_windows, Shift_windows, sim_step, states1, inputs1, True)
    (x1_train5,u1_train5) = Data_Generation(5, Time_windows, Shift_windows, sim_step, states1, inputs1, True)
    
    """

    Time_points = int(Time_windows/sim_step)   # model generation period
    Shift_points = int(Shift_windows/sim_step)   # next model generation
    Data_length = Time_points   # designate the time windows by time
    
    states_num = len(states)
    inputs_num = len(inputs)

    x_train = np.array(m.eval(states[0]))[(windows_num-1)*Shift_points:(windows_num-1)*Shift_points+Time_points,:].reshape(Data_length,1)
    # we definitely have one state, so put the first one here
    # and then check if there are more states
    # slice from shift*unit to shift*unit + time_length
    if states_num > 1:
        for num1 in range(0, states_num - 1):
            x_train = np.concatenate((np.array(x_train).reshape(Data_length,num1+1),
            np.array(m.eval(states[num1+1]))[(windows_num-1)*Shift_points:(windows_num-1)*Shift_points+Time_points,:].reshape(Data_length,1)), axis=1)
    
    inputs_ = {}  # an auxiliary dictionary for one unit checking here

    for num2 in range(inputs_num):
        
        if type(m.eval(inputs[num2]))==float:  # first check if the inputs is only one constant
            value = np.array(m.eval(inputs[num2])).reshape(1,1).repeat(Data_length,axis=0)
            inputs_['inputs_{}'.format(num2)] = value
            # if it was a constant, we need repeat it
        else:
            value = np.array(m.eval(inputs[num2]))[(windows_num-1)*Shift_points:(windows_num-1)*Shift_points+Time_points,:].reshape(Data_length,1)
            inputs_['inputs_{}'.format(num2)] = value
    
    u_train = inputs_['inputs_0']  # the same, put the first one here
    if inputs_num > 1:
        for num3 in range(0, inputs_num - 1):
            u_train = np.concatenate((np.array(u_train).reshape(Data_length,num3+1),
                                      inputs_['inputs_{}'.format(num3+1)]), axis=1)
    
    if add_noise == False:  # add noise here for Matlab simulink.
        rmse = mean_squared_error(x_train, np.zeros(x_train.shape), squared=False)
        x_train = x_train + np.random.normal(0, rmse / 2000.0, x_train.shape)

    return x_train, u_train


def files_import(m, windows_num, Time_windows, Shift_windows, sim_step, states, inputs):
    """
    This is for data files, stored in cvs, may from PowerFactory, Pscad, Simulink, RT-LAB
    something like that. 
    Importantly, the structure of the data is important.
    
    All of the parameters in Different blocks are stored in one csv files.
    the names of the states are corresponding to the Configurations files
    
    """
    
    encoding = "cp1252"  # assign the coding
    data = pd.read_csv(m, encoding=encoding)
    
    Time_points = int(Time_windows/sim_step)   # model generation period
    Shift_points = int(Shift_windows/sim_step)   # next model generation
    
    x_train = data[states][(windows_num-1)*Shift_points:(windows_num-1)*Shift_points+Time_points]
    u_train = data[inputs][(windows_num-1)*Shift_points:(windows_num-1)*Shift_points+Time_points]
    
    return x_train.values, u_train.values
    

def files_time(m):
    """
    a small function to return the simulation times
    """
    
    encoding = "cp1252"  # assign the coding
    data = pd.read_csv(m, encoding=encoding)
    
    t_test = data['Times']
    
    return t_test.values.reshape(t_test.shape[0],1)
    
    