# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 14:28:43 2023

@author: Gregory_Guo
"""

"""
This is for Coefficient Analysis for identified model
Mainly for sensitivity analysis and dominant dynamic analysis
"""

import matplotlib.pyplot as plt
# plt.style.use( ['science',"grid","ieee"])
import numpy as np
from Tools import PIC as pic


def Coefficients_Analysis(Models, block_num_dominant, train_series):
    """
    block_num_dominant is a list and train_series is also a list
    for example: train_series = [1,2,3,4,5]
                 block_num_dominant = [1,3,5,7]
                 Models are all of the blocks in the system, which is a list
                 Models[b_num-1].Midentified_dict[batch_num].coefficients()
                 train_series = [[1],[1,2],[1,2,3],[1,2,3,4]]
    """
    coef_stds_dic = {}  # return value for analyze
    # basic parameters calculation
    for b_num in block_num_dominant:  # block equations
        coef_stds = []
        for eq_num in range(Models[b_num-1].Midentified_dict[0].coefficients().shape[0]):  # equation numbers
            row_list = []
            vector_length = Models[b_num-1].Midentified_dict[0].coefficients().shape[1]
            coefficient_eq = np.empty((0, vector_length))
            for batch_num in range(len(train_series)):  # train batch, order starts from 0
                new_row = Models[b_num-1].Midentified_dict[batch_num].coefficients()[eq_num]
                row_list.append(new_row)
            for row_num in row_list:  # create the coefficients matrix
                coefficient_eq = np.vstack((coefficient_eq, row_num))
            coef_stds.append(np.std(coefficient_eq, axis = 0))  # all of the equations
        coef_stds_dic[f'{b_num}'] = coef_stds  # for each blocks
    
    return coef_stds_dic


def Coefficients_plot(coef_stds_dic, block_num_dominant):
    plot_index = 0
    # basic parameters for picture
    color = [pic.color_dict["琉璃"][1],pic.color_dict["琉璃"][2],pic.color_dict["天青"][0],pic.color_dict["玄泽"][0]]
    fig, axs = plt.subplots(len(block_num_dominant), 1, figsize=(2, 3.2))
    for b_num in block_num_dominant:  # block equations
        # Loop over the different post-processed coefficients
        coef_stds = coef_stds_dic[f'{b_num}']
        for k, coef_std in enumerate(coef_stds):
            for std in range(coef_std.shape[0]):
                col_num = coef_stds[0].shape[0]
                axs[plot_index].errorbar(range(col_num), (k+1)*np.ones((1,col_num)).reshape(col_num), yerr = coef_std/2, 
                             fmt='o', markersize=0.5, color=color[k]
                             )
            axs[plot_index].set_xticks(range(col_num))

            plt.xticks(fontsize=8)
            plt.yticks(fontsize=8)
            plt.grid(True)
            plt.tight_layout()
        plot_index = plot_index + 1

    return coef_stds_dic


def block_matrix_normalized(Model_coefficient, block_num_dominant):
    """
    normalized the variance into -0.5 to 0.5
    """
    max_values = {}
    min_values = {}
    
    for key, value_list in Model_coefficient.items():
        max_arr = None
        min_arr = None
        
        for arr in value_list:
            if max_arr is None or arr.max() > max_arr.max():
                max_arr = arr.max()
            if min_arr is None or arr.min() < min_arr.min():
                min_arr = arr.min()
        
        max_values[key] = max_arr
        min_values[key] = min_arr
    
    for b_num in block_num_dominant:
        model_list = Model_coefficient[f"{b_num}"]
        gap = (max_values[f"{b_num}"] - min_values[f"{b_num}"])
        for e_num in range(len(model_list)):
            Model_coefficient[f"{b_num}"][e_num] = (Model_coefficient[f"{b_num}"][e_num] - min_values[f"{b_num}"])/gap
    Model_coefficient_stds = Model_coefficient
    
    return Model_coefficient_stds
