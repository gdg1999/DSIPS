# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 15:32:22 2023

@author: Gregory_Guo
"""

"""
Used for block building, related to the System_Building block
"""

import pysindy as ps
import numpy as np
from Algo import Constraint_Generation as CG
from Tools import Data_Import as DI
import copy
import time


class Block(object):
    """
    The class for block, related to System building_Block generation
    """
    
    def __init__(self, name, source, states, input_dot, 
                 windows_num, Time_windows, Shift_windows,
                 constraints_assign, constraints_combi, 
                 Lib, TYPE, dt = 1e-4, optConfig = [1e-8, 0, 'l1', 5000], 
                 add_noise = 'True'):
        """
        source = (Matlab, m)
        source = (Other, file_path)
        dt is a default here, related to the time_step of simulink
        optConfig is also a default here, specifying the optimization parameters
        add_noise is default, to chanllenge the accuracy of the identification
        """
        
        self.name = name
        self.source = source
        self.states = states
        self.input_dot = input_dot
        self.windows_num = windows_num
        self.Time_windows = Time_windows  # some of the parameters are common with the system
        self.Shift_windows = Shift_windows
        self.Noise = add_noise
        
        self.type = TYPE
        self.sim_step = dt
        self.Libindex = Lib
        self.Lib = None  # Library defined later
        self.optConfig = optConfig
        self.opt = None  # Optimizaiton defined later
        
        self.train = []  # the training data, if multi-windows exist, stored in the list
        self.input_dot_data = []  # given data, if multi-windows exist, stored in the list
        self.constraints_assign = constraints_assign
        self.constraints_combi = constraints_combi
        self.constraint = None  # a Constraint class for the block
        self.identified = None  # identified model, a pysindy class
        self.Midentified_dict = {}  # lots of identified model, for more advanced use
        
    
    def Data_generation(self):
        if self.source[0] == "Matlab":  # Matlab source
            for num in range(self.windows_num):  # scan the windows
                num = num + 1
                (x_train,u_train) = DI.Matlab_import(self.source[1],
                                                                 num, 
                                                                 self.Time_windows, 
                                                                 self.Shift_windows, 
                                                                 self.sim_step, 
                                                                 self.states, 
                                                                 self.input_dot, 
                                                                 self.Noise)
                self.train.append(x_train)  # in the list
                self.input_dot_data.append(u_train)

        else:  # files read
            for num in range(self.windows_num):
                num = num + 1
                (x_train,u_train) = DI.files_import(self.source[1],
                                                    num,
                                                    self.Time_windows,
                                                    self.Shift_windows,
                                                    self.sim_step,
                                                    self.states,
                                                    self.input_dot)
                self.train.append(x_train)
                self.input_dot_data.append(u_train)
                print(f"Now reading the data...with step {self.sim_step}")
    
    
    def Library_build(self):
        if self.Libindex[0] == 'L':  # if linearized
            self.Lib = ps.PolynomialLibrary(degree=self.Libindex[1], 
                                            include_bias=self.Libindex[2])
        
        if self.Libindex[0] == 'I':  # if implicit
            # for Capacitor is implicit
            x_library_functions = [lambda x: x]
            x_dot_library_functions = [lambda x: x]
            # library function names includes both the x_library_functions 
            # and x_dot_library_functions names
            library_function_names = [lambda x: x, lambda x: x]
            # Need to pass time base to the library so can build the x_dot library from x 
            self.Lib = ps.SINDyPILibrary(library_functions=x_library_functions,
                                            x_dot_library_functions=x_dot_library_functions,
                                            t=self.sim_step,
                                            function_names=library_function_names,
                                            include_bias=False)
        
        if self.Libindex[0] == 'S':  # if sine/cosine
            # for PLL with sin and cos
            identity_library = ps.IdentityLibrary()
            fourier_library = ps.FourierLibrary()
            # Initialize the default inputs, i.e. each library
            # uses all the input variables
            inputs_temp = np.tile([0, 1, 2, 3], 2)
            inputs_per_library = np.reshape(inputs_temp, (2, 4))
            inputs_per_library[0, 0] = 1
            # inputs_per_library[0, 1] = 0
            inputs_per_library[1, 1] = 0
            inputs_per_library[1, 2] = 0
            inputs_per_library[1, 3] = 0
            # [1 1 2 3; Identity Library with x1, u0, u1
            #  0 0 0 0] Fourier Library  with x0
            # Tensor all the polynomial and Fourier library terms together
            tensor_array = [[1, 1]]
            # Initialize this generalized library, all the work hidden from the user!
            self.Lib = ps.GeneralizedLibrary([identity_library, fourier_library], 
                                                        tensor_array=tensor_array, exclude_libraries=[1], # exclude Fourier
                                                        inputs_per_library=inputs_per_library)
        
        if len(self.Libindex[0]) == 2:
            degree = int(self.Libindex[0][1])
            self.Lib = ps.PolynomialLibrary(degree=degree, include_bias=self.Libindex[2])
    
    
    def Constraint(self):
        if self.Libindex[0] == 'L':  # if linearized
            self.constraint = CG.block_constraint(self.states, self.input_dot, 
                                            self.constraints_assign, 
                                            self.constraints_combi, 
                                            self.Libindex,
                                            self.type,
                                            self.optConfig)  # this is a default
            self.opt = self.constraint.optimizer_config()
        
        if self.Libindex[0] == 'I':  # if implicit
            model_temp = ps.SINDy(feature_library=self.Lib)
            model_temp.fit(self.train[0], u = self.input_dot_data[0], t=self.sim_step)
            
            self.constraint = CG.nonlinear_constraint(self.states,
                                                      model_temp.get_feature_names(),
                                                      self.constraints_assign,
                                                      self.constraints_combi,
                                                      self.optConfig)
            self.opt = self.constraint.optimizer_config()
            
        if self.Libindex[0] == 'S':  # if sine/cosine
            model_temp = ps.SINDy(feature_library=self.Lib)
            model_temp.fit(self.train[0], u = self.input_dot_data[0], t=self.sim_step)

            self.constraint = CG.nonlinear_constraint(self.states,
                                                      model_temp.get_feature_names(),
                                                      self.constraints_assign,
                                                      self.constraints_combi,
                                                      self.optConfig)
            self.opt = self.constraint.optimizer_config()
        
        if len(self.Libindex[0]) == 2:
            model_temp = ps.SINDy(feature_library=self.Lib)
            model_temp.fit(self.train[0], u = self.input_dot_data[0], t=self.sim_step)

            self.constraint = CG.nonlinear_constraint(self.states,
                                                      model_temp.get_feature_names(),
                                                      self.constraints_assign,
                                                      self.constraints_combi,
                                                      self.optConfig)
            self.opt = self.constraint.optimizer_config()
       
    
    def Error_analysis(self, window = 1):
        if self.type == 'B':
            print(f'Model_{self.name} score: %f' % self.identified.score(eval(f"self.train[{window-1}]"),u = eval(f"self.input_dot_data[{window-1}]"), t=self.sim_step))

        elif self.type == 'A':
            print(f'Model_{self.name} score: %f' % self.identified.score(eval(f"self.train[{window-1}]"), x_dot = eval(f"self.input_dot_data[{window-1}]"), t=self.sim_step))


    def __preparation(self):
        """
        This is the preparation for SINDy algorithm
        """
        
        self.Data_generation()
        self.Library_build()
        self.Constraint()
    
    
    def Perform(self, xtrain_list, utrain_list, method = 'SF'):
        """
        For general analysis, method is a default para
        """
        
        self.__preparation()
        
        print("You are performing:\n")
        print(f"Block{self.name}:")
        
        fd_drop_endpoints = None
        
        if method == 'FD':
            fd_drop_endpoints = ps.FiniteDifference(drop_endpoints=True)
        
        elif method == 'SF':
            fd_drop_endpoints = ps.SmoothedFiniteDifference(drop_endpoints=True)
        
        model_Block = ps.SINDy(feature_library = self.Lib, 
                               optimizer = self.opt, 
                               differentiation_method = fd_drop_endpoints)
        
        x_train = [eval(f'self.train[{item-1}]', globals(), {'self': self}) for item in xtrain_list]
        u_train = [eval(f'self.input_dot_data[{item-1}]', globals(), {'self': self}) for item in utrain_list]
        
        start = time.time()
        if self.type == 'B':
            model_Block.fit(x_train, u = u_train, t = self.sim_step, multiple_trajectories=True)
        
        if self.type == 'A':
            model_Block.fit(x_train, t = self.sim_step, x_dot = u_train, multiple_trajectories=True)
        end = time.time()

        model_Block.print()
        print(f"{end - start} cost in thie block\n")  # print the time cost  
        self.identified = model_Block


    def __Mperform(self, xtrain_list, utrain_list, method = 'SF'):
        """
        Multi_Perform to return model into the dictionary
        """
        
        fd_drop_endpoints = None
        
        if method == 'FD':
            fd_drop_endpoints = ps.FiniteDifference(drop_endpoints=True)
        
        elif method == 'SF':
            fd_drop_endpoints = ps.SmoothedFiniteDifference(drop_endpoints=True)
        
        model_Block = ps.SINDy(feature_library = self.Lib, 
                               optimizer = self.opt, 
                               differentiation_method = fd_drop_endpoints)
        # strange method to solve the problem ?
        x_train = [eval(f'self.train[{item-1}]', globals(), {'self': self}) for item in xtrain_list]
        u_train = [eval(f'self.input_dot_data[{item-1}]', globals(), {'self': self}) for item in utrain_list]
        
        if self.type == 'B':
            model_Block.fit(x_train, u = u_train, t = self.sim_step, multiple_trajectories=True)
        
        if self.type == 'A':
            model_Block.fit(x_train, t = self.sim_step, x_dot = u_train, multiple_trajectories=True)

        model_Block.print()
        print("\n")
        
        return model_Block
    

    def Multi_perform(self, train_series):
        """
        For coefficient analysis, obtain multi-models in batch
        with input train_series: [[1,2],[1,2,3],[2,3],[3,4]]
        """
        
        model_num = len(train_series)
        
        for train_num in range(model_num):  # into the dictionary
            # you should return a real object, instead of the address
            self.Midentified_dict[train_num] = copy.deepcopy((self.__Mperform(train_series[train_num], train_series[train_num], method = 'SF')))
                
