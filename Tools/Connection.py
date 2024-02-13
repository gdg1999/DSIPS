# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 11:16:37 2024

@author: Yuan Jing, Gregory_Guo
"""

"""
This is a tool for Connection of Subsystem
"""


import numpy as np
from scipy.linalg import *


class Connection():
    """
    The connection for the whole system
    """
    
    
    def __init__(self, sub_system, order):
        """
        Basic attributes
        """
        
        self.subSystem = sub_system
        self.Number_sub = len(self.subSystem)
        self.operation = order
        self.Operation_times = len(self.operation) - 1
        
        if self.Number_sub != self.Operation_times + 1:
            print("The operation times do not match the subsystem...")
        
        firstOne = self.sub_system[0]
        self.X = firstOne.X
        self.U = firstOne.U
        self.Y = firstOne.Y

        self.A = firstOne.A
        self.B = firstOne.B
        self.C = firstOne.C
        self.D = firstOne.D
        self.E = None  # A proper system is used
    

    def Auto_system(self):
        """
        sys->list is the prepared system you will contain
        order->list specifies the operation the system used
        eg. sys1, sys2, sys3, [1,2,3]
        final_sys = ((sys0 1 sys1) 2 sys2) 3 sys3;
        """
        
        for num in range(self.Operation_times):
            operation = self.operation[num]
            
            if operation == 1:    
                return self.feedback(self.subSystem[num+1])
            
            elif operation == 2:
                return self.series(self.subSystem[num+1])
            
            elif operation == 3:
                return self.shunt(self.subSystem[num+1])

            else:
                print("Invalid operation!")
                
                return None
        
        return (self.A, self.B, self.C, self.D, self.X, self.U, self.Y)


    def feedback(self, sys2):
        """
        The negative feedback operation

        Parameters
        ----------
        sys1 : system1
            system1 from Modal_analysis, forward
        sys2 : system2
            system2 from Modal_analysis, the feedback one

        Returns
        -------
        Tuple: the integrated system

        """
        
        A1 = self.A
        B1 = self.B
        C1 = self.C
        D1 = self.D
        X1 = self.X
        U1 = self.U
        Y1 = self.Y
        
        A2 = sys2.A
        B2 = sys2.B
        C2 = sys2.C
        D2 = sys2.D
        X2 = sys2.X
        U2 = sys2.U
        Y2 = sys2.Y

        # calculate the state equation after feedback connection
        I = np.ones([len(D1@D2),len(D1@D2)],int)
        N = np.linalg.inv(I + (D1@D2))
        
        self.A = np.block([[A1 - B1@D2@N@C1, -B1@(C2-D2@N@D1@C2)], [B2@N@C1, A2 - B2@N@D1@C2]])
        self.B = np.block([[B1 - B1@D2@N@D1], [B2@N@D1]])
        self.C = np.block([N@C1, -N@D1@C2])
        self.D = N@D1
        
        self.X = X1 + X2
        self.U = U1
        self.Y = Y1
        
        return (self.A, self.B, self.C, self.D, self.X, self.U, self.Y)
    
    
    def append(self, sys2):
        """
        The append operation

        Parameters
        ----------
        sys1 : system1, default: the original one

        sys2 : system2, default: the appended one

        Returns
        -------
        Tuple: the integrated system

        """
        
        A1 = self.A
        B1 = self.B
        C1 = self.C
        D1 = self.D
        X1 = self.X
        U1 = self.U
        Y1 = self.Y
        
        A2 = sys2.A
        B2 = sys2.B
        C2 = sys2.C
        D2 = sys2.D
        X2 = sys2.X
        U2 = sys2.U
        Y2 = sys2.Y
        
        self.U = U1 + U2
        self.Y = Y1 + Y2
        self.X = X1 + X2
    
        # constructing the state equation of the new system
        self.A = block_diag(A1, A2)
    
        self.B = block_diag(B1, B2)

        self.C = block_diag(C1, C2)

        self.D = block_diag(D1, D2)
    
        return (self.A, self.B, self.C, self.D, self.X, self.U, self.Y)
    
    
    def cross(self, sys2):
        pass
    
    
    def shunt(self, sys2):
        """
        Shunt operation

        Parameters
        ----------
        sys1 : TYPE
            DESCRIPTION.
        sys2 : TYPE
            DESCRIPTION.

        Returns
        -------
        Tuple: the integrated system

        """
        
        A1 = self.A
        B1 = self.B
        C1 = self.C
        D1 = self.D
        X1 = self.X
        U1 = self.U
        Y1 = self.Y
        
        A2 = sys2.A
        B2 = sys2.B
        C2 = sys2.C
        D2 = sys2.D
        X2 = sys2.X
        U2 = sys2.U
        Y2 = sys2.Y
        
        self.X = X1 + X2
        self.U = self.U
        self.Y = Y1  # its output should be the sum of y1 and y2 !
        
        self.A = block_diag(A1, A2)
    
        self.B = np.concatenate((B1, B2), axis=0)  # with col

        self.C = np.concatenate((C1, C2), axis=1)  # with row

        self.D = np.add(D1, D2)
        
        return (self.A, self.B, self.C, self.D, self.X, self.U, self.Y)
    
    
    def series(self, sys2):
        """
        Series operation

        Parameters
        ----------
        sys1 : system1 from Modal analysis, the first one

        sys2 : system2 from Modal analysis, the second one

        Returns
        -------
        Tuple: the integrated system

        """
        
        A1 = self.A
        B1 = self.B
        C1 = self.C
        D1 = self.D
        X1 = self.X
        U1 = self.U
        Y1 = self.Y
        
        A2 = sys2.A
        B2 = sys2.B
        C2 = sys2.C
        D2 = sys2.D
        X2 = sys2.X
        U2 = sys2.U
        Y2 = sys2.Y
        
        self.X = X1 + X2
        self.U = U1
        self.Y = Y2
        
        self.A = np.matmul(A2, A1)
        self.B = np.matmul(A2, B1) + B2
        self.C = np.matmul(C1, A2) + C2
        self.D = np.matmul(C1, B2) + D2 + D1
        
        return (self.A, self.B, self.C, self.D, self.X, self.U, self.Y)
    
