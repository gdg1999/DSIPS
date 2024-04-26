# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 09:23:19 2024

@author: Gregory_Guo
"""

"""
Used for Basic calculation of Semi-tensor
"""

import sympy as sp

def compute_jacobian(matrix, variables):
    """
    Compute the Jacobian matrix of a symbolic matrix with respect to the given variables.

    Parameters:
    - matrix: sympy.Matrix, the input symbolic matrix.
    - variables: list of sympy.Symbol, the variable vector.

    Returns:
    - sympy.Matrix, the Jacobian matrix.
    """
    # Differentiate with respect to the vector variables
    jacobian_matrix = sp.Matrix([[element.diff(variable) for variable in variables] for element in matrix])

    return jacobian_matrix

# Example usage
# Create symbolic variables
x, y, z = sp.symbols('x y z')

# Prompt the user to input a matrix
matrix_input = [(x**2, y*z, z**2*x),(x**2, y, z)]

# Parse the user input matrix
rows = len(matrix_input)
matrix_rows_elements = [[sp.sympify(element) for element in matrix_input(row)] for row in rows]

# Create a symbolic matrix
A = sp.Matrix(matrix_elements)

# Create a variable vector
variables = [x, y, z]

# Compute the Jacobian matrix
jacobian_matrix = compute_jacobian(A, variables)

# Output the result
print("dA/dv =")
print(jacobian_matrix)




