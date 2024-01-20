# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 18:17:35 2023

@author: Gregory_Guo
"""

"""
This is a tool for model analysis
using python instead of matlab will be more convinent!

"""


from Configurations import *
from Tools import Controller_Optimization as CO
import sympy as sp
import control as ct
import matplotlib.pyplot as plt
# plt.style.use( ['science',"grid","ieee"])
import numpy as np
from scipy.linalg import schur, ordqz


class Analysis():
    """
    This is a tool box for system analysis
    Mainly for Time/Frequency domain analysis
    including relative controller design
    """
    
    def __init__(self, system, u, y):
        """
        States themselves are outputs
        """
        
        self.system = system  # analyzed system
        self.input = u  # system input, in list way
        self.output = y  # system output
        
        self.states_dict = dict()
        self.algebra_dict = dict()
        
        self.X = None  # the states of the system, in symbol way
        self.U = None  # system input
        self.Y = None  # system output
        
        self.A = None
        self.B = None
        self.C = None
        self.D = None
        self.state_space = None  # the state space of identified system
    
    
    def R(self, my_dict, search_string):
        keys = list(my_dict.keys())
        if search_string in keys:
            return keys.index(search_string)
        return None
    
    
    def Jacobian_mat(self):
        """
        This function will return the jocobian linearized matrix of your
        identifie system
        
        and the order of your system states and inputs/output variables.
        
        if the outputs are not designed, then all of the algebraic variables will be represented
        """
        
        Block_num = self.system.Block_num
        Algebra_num = self.system.Algebra_num
        REBlock_eq = []  # simplified differential system
        RE_ABlock_eq = []  # simplified algebraic system
        XBlock_eq = []  # the original identifed system, differential
        ABlock_eq = []  # the original identified system, algebra
        Xstates = []  # refresh, used for storing the total states
        
        
        for num in range(0, Block_num + Algebra_num):  # for each block
            
            # for block type A, orignial
            if  eval(f"Type{num+1}") == 'A':
                State = sp.symbols(eval(f"dot{num+1}_x"))  # here better to change the order
                Input = sp.symbols(eval(f"states{num+1}")) 
                
                for item in eval(f"dot{num+1}_x"):
                    self.algebra_dict[item] = sp.symbols(item)  # store all of the symbol in dict
        
                # state is represented by input 
                print(f"the block num{num+1} includes {State} and {Input}") # print all of the states
                
                Astate = [0]*len(eval(f"dot{num+1}_x"))  # the state equation in the block          
                for row in range(len(eval(f"dot{num+1}_x"))):
                    if eval(f"bias{num+1}") == False:
                        for col, pu in enumerate(Input):
                            # print(row, col, pu)
                            Astate[row] = Astate[row] + self.system.Blocks[num].identified.coefficients()[row, col]*pu
                    if eval(f"bias{num+1}") == True:
                        for col, pu in enumerate([sp.symbols('1')] + Input):
                            # print(row, col, pu)
                            Astate[row] = Astate[row] + self.system.Blocks[num].identified.coefficients()[row, col]*pu
                            
                ABlock_eq.append(Astate)  # append to the total equation list
        
        
            # for block type B, still in the loop
            if eval(f"Type{num+1}") == 'B':
                State = sp.symbols(eval(f"states{num+1}"))  # the state of B
                Input = sp.symbols(eval(f"inputs{num+1}"))  # the input of B
                Xstates.append(State)  # add state to total state      
                
                for item in eval(f"states{num+1}"):
                    self.states_dict[item] = sp.symbols(item)  # just for check

                # state is represented by input 
                print(f"the block num{num+1} includes {State} and {Input}") # print all of the states
                
                Dstate = [0]*len(eval(f"states{num+1}"))  # the state equation in the block          
                for row in range(len(eval(f"states{num+1}"))):
                    if eval(f"bias{num+1}") == False:
                        for col, pu in enumerate(State + Input):
                            # print(row, col, pu)
                            Dstate[row] = Dstate[row] + self.system.Blocks[num].identified.coefficients()[row, col]*pu
                    if eval(f"bias{num+1}") == True:
                        for col, pu in enumerate([sp.symbols('1')] + State + Input):
                            # print(row, col, pu)
                            Dstate[row] = Dstate[row] + self.system.Blocks[num].identified.coefficients()[row, col]*pu
                    
                XBlock_eq.append(Dstate)  # list in the list, including all of the Eq in Block B
        
        self.flattened_ABlock_eq = [element for sublist in ABlock_eq for element in sublist]         
        self.flattened_XBlock_eq = [element for sublist in XBlock_eq for element in sublist]  # change to one list


        # regenerate Matrix C, another new loop
        for num in range(Block_num, Block_num + Algebra_num):  # for each B block
        
            State = sp.symbols(eval(f"dot{num+1}_x"))  # here better to change the order
            Input = sp.symbols(eval(f"states{num+1}")) # state is represented by inputs
            
            RE_Astate = [0]*len(eval(f"dot{num+1}_x"))  # the state equation in the block   

            for row in range(len(eval(f"dot{num+1}_x"))):
                if eval(f"bias{num+1}") == False:
                    for col, pu in enumerate(Input):
                        if str(pu) in self.algebra_dict:  # clean the repetition
                            pu = self.flattened_ABlock_eq[self.R(self.algebra_dict, str(pu))]  # REPLACEMENT!
                            RE_Astate[row] = RE_Astate[row] + self.system.Blocks[num].identified.coefficients()[row, col]*pu
                        else:
                            RE_Astate[row] = RE_Astate[row] + self.system.Blocks[num].identified.coefficients()[row, col]*pu
                if eval(f"bias{num+1}") == True:
                    for col, pu in enumerate([sp.symbols('1')] + Input):  # don't forget "1"
                        if str(pu) in self.algebra_dict:
                            pu = self.flattened_ABlock_eq[self.R(self.algebra_dict, str(pu))]  # REPLACEMENT!
                            RE_Astate[row] = RE_Astate[row] + self.system.Blocks[num].identified.coefficients()[row, col]*pu
                        else:
                            RE_Astate[row] = RE_Astate[row] + self.system.Blocks[num].identified.coefficients()[row, col]*pu
                        
            RE_ABlock_eq.append(RE_Astate)   

        self.flattened_RABlock_eq = [element for sublist in RE_ABlock_eq for element in sublist]  # update the eq_list
        

        # regenerate Matrix A
        for num in range(0, Block_num):  # for each B block
        
            State = sp.symbols(eval(f"states{num+1}"))  # the state of B
            Input = sp.symbols(eval(f"inputs{num+1}"))  # the input of B
            
            RE_Dstate = [0]*len(eval(f"states{num+1}"))  # the state equation in the block   
            
            for row in range(len(eval(f"states{num+1}"))):
                
                if eval(f"bias{num+1}") == False:
                    for col, pu in enumerate(State + Input):
                        if str(pu) in self.algebra_dict:
                            # print(num, str(pu))
                            pu = self.flattened_RABlock_eq[self.R(self.algebra_dict, str(pu))]  # REPLACEMENT!
                            RE_Dstate[row] = RE_Dstate[row] + self.system.Blocks[num].identified.coefficients()[row, col]*pu
                        else:
                            RE_Dstate[row] = RE_Dstate[row] + self.system.Blocks[num].identified.coefficients()[row, col]*pu
                if eval(f"bias{num+1}") == True:
                    for col, pu in enumerate([sp.symbols('1')] + State + Input):
                        if str(pu) in self.algebra_dict:
                            # print(num, str(pu))
                            pu = self.flattened_RABlock_eq[self.R(self.algebra_dict, str(pu))]
                            RE_Dstate[row] = RE_Dstate[row] + self.system.Blocks[num].identified.coefficients()[row, col]*pu
                        else:
                            RE_Dstate[row] = RE_Dstate[row] + self.system.Blocks[num].identified.coefficients()[row, col]*pu
                
            REBlock_eq.append(RE_Dstate)  # list in the list, including all of the Eq in Block B

        self.flattened_RBlock_eq = [element for sublist in REBlock_eq for element in sublist]  # change to one list


        # if you wanna assign certain output
        Output_Y = []
        for item in self.output:
            Output_Y.append(self.flattened_RABlock_eq[self.R(self.algebra_dict, item)])
        self.OutputY = sp.Matrix(Output_Y) 
    
        self.Afuncs = sp.Matrix(self.flattened_ABlock_eq)  # algebraic function    
        self.Xfuncs = sp.Matrix(self.flattened_XBlock_eq)  # state function
        self.RXfuncs = sp.Matrix(self.flattened_RBlock_eq)  # state function with replacement
        self.RAfuncs = sp.Matrix(self.flattened_RABlock_eq)  # state function with replacement
        
        self.X = [element for sublist in Xstates for element in sublist]  # state symbol list
        self.U = sp.symbols(self.input)  # input string list to symbol list
        
        self.A = self.RXfuncs.jacobian(self.X)
        self.B = self.RXfuncs.jacobian(self.U)
        
        if len(self.output) ==0:
            self.C = self.RAfuncs.jacobian(self.X)
            self.D = self.RAfuncs.jacobian(self.U)
            self.Y = self.algebra_dict
        else:
            self.C = self.OutputY.jacobian(self.X)
            self.D = self.OutputY.jacobian(self.U)
            self.Y = sp.symbols(self.output)
  
        return [(self.A,self.B,self.C,self.D), (self.X, self.U, self.Y)]


    def Plot_poles(self, poles):
        """
        Using the data from Damp_analysis()
        """
        
        real_parts = np.real(poles)
        imaginary_parts = np.imag(poles)
        
        plt.scatter(real_parts, imaginary_parts, marker='x', color='red')
        plt.xlabel('Real Part')
        plt.ylabel('Imaginary Part')
        plt.title('Scatter Plot of Poles')
        plt.grid(True)
        
        plt.show()
        
    
    def Plot_bode(self, input_output):
        """
        input_output = [0,0] --> a list
        """
        
        output_index = input_output[0]
        input_index = input_output[1]
        
        Data = ct.bode_plot(self.state_space[input_index, output_index], 
                            dB = True, 
                            omega_limits = [1e-2,1e2])
        
        return Data
    
    
    def Plot_step(self, output_index):
        """
        output_index = 1 --> an integral
        """
        
        step_data = ct.step_response(self.state_space)
        
        plt.plot(step_data[0],step_data[2][output_index,:])
        
        return step_data


    def Damp_analysis(self):
        """
        This is damp analysis for the linearized system,
        return the oscillation frequency and damp value
        also the zplot of the system.
        """
        
        self.state_space = ct.ss(self.A, self.B, self.C, self.D)
        (wn, zeta, poles) = self.state_space.damp()
        
        self.Plot_poles(poles)
        
        return wn/(2*np.pi), zeta, poles
    
    
    def Plot_range_poles(self, poles, re_range, im_range):
        """
        Filter the poles with specific real part range
        re_range = [min, max]
        poles -> array
        """
        
        # Create an array of complex numbers
        complex_numbers = poles

        # Define the range for the real part that you want to keep
        min_real = re_range[0]  # Minimum real part
        max_real = re_range[1]  # Maximum real part
        
        min_im = im_range[0]  # Minimum real part
        max_im = im_range[1]  # Maximum real part

        # Split complex numbers into real and imaginary parts
        real_parts = np.real(complex_numbers)
        imaginary_parts = np.imag(complex_numbers)
        
        # Create a mask to filter the points within the specified range
        mask_real = (real_parts >= min_real) & (real_parts <= max_real) & (imaginary_parts >= min_im) & (imaginary_parts <= max_im)
        
        # Filter the complex numbers and their corresponding real and imaginary parts
        filtered_complex_numbers = complex_numbers[mask_real]
        filtered_real_parts = real_parts[mask_real]
        filtered_imaginary_parts = imaginary_parts[mask_real]
        
        # Create the scatter plot with the filtered points
        plt.scatter(filtered_real_parts, 
                    filtered_imaginary_parts, 
                    label='Poles', 
                    color='b', 
                    marker='x', 
                    s = 25)

        # Add labels and title
        plt.xlabel('Damping',fontsize=9)
        plt.ylabel('Frequency (Hz)',fontsize=9)
        # plt.title('Scatter Plot of Filtered Complex Numbers')
        plt.grid(True)
        plt.legend(fontsize=9)
        plt.tick_params('y', labelsize=9)
        plt.tick_params('x', labelsize=9)

        # Show the plot
        plt.show()
        
        return filtered_complex_numbers
        
        
    def __ctrb_obsv(self):
        """
        check the ability
        """
        
        Controllabilty_matrix = ct.ctrb(self.A, self.B)
        Observability_matrix = ct.obsv(self.A, self.C)
        ability_index = [None, None]
        
        rank_controllable = np.linalg.matrix_rank(Controllabilty_matrix)
        if rank_controllable == self.A.shape[0]:
            print("The system is controllable")
            ability_index[0] = True
        else:
            print(f"The rank of control Matrix is {rank_controllable}")
            ability_index[0] = False
        
        rank_observable = np.linalg.matrix_rank(Observability_matrix)
        if rank_observable == self.A.shape[0]:
            print("The system is observable")
            ability_index[1] = True
        else:
            print(f"The rank of observe Matrix is {rank_observable}")
            ability_index[1] = False
        
        return ability_index
    
    
    def Controller_design(self, constraint_H):
        """
        Here we use the basic pole replacement controller.
        with the controller structure constrained
        
        here is the algorithm:
            1.return the state space of the system
            2.calcualte the controllability and observability matrix
            3.check the ability
            4.apply the feedback from outputs to states
            5.feedback matrix constraint
            6.poles placement or optimal control
            7.retrun the feedback matrix
        """
        
        
        Matrix, dim = CO.Pre_Para(self.A, self.C, constraint_H)
        
        pso = CO.PSO(Matrix, self.C, constraint_H, dim, 30, 10, 30, 60, -3, C1=1.2, C2=1.2, W=0.5)
        fit_var_list, best_pos = pso.update_ndim()
        print("最优位置:" + str(best_pos))
        print("最优解:" + str(fit_var_list[-1]))
        plt.plot(range(len(fit_var_list)), fit_var_list, alpha=0.5)

        
        
        
        
        
        
        
