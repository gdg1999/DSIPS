# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 11:16:37 2024

@author: Yuan Jing
"""

"""
This is a tool for Participation Analysis
using python instead of matlab will be more convinent!

"""


import numpy as np


class PF_Analysis():
    """
    
    """



def Auto_system(order):
    
   pass



def feedback(A1, B1, C1, D1, A2, B2, C2, D2):
        # 计算反馈连接后的状态方程
        A = np.block([[A1, -B1@D2@C1],[B2@C1, A2]])
        B = np.block([[B1],[B2@D1]])
        C = np.block([D2@C1, C2])
        D = D2@D1
        
        return A, B, C, D

# 测试
A1 = np.array([[1, 2],[3, 4]])
B1 = np.array([[5],[6]])
C1 = np.array([[7, 8]])
D1 = np.array([[9]])
state_str1 = ['x11', 'x12']  # information related to this system1
input_str1 = ['u11']
output_str1 = ['y11']


A2 = np.array([[10, 11],[12, 13]])
B2 = np.array([[14],[15]])
C2 = np.array([[16, 17]])
D2 = np.array([[18]])
state_str1 = ['x21', 'x22']  # information related to this system2
input_str1 = ['u21']
output_str1 = ['y21']

A, B, C, D = feedback(A1, B1, C1, D1, A2, B2, C2, D2)

print("A = ", A)
print("B = ", B)
print("C = ", C)
print("D = ", D)

 
def connect_systems(A1, B1, C1, D1, A2, B2, ):
    
    sys1.A
    sys1.B
    sys1.X
    sys1.U
    
    
    
    return A, B, C, D, X, U, Y


def shunt(A1,B1,C1,D1,A2,B2,C2,D2):
    # 确定新系统的状态方程维度
    n1, m1 = B1.shape
    n2, m2 = B2.shape
    n = n1 + n2
    m = m1 + m2

    # 构建新系统的状态方程
    A = np.zeros((n, n))
    A[:n1, :n1] = A1
    A[n1:, n1:] = A2

    B = np.zeros((n, m))
    B[:n1, :m1] = B1
    B[n1:, m1:] = B2

    C = np.zeros((m, n))
    C[:m1, :n1] = C1
    C[m1:, n1:] = C2

    D = np.zeros((m, m))
    D[:m1, :m1] = D1
    D[m1:, m1:] = D2

    return A, B, C, D
# 测试
A1 = np.array([[1, 2], [3, 4]])
B1 = np.array([[5], [6]])
C1 = np.array([[7, 8]])
D1 = np.array([[9]])
A2 = np.array([[10]])
B2 = np.array([[11]])
C2 = np.array([[12]])
D2 = np.array([[13]])
A, B, C, D = shunt(A1, B1, C1, D1, A2, B2, C2, D2)
print("A =",A)
print("B =",B)
print("C =",C)
print("D =",D)
   


def series(A1,B1,C1,D1,A2,B2,C2,D2):
    A = np.matmul(A2, A1)
    B = np.matmul(A2, B1) + B2
    C = np.matmul(C1, A2) + C2
    D = np.matmul(C1, B2) + D2 + D1
    return A, B, C, D

# 测试
A1 = np.array([[1, 2], [3, 4]])
B1 = np.array([[5], [6]])
C1 = np.array([[7, 8]])
D1 = np.array([[9]])

A2 = np.array([[10, 11], [12, 13]])
B2 = np.array([[14], [15]])
C2 = np.array([[16, 17]])
D2 = np.array([[18]])

A, B, C, D = series(A1, B1, C1, D1, A2, B2, C2, D2)

print("A =", A)
print("B =", B)
print("C =", C)
print("D =", D)

def happy(A, B, C, D, X, U, Y):
    """
    intro
    """
    
    # Mode Shapes
    Mode
    
    # Participation Factors
    
    PF
    
    # Residues
    
    Res
    
    
    return Mode, PF, Res
    
