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
import pandas as pd


class PF_Analysis():
    def __init__(self, A, X):
        """
        Obtain initial states
        """   
        self.A = A
        self.X = X
    
        
    def calculate_eigenvalues(self):
        eigenvalues, _ = np.linalg.eig(self.A)
        print("特征值矩阵:")
        print(eigenvalues)
        return eigenvalues
    
    
    def eigen_vector_mode(self):
        """
        Obtain the right/left eigenvector
        """
        _, eigenvectors = np.linalg.eig(self.A)
        # Output right eigenvectors matrix
        print("\n右特征向量矩阵:")
        print(eigenvectors)
        # Calculate left eigenvectors matrix
        left_eigenvectors = np.linalg.inv(eigenvectors)
        # Output left eigenvectors matrix
        print("\n左特征向量矩阵:")
        print(left_eigenvectors)  
        return eigenvectors
    
    
    def compute_observability(self,eigenvectors):
         # constructing observability matrix
         D = np.transpose(eigenvectors)
         for i in range(len(eigenvalues)):
             D[i] = D[i] * np.exp(eigenvalues[i])    
         # calculate the rank of a natrix
         rank = np.linalg.matrix_rank(D)
         # judging observability
         if rank == len(eigenvalues):
             print("The system is observable.")
         else:
             print("The system is not observable.")
         return D
     
        
    def controllability(self,eigenvectors,eigenvalues):
        # Transpose the eigenvalue vector matrix
        eigenvectors_T = np.transpose(eigenvectors)
        # Calculate the controllability matrix C
        C = np.matmul(np.matmul(eigenvectors_T, self.A), eigenvectors)
        # Extracting the Real Part of eigenvalues
        real_part = np.real(eigenvalues)
        # Check if the real parts of all eigenvalues are not 0
        if np.any(real_part == 0):
            print("System not completely controllable.")
        # Check the rank of controllability matrix C
        rank_C = np.linalg.matrix_rank(C)
        # Obtain the dimension of matrix A
        n = self.A.shape[0]      
        # Determine if the system is controllable
        if rank_C == n:
            print("System is completely controllable.")
        else:
            print("System is not completely controllable.")
        return C
    
    
    def PF(self, eigenvectors):
        result = np.zeros((len(self.A), len(self.A)))
        for i in range(len(self.A)):
            for j in range(len(self.A)):  
                result[i][j] = abs(np.dot(self.A[:, i], eigenvectors[:, j]))
    
        
        result_normalized = result / result.sum(axis=0)

        sorted_result = np.sort(-result_normalized,axis=0)
        sorted_result=np.abs(sorted_result)
        print(result_normalized)
        print(sorted_result)
        return sorted_result
      
    def Residue(self,D,C):
         """
         Calculate the residue

         Returns
         -------
         Res : TYPE
             DESCRIPTION.

         """
         Res=[]
         # Obtain the dimension of matrix A
         n = self.A.shape[0]        
         for k in range(n):
             Res.append(D*C)
         for value in range:
             print(value)
         return Res
            
     
    def toExcel(self, eigenvalues, eigenvectors,sorted_result, filename):
        """
        Write the results into excel

        Returns
        -------
        None.
        """

        # Create an Excel writer object
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')

        # Write the eigenvalue matrix into a worksheet in an Excel file
        df_eigenvalues = pd.DataFrame({'特征值': eigenvalues})
        df_eigenvalues.to_excel(writer, index=False, sheet_name='特征值矩阵')

        # Write the right eigenvector matrix into a worksheet in an Excel file
        df_eigenvectors = pd.DataFrame(eigenvectors)
        df_eigenvectors.to_excel(writer, index=False, sheet_name='右特征向量矩阵')

        # Calculate and sort the participation factor matrix for each state variable
        # Sort indices in descending order of participation factors
        

        # Create initial participation factor dataframe
        df_participation = pd.DataFrame(sorted_result,index=['mode'+str(i+1)for i in range(len(sorted_result))])

        # Replace the column names with state1, state2, ...
        df_participation.columns = ['state' + str(i + 1) for i in range(len(df_participation.columns))]
        frequencies= np.sqrt(np.abs(eigenvalues))/(2*np.pi)
        damping_ratios = -np.real(eigenvalues) / np.abs(eigenvalues)
        df_participation['振荡频率']=frequencies
        df_participation['阻尼']=damping_ratios
 
        # Save the participation factor matrix into a worksheet in an Excel file
        df_participation.to_excel(writer, index=True, sheet_name='参与因子归一化矩阵')

        # Save the Excel file
        writer.close()

        
# Create objects to perform modal analysis
A = np.array([[0, 2], [-4, -6]])
X = ['state1','state2']
pf_analysis = PF_Analysis(A,X)
eigenvalues = pf_analysis.calculate_eigenvalues()
eigenvectors = pf_analysis.eigen_vector_mode()

sorted_result=pf_analysis.PF(eigenvectors)
pf_analysis.toExcel(eigenvalues,eigenvectors,sorted_result,'output.xlsx')
D=pf_analysis.compute_observability(eigenvectors)
C=pf_analysis.controllability(eigenvectors,eigenvalues)







