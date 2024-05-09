# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 12:02:36 2024

@author: Gregory_Guo
"""

from Algo import System_Build as SB
from Tools import Model_Analysis
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# plt.style.use( ['science',"grid","ieee"])
import os
from scipy.io import savemat

color_dict = {
    "classic":[(205/255,92/255,92/255),(60/255,179/255,113/255),(65/255,105/255,225/255)],
    "千里江山":[(117/255,159/255,107/255),(189/255,144/255,43/255),(70/255,141/255,165/255)],
    "琉璃":[(145/255,187/255,221/255),(33/255,65/255,107/255),(172/255,75/255,71/255)],
    "天青":[(70/255,128/255,139/255),(143/255,209/255,225/255),(194/255,225/255,230/255)],
    "玄泽":[(143/255,110/255,103/255),(220/255,169/255,104/255),(56/255,5/255,9/255)]
    }


Block_num = 13
Algebra_num = 10

# Algebra_num = 0


# WindFarmNum = [5,15,25]
# Square = [5,10,15,20,25,30]

WindFarmNum = [25]
Square = [30]

# file root check
directory = r"G:\paper4\PythonData"
if not os.path.exists(directory):
    # If it doesn't exist, create the directory
    os.makedirs(directory)
    print(f"The directory '{directory}' doesn't exist and has been successfully created.")
else:
    print(f"The directory '{directory}' already exists.")


# Iterate over each combination of elements from WindFarmNum and Square
for wind_num in WindFarmNum:
    for square_num in Square:
        # Form the filename using the combination
        file_name = f"{wind_num}_{square_num}.csv"
        print(f"Now configure the {file_name}...\n")

        m = r"G:\paper4\ExcelData\Operation_state_"+f"{file_name}"  # files root
        source = ('PowerFactory', m)
        windows_num = 2
        print(f"Configure {file_name} Finished...\n")
        
        print("Small Transient")
        
        ### Algorithm Parameters
        Time_windows = 0.65      # [s] simulation time
        Shift_windows = 0        # [s] simulation time
        # System generation
        Transient1 = SB.System('Transient1', Block_num, Algebra_num, source, 
                     windows_num, Time_windows, Shift_windows)
        
        train_list = [1]
        print(f"Now train the model with list {train_list[0]} to {train_list[-1]}\n")
        Transient1.Block_generation(train_list, train_list)
        
        print("Now draw the Tran picture:\n")
        LengthTran = int(0.65 * 1e5 - 1)
        win_numTran = 1
        
        dataplot1 = Transient1.Figure_paper_X(LengthTran, [22,23], win_numTran, [1,2])
        
        CalTranP1 = dataplot1[1]['self.Blocks[21].identified']
        CalTranQ1 = dataplot1[1]['self.Blocks[22].identified']
        
        
        print("Fault Transient")
        
        ### Algorithm Parameters
        Time_windows = 0.05       # [s] simulation time
        Shift_windows = 0.65        # [s] simulation time
        # System generation
        Transient2 = SB.System('Transient2', Block_num, Algebra_num, source, 
                     windows_num, Time_windows, Shift_windows)
        
        train_list = [2]
        print(f"Now train the model with list {train_list[0]} to {train_list[-1]}\n")
        Transient2.Block_generation(train_list, train_list)
        
        print("Now draw the Tran picture:\n")
        LengthTran = int(0.05 * 1e5 - 1)
        win_numTran = 2
        
        dataplot2 = Transient2.Figure_paper_X(LengthTran, [22,23], win_numTran, [1,2])
        
        CalTranP2 = dataplot2[1]['self.Blocks[21].identified']
        CalTranQ2 = dataplot2[1]['self.Blocks[22].identified']
        
        print("After Fault")
        
        ### Algorithm Parameters
        Time_windows = 0.3       # [s] simulation time
        Shift_windows = 0.7        # [s] simulation time
        # System generation
        Transient3 = SB.System('Transient3', Block_num, Algebra_num, source, 
                     windows_num, Time_windows, Shift_windows)
        
        train_list = [2]
        print(f"Now train the model with list {train_list[0]} to {train_list[-1]}\n")
        Transient3.Block_generation(train_list, train_list)
        
        print("Now draw the Tran picture:\n")
        LengthTran = int(0.3 * 1e5 - 1)
        win_numTran = 2
        
        dataplot3 = Transient3.Figure_paper_X(LengthTran, [22,23], win_numTran, [1,2])
        
        CalTranP3 = dataplot3[1]['self.Blocks[21].identified']
        CalTranQ3 = dataplot3[1]['self.Blocks[22].identified']
        
        Ptotal = CalTranP1 + CalTranP2 + CalTranP3
        Qtotal = CalTranQ1 + CalTranQ2 + CalTranQ3
        
        
        data_dict = {
            'Ptotal': Ptotal,
            'Qtotal': Qtotal
        }
        data_dict2 = {'Agat':data_dict}
        
        directory = r"G:\paper4\PythonData"
        fault_name = f"\Fault_{wind_num}_{square_num}.mat"
        Datapath = directory + fault_name
                
        savemat(Datapath, data_dict2)
        
        
        # # Other processing
        # print("Now error analysis:\n")
        # for num in range(Block_num + Algebra_num):
        #     Transient.Blocks[num].Error_analysis()  # Error Analysis
        
        # print("\nNow equations output:\n")
        # Transient.Batch_output(r"G:\paper4\PythonData\Para_"
        #                        +f"{wind_num}"+"_"+f"{square_num}")
        # print()
        # Transient.Info_output(r"G:\paper4\PythonData\Para_"
        #                        +f"{wind_num}"+"_"+f"{square_num}")
        # print()
        
        

print("Step 5 Finished, Please use Matlab next.")




        


