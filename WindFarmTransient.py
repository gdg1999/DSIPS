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
plt.style.use( ['science',"grid","ieee"])

color_dict = {
    "classic":[(205/255,92/255,92/255),(60/255,179/255,113/255),(65/255,105/255,225/255)],
    "千里江山":[(117/255,159/255,107/255),(189/255,144/255,43/255),(70/255,141/255,165/255)],
    "琉璃":[(145/255,187/255,221/255),(33/255,65/255,107/255),(172/255,75/255,71/255)],
    "天青":[(70/255,128/255,139/255),(143/255,209/255,225/255),(194/255,225/255,230/255)],
    "玄泽":[(143/255,110/255,103/255),(220/255,169/255,104/255),(56/255,5/255,9/255)]
    }


Block_num = 13
# Algebra_num = 10

Algebra_num = 0


### Algorithm Parameters
Time_windows = 0.1       # [s] simulation time
Shift_windows = 0.01      # [s] simulation time


# WindFarmNum = [5,15,25]
# Square = [5,10,15,20,25,30]

WindFarmNum = [5]
Square = [5, 10]

# Iterate over each combination of elements from WindFarmNum and Square
for wind_num in WindFarmNum:
    for square_num in Square:
        # Form the filename using the combination
        file_name = f"{wind_num}_{square_num}.csv"
        print(f"Now configure the {file_name}...\n")

        m = r"C:\Users\29639\Desktop\研二下研究\paper4电工\code\Operation_state_"+f"{file_name}"  # files root
        source = ('PowerFactory', m)
        windows_num = 1
        print(f"Configure {file_name} Finished...\n")
        
        # System generation
        Transient = SB.System('Transient', Block_num, Algebra_num, source, 
                     windows_num, Time_windows, Shift_windows)
        
        train_list = [1]
        print(f"Now train the model with list {train_list[0]} to {train_list[-1]}\n")
        Transient.Block_generation(train_list, train_list)
        
        # Other processing
        print("Now error analysis:\n")
        for num in range(Block_num + Algebra_num):
            Transient.Blocks[num].Error_analysis()  # Error Analysis
        
        print("\nNow equations output:\n")
        # Transient.Batch_output()
        
        
        
        
        
        
        
        
        
        


