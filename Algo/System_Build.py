# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 15:21:07 2023

@author: Gregory_Guo
"""

"""
Used for system building

suitable for the block with known model
"""

from Algo import Block_Build as BB
from Tools import Figure_Plot as PF
from Tools import PIC as pic
from Tools import Data_Import as DI
from Tools import Coefficient_Analysis as CA
from scipy.io import savemat
import os
import re
from functools import partial
import pandas as pd
import numpy as np
import Configurations as C  # configuration files corresponding to your simulink


class System(object):
    """
    Class for the whole system consist of different blocks
    the model of blocks in the system are stored in a list
    """
    
    def __init__(self, Name, Block_num, Algebra_num, source, 
                 windows_num, Time_windows, Shift_windows):
        """
        In this class, data from configuration will be used here
        we have system name here and the total block number, 
        including differential block number and algebra number
        the source to decide which software to use
        windows number and the length of it, and shift length of the windows
        
        In plot function, the length of time should be equal with Time windows
        """
        
        self.Name = Name  # system name
        self.Block_num = Block_num  # dynamic blocks
        self.Algebra_num = Algebra_num  # algebra blocks
        self.source = source
        
        self.windows_num = windows_num
        self.Time_windows = Time_windows
        self.Shift_windows = Shift_windows
        
        if self.source[0] == 'Matlab':
            self.t_test = np.array(self.source[1].eval('out'))
            # name 'out' is corresponding to simulink configuration
        else:
            self.t_test = DI.files_time(self.source[1])
            
        self.dt = float(self.t_test[2]-self.t_test[1])
        
        self.Blocks = []  # store blocks models


    def Block_generation(self, xtrain_list, utrain_list):
        """
        Generate the block in the system
        with the train_list among the whole operation data
        xtrain_list should be equal with utrain_list
        """
        
        self.Blocks = []  # necessary to refresh it
        
        for block in range(self.Block_num + self.Algebra_num):  # generate in loop
                # read the data from Configuration files
                block = block + 1  # index from 1 instead of 0
                states = eval(f"C.states{block}")  # because the name in configuration starts from 0
                print(f"The states in block{block} are {states}...")
                if block < self.Block_num + 1:  # the name of input_dot is different
                    input_dot = eval(f"C.inputs{block}")
                else:
                    input_dot = eval(f"C.dot{block}_x")
                print(f"The inputs/dots in block{block} are {input_dot}...")
                # if you wanna change the constraint, necessary to restart Python
                constraints_assign = eval(f"C.constraints_assign{block}")
                constraints_combi =  eval(f"C.constraints_combi{block}")
                
                print(f"the constraint in block{block} is {constraints_assign} and {constraints_combi}")
                
                bias = eval(f"C.bias{block}")
                Type = eval(f"C.Type{block}")
                Ident_type = eval(f"C.Ident{block}")  # add nonlinear choice
                # Create each block
                block_ = BB.Block(block,  # block number
                                  self.source,  # source of files or Matlab
                                  states,  # variables from configuration
                                  input_dot,  # variables from configuration
                                  self.windows_num, 
                                  self.Time_windows, 
                                  self.Shift_windows,
                                  constraints_assign, constraints_combi,
                                  Lib = [Ident_type, 1, bias], TYPE = Type,
                                  dt = self.dt)
                                    # Poly chosen here, we identify linearized system
                
                block_.Perform(xtrain_list, utrain_list)
                self.Blocks.append(block_)  # append the block to the list


    def __Equation_Matlab(self, A_, Item_, State_, Input_, Bnum, path):
        """
        A_ is the coefficients of the block, array
        Item_ is the corresponding variable names, list
        State_ is the state variables of the block, list
        Input is the input variables of the block, list
        Bnum is the block num we generate, int
        return nothing, but generate mat data files in the files
        path is the root you write

        """
        
        if not os.path.exists(path):  # prepare for the folder in advance
            os.makedirs(path)
            
        print("===============")
        print(f"Block{Bnum}")
        eq_num = A_.shape[0] # to get the row of A
        states_num = A_.shape[1] # to get the column of A
        
        if self.Blocks[Bnum-1].Libindex[0] == 'L':
        
            if Item_[0] != '1':  # no bias
                all_items = State_ + Input_
            else:
                Item_[0] = 'one'  # with bias
                all_items = ['1'] + State_ + Input_
            
            for eq in range(eq_num):
                dic = {}
                for item in range(states_num):
                    dic[Item_[item]] = []
                    if True:
                        dic[Item_[item]].append(all_items[item])
                    dic[Item_[item]].append(A_[eq, item])
                file_name = f'Block{Bnum}_eq{eq}.mat'
                full_file_path = os.path.join(path, file_name)
                savemat(full_file_path, dic)  # in a dic way
                print(f"eq{eq}-----------------")
                print(dic)
        
        else:
            FeaList = self.Blocks[Bnum-1].constraint.fea_list
            FeaListNum = len(FeaList)  
            temp_fun = partial(self.__Equation_Matlab_Nonlinear,
                               states=State_, inputs=Input_)
            for eq in range(eq_num):
                dic = {}
                for item in range(FeaListNum):
                    dic[FeaList[item]] = []
                    fea_true = re.sub(r'([xu])(\d+)?(_dot)?',
                                      temp_fun,
                                      FeaList[item])
                    dic[FeaList[item]].append(fea_true)
                    dic[FeaList[item]].append(A_[eq, item])
                file_name = f'Block{Bnum}_eq{eq}.mat'
                full_file_path = os.path.join(path, file_name)
                savemat(full_file_path, dic)  # in a dic way
                print(f"eq{eq}-----------------")
                print(dic)
    
    
    def __Equation_Matlab_Nonlinear(self, match, states, inputs):
        """
        transfer fea_list to true name
        """
        identifier = match.group(1) # Get the matched identifier (e.g., x0, u1)
        index_match = match.group(2) # Get the number after the identifier
        index = int(index_match) if index_match is not None else None
        if identifier.startswith('x') and index is not None and 0 <= index < len(states):
            name = states[index]
        elif identifier.startswith('u') and index is not None and 0 <= index < len(inputs):
            name = inputs[index]
        else:
            name = identifier
        if match.group(3) is None:
            return name
        else:
            return name + '_dot'

    
    def __Output_batch(self, Bnum, algebraic, path):
        A = eval(f"self.Blocks[{Bnum}].identified").coefficients()
        items = eval(f"self.Blocks[{Bnum}].identified").get_feature_names()
        if algebraic:
            self.__Equation_Matlab(A, items, eval(f'C.states{Bnum+1}'), eval(f'C.dot{Bnum+1}_x'), Bnum+1, path)
        else:
            self.__Equation_Matlab(A, items, eval(f'C.states{Bnum+1}'), eval(f'C.inputs{Bnum+1}'), Bnum+1, path)


    def Batch_output(self, path):
        """
        Together with function "Equation_Matlab" and "Output_batch",
        return the model to the Simulink for analysis
        in a coefficient way
        """

        for block in range(self.Block_num + self.Algebra_num):
            
            if self.Blocks[block].type == 'A':
                index = True
            if self.Blocks[block].type == 'B':
                index = False
                
            self.__Output_batch(block, index, path)

    
    def Figure_plot(self, Data_Length, win_num):
        """
        draft plot for check, the data length should be equal with time windows
        if you wanna check the predict, you should have multi-windows and
        train the model with data, and plot with another window.
        """
        
        for b in self.Blocks:
            Model = b.identified
            x_train = b.train[win_num - 1]
            u_dot = b.input_dot_data[win_num - 1]
            dt = b.sim_step
            
            if b.type == 'B':
                PF.test_fig(Model, x_train, u_dot, Data_Length, dt, self.t_test)
            if b.type == 'A':
                PF.test_algebraic(Model, x_train, u_dot, Data_Length, self.t_test)

    
    def __paper_result_dot(self, block_num, train_num, Length, dt, t_test):
        """
        train: self.Blocks[{b_num}].train{train_num-1}
        input_dot_data: self.Blocks[{b_num}].input_dot_data{train_num-1}
        block model: Model[{b_num}].identified
        
        this is for data generation
        for state block
        remeber, only the first state in the block will be represented here
        """
        
        t_sub = list(t_test[0:Length])
        x_dot_predicted = dict()
        x_dot_computed = dict()
        for b_num in block_num:
            b_num = b_num - 1
            if b_num < self.Block_num:
                predicted = eval(f'self.Blocks[{b_num}].identified').predict(eval(f'self.Blocks[{b_num}].train[{train_num-1}]')[0:Length,:], u=eval(f'self.Blocks[{b_num}].input_dot_data[{train_num-1}]')[0:Length,:])
                computed = eval(f'self.Blocks[{b_num}].identified').differentiate(eval(f'self.Blocks[{b_num}].train[{train_num-1}]')[0:Length,:], t=dt)
                x_dot_predicted[f'self.Blocks[{b_num}].identified'] = list((predicted[:,0]))
                x_dot_computed[f'self.Blocks[{b_num}].identified'] = list((computed[:,0]))
            else:
                predicted = eval(f'self.Blocks[{b_num}].identified').predict(eval(f'self.Blocks[{b_num}].train[{train_num-1}]')[0:Length,:])
                computed = eval(f'self.Blocks[{b_num}].input_dot_data[{train_num-1}]')[0:Length , 0]
                x_dot_predicted[f'self.Blocks[{b_num}].identified'] = list((predicted[:,0]))
                x_dot_computed[f'self.Blocks[{b_num}].identified'] = list(computed)
            
        return (t_sub, x_dot_predicted, x_dot_computed)


    def __paper_result_real(self, block_num, train_num, Length, t_test):
        """
        train: self.Blocks[{b_num}].train{train_num-1}
        input_dot_data: self.Blocks[{b_num}].input_dot_data{train_num-1}
        block model: Model[{b_num}].identified
        
        this is for data generation
        for state block
        remeber, only the first state in the block will be represented here        
        """
        
        t_sub = t_test[0:Length]
        x_predicted = dict()
        x_real = dict()
        for b_num in block_num:
            b_num = b_num - 1
            if b_num < self.Block_num:
                # The result from sim will less than length, with a unit gap
                # eg. the length is 20000, the sim result will be 19999
                # and the data length should be equal with Length
                # what is more, the t_test is large enough, but the u only contains Length points!
                sim_ret = eval(f'self.Blocks[{b_num}].identified').simulate(eval(f'self.Blocks[{b_num}].train[{train_num-1}]')[0, :],
                                                                            t = t_test[0:Length+1].reshape(-1),
                                                                            u = eval(f'self.Blocks[{b_num}].input_dot_data[{train_num-1}]')[0:Length+1, :])
                x_real[f'self.Blocks[{b_num}].identified'] = eval(f'self.Blocks[{b_num}].train[{train_num-1}]')[0:Length, 0]
                x_predicted[f'self.Blocks[{b_num}].identified'] = sim_ret[:, 0]
            else:
                print("Only Dynamic Equations Here")

        return (t_sub, x_predicted, x_real)
    
    
    def __perform_paper_plot(self, Length, block_num_dot, train_num_dot, layout, dt, t_test):
        """
        state_variable: C.states{Bnum+1}
        input_variable: C.dot{Bnum+1}_x
        block model: Model[{b_num}].identified
        
        this is for beautifying the picture
        with method self.__paper_result_real in it
        plot state picture
        """
        
        (t_sub_dot, x_dot_predicted, x_dot_computed) = self.__paper_result_dot(block_num_dot, train_num_dot, Length, dt, t_test)
        Y_data_dot = dict()
        
        for num in block_num_dot:
            num = num - 1
            y_data_dot = []
            common_keys_dot = [f'self.Blocks[{num}].identified']  # this is a list
            for key in common_keys_dot:
                if key in x_dot_computed and key in x_dot_predicted:
                    y_data_dot.append(x_dot_computed[key])
                    y_data_dot.append(x_dot_predicted[key])
                    Y_data_dot[f'Block{num+1}'] = y_data_dot
        color = [pic.color_dict["琉璃"][1],pic.color_dict["琉璃"][2],pic.color_dict["天青"][0],pic.color_dict["玄泽"][0]]
        linetype = ['-','--','-.','-.']
        linewidth = [0.8,0.8,0.8,0.8]
        subplot_data = [(t_sub_dot, y_data_dot, 'Subplot 1', color, linetype, linewidth, 'x', y)
                        for y, y_data_dot in Y_data_dot.items()]
        
        pic.generate_subplots(layout[0], layout[1], subplot_data, Length)
        
        return (t_sub_dot, x_dot_predicted, x_dot_computed)
        
        
    def __perform_paper_plot_real(self, Length, block_num_real, train_num_real, layout, t_test):
        """
        state_variable: C.states{Bnum+1}
        input_variable: C.dot{Bnum+1}_x
        block model: Model[{b_num}].identified
        
        this is for beautifying the picture
        with method self.__paper_result_real in it
        plot real picture
        """       
        
        # real_test_paper
        (t_sub_real, x_predicted, x_real) = self.__paper_result_real(block_num_real, train_num_real, Length, t_test)
        Y_data_real = dict()
        for num in block_num_real:
            num = num - 1
            y_data_real = []
            common_keys_real = [f'self.Blocks[{num}].identified']
            for key in common_keys_real:
                if key in x_real and key in x_predicted:
                    y_data_real.append(x_real[key])
                    y_data_real.append(x_predicted[key])
                    Y_data_real[f'Block{num+1}'] = y_data_real
        color = [pic.color_dict["classic"][2],pic.color_dict["classic"][0],pic.color_dict["天青"][0],pic.color_dict["玄泽"][0]]
        linetype = ['-','--','-.','-.']
        linewidth = [3,3,1,1]
        subplot_data = [(t_sub_real, y_data_real, 'Subplot 1', color, linetype, linewidth, 'x', y)
                        for y, y_data_real in Y_data_real.items()]
        pic.generate_subplots(layout[0], layout[1], subplot_data, Length)
        
        return (t_sub_real, x_predicted, x_real)
        

    def Figure_paper_X(self, Data_Length, block_num, win_num, layout):
        """
        paper plot for derivatives
        """
        
        (t_sub_dot, x_dot_predicted, x_dot_computed) = self.__perform_paper_plot(Data_Length, block_num, win_num, layout, self.dt, self.t_test)
        
        return (t_sub_dot, x_dot_predicted, x_dot_computed)
    
    
    def Figure_paper_R(self, Data_Length, block_num, win_num, layout):
        """
        paper plot for real
        """

        (t_sub_real, x_predicted, x_real) = self.__perform_paper_plot_real(Data_Length, block_num, win_num, layout, self.t_test)
        
        return (t_sub_real, x_predicted, x_real)

    
    def Coefficient_analysis(self, block_num_dominant, train_series):
        """
        This is for Coefficient Analysis for identified model
        Mainly for sensitivity analysis and dominant dynamic analysis
        """
        
        for num in block_num_dominant:
            self.Blocks[num-1].Multi_perform(train_series)  # this is a list, start from 0
        
        self.Model_coefficient = CA.Coefficients_Analysis(self.Blocks, block_num_dominant, train_series)
        self.Model_coefficient_stds = CA.block_matrix_normalized(self.Model_coefficient, block_num_dominant)
        CA.Coefficients_plot(self.Model_coefficient_stds, block_num_dominant)
    
    
    def Info_output(self, path):
        """
        Output some information to designated file root
        Information including block training cost time, in excel form
        block training data and prediction data for drawing, in mat form
        """
        
        if not os.path.exists(path):  # prepare for the folder in advance
            os.makedirs(path)
        
        TimeList = []
        BlockName = []
        for blocks in self.Blocks:
            TimeList.append(blocks.time)
            BlockName.append("Block_"+f"{blocks.name}")
        df = pd.DataFrame(list(zip(BlockName, TimeList)), columns=['Name', 'Time(s)'])
        print("Output block cost time in excel...")
        fileName = "Cost_time.xlsx"
        full_file_path = os.path.join(path, fileName)
        df.to_excel(full_file_path, index=False)
        print("Excel file Cost_time.xlsx has been created.")
        print()
        
        # Blocks_data = {}
        # Block_dic = {}
        # for blocks in self.Blocks:
        #     block_order = blocks.name
        #     (Block_dic["Time"], Block_dic["X_predicted"], Block_dic["X_real"]) = self.__paper_result_real([block_order],
        #                                                                  1,  # for easy use
        #                                                                  int(self.Time_windows*(1/self.dt)-1),
        #                                                                  self.t_test)

        #     Blocks_data[f"{block_order}"] = Block_dic.copy()  # the real value instead of the address
        
        # print("Output real data for comparing...")
        # file_name = 'SystemSimulation.mat'
        # full_file_path = os.path.join(path, file_name)
        # savemat(full_file_path, Blocks_data)  # in a dic way
