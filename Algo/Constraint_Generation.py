# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 16:51:45 2023

@author: Gregory_Guo
"""

import pysindy as ps
import numpy as np


"""
This file generates constraints from Configuration files
Only equation files here, and suitable for linerized representations.
"""


class block_constraint(object):
    """
    The constraint class, one object for each block(Model)
    with five inputs illustrated below
    """
    
    def __init__(self, states, inputs, constraints_assign, constraints_combi, Lib, Type, optConfig = [1e-8, 0, 'l1', 5000]):
        """
        constraints_assign = [('state', 'feature', value), (...), (...)]
        means: feature coefficient in state equation == value
        
        constraints_combi = [('state1', 'feature1', 'state2', 'feature2', value), (...), (...)]
        means: feature1 coefficient in state1 + feature2 coefficient in state2 == value
        
        optConfig = [tol, threshold, thresholder, max_iter]
        """
        
        self.constraints_assign = constraints_assign
        self.constraints_combi = constraints_combi
        self.Lib = Lib
        self.Type = Type
        self.optConfig = optConfig

        if self.Type == 'B':  # only two kinds of blocks here, the total feature numbers are different
            self.states = states  # wait to be represented
            self.inputs = inputs  # which represente the state
            self.features = states + inputs
            if self.Lib[2] == 1:
                self.features = ['1'] + self.features  # for linearized system, the core features are the sum
            self.n_features = len(self.states) + len(self.inputs) + 1*self.Lib[2]

        else:
            self.states = inputs  # wait to be represented
            self.inputs = states  # which represente the state
            self.n_features = len(self.inputs) + 1*self.Lib[2]  # self.inputs are the features
            self.features = states  # for linearized system, the core features are the sum
            if self.Lib[2] == 1:
                self.features = ['1'] + self.features  # for linearized system, the core features are the sum

        self.n_targets = len(self.states)
        self.constraint_num = len(self.constraints_assign) + len(self.constraints_combi)
        # the constraint numbers is equal with the row of the constraint matrix


    def constraint_matrix(self):
        """
        Generate the constraint matrix, equation constraint only
        and no constraints for the bias!
        """
        
        self.constraint_rhs = np.zeros((self.constraint_num))
        self.constraint_lhs = np.zeros((self.constraint_num, self.n_targets * self.n_features))
        
        if self.constraints_assign == [] and self.constraints_combi == []:
            return True  # if we do not have constraint, leave it
            
        for constraint_num in range(self.constraint_num):  # process with the number of constraint_num
            if constraint_num < len(self.constraints_assign):  # the assign type constraint
                self.constraint_rhs[constraint_num] = self.constraints_assign[constraint_num][2]
                # assign the given value to the right side of the matrix
                # one group
                eq_name = [i for i, x in enumerate(self.states) if x == self.constraints_assign[constraint_num][0]]  # the equation
                feature_name = [i for i, x in enumerate(self.features) if x == self.constraints_assign[constraint_num][1]]  # the feature
                # follow the name, instead of the order
                self.constraint_lhs[constraint_num, self.n_features*eq_name[0] + feature_name[0]] = 1
                # assign the value unit to corresponding features
                
            else:  # the combination type constraint
                self.constraint_rhs[constraint_num] = self.constraints_combi[constraint_num-len(self.constraints_assign)][4]
                # two groups
                eq_name1 = [i for i, x in enumerate(self.states) if x == self.constraints_combi[constraint_num-len(self.constraints_assign)][0]]
                feature_name1 = [i for i, x in enumerate(self.features) if x == self.constraints_combi[constraint_num-len(self.constraints_assign)][1]]
                
                eq_name2 = [i for i, x in enumerate(self.states) if x == self.constraints_combi[constraint_num-len(self.constraints_assign)][2]]
                feature_name2 = [i for i, x in enumerate(self.features) if x == self.constraints_combi[constraint_num-len(self.constraints_assign)][3]]
                
                self.constraint_lhs[constraint_num, self.n_features*eq_name1[0] + feature_name1[0]] = 1
                self.constraint_lhs[constraint_num, self.n_features*eq_name2[0] + feature_name2[0]] = 1
                
        return False
        
    
    def optimizer_config(self):
        """
        Return opt method
        """
        
        if self.constraint_matrix():  # No constraint
            
            self.opt = ps.ConstrainedSR3(tol = self.optConfig[0],
                                         threshold = self.optConfig[1],
                                         thresholder = self.optConfig[2],
                                         max_iter = self.optConfig[3])
        
        else:  # with constraint
            
            self.opt = ps.ConstrainedSR3(constraint_rhs = self.constraint_rhs,
                                         constraint_lhs = self.constraint_lhs,
                                         tol = self.optConfig[0],
                                         threshold = self.optConfig[1],
                                         thresholder = self.optConfig[2],
                                         max_iter = self.optConfig[3])
        
        return self.opt


class nonlinear_constraint(block_constraint):
    """
    this is for nonlinear constraint!
    """
    
    def __init__(self, states, feature_name_list, constraints_assign, constraints_combi, optConfig = [1e-8, 0, 'l1', 5000]):
        self.states = states
        self.n_targets = len(states)
        self.fea_list = feature_name_list  # obtain the feature list to access the order of constraint element
        self.n_features = len(feature_name_list)
        self.constraints_assign = constraints_assign
        self.constraints_combi = constraints_combi
        self.optConfig = optConfig
        self.constraint_num = len(self.constraints_assign) + len(self.constraints_combi)
    
    
    def constraint_matrix(self):
        self.constraint_rhs = np.zeros((self.constraint_num))
        self.constraint_lhs = np.zeros((self.constraint_num, self.n_targets * self.n_features))
        
        if self.constraints_assign == [] and self.constraints_combi == []:
            return True  # if we do not have constraint, leave it
            
        for constraint_num in range(self.constraint_num):  # process with the number of constraint_num
            if constraint_num < len(self.constraints_assign):  # the assign type constraint
                self.constraint_rhs[constraint_num] = self.constraints_assign[constraint_num][2]
                # assign the given value to the right side of the matrix
                # one group
                eq_name = [i for i, x in enumerate(self.states) if x == self.constraints_assign[constraint_num][0]]  # the equation
                feature_name = [i for i, x in enumerate(self.fea_list) if x == self.constraints_assign[constraint_num][1]]  # the feature
                
                if feature_name == []:
                    print("Check your feature list:\n")
                    print(self.fea_list)
                    print("\n")
                
                # follow the name, instead of the order
                self.constraint_lhs[constraint_num, self.n_features*eq_name[0] + feature_name[0]] = 1
                # assign the value unit to corresponding features
                
            else:  # the combination type constraint
                self.constraint_rhs[constraint_num] = self.constraints_combi[constraint_num-len(self.constraints_assign)][4]
                # two groups
                eq_name1 = [i for i, x in enumerate(self.states) if x == self.constraints_combi[constraint_num-len(self.constraints_assign)][0]]
                feature_name1 = [i for i, x in enumerate(self.fea_list) if x == self.constraints_combi[constraint_num-len(self.constraints_assign)][1]]
                
                eq_name2 = [i for i, x in enumerate(self.states) if x == self.constraints_combi[constraint_num-len(self.constraints_assign)][2]]
                feature_name2 = [i for i, x in enumerate(self.fea_list) if x == self.constraints_combi[constraint_num-len(self.constraints_assign)][3]]
                
                if feature_name1 == [] or feature_name2 == []:
                    print("Check your feature list:\n")
                    print(self.fea_list)
                    print("\n")
                
                self.constraint_lhs[constraint_num, self.n_features*eq_name1[0] + feature_name1[0]] = 1
                self.constraint_lhs[constraint_num, self.n_features*eq_name2[0] + feature_name2[0]] = 1
                
        return False
    
    
    