# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 09:16:44 2023

@author: Gregory_Guo
"""

"""
Use PSO to solve the eigenvalues of the matrix
"""

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
# plt.style.use( ['science',"grid","ieee"])

real = sp.symbols('x')
imag = sp.symbols('y')
# A = sp.Matrix([[10, 2.5, 4, 9, 5], [2.5, 10, 3, 7, 10], [0, 1, 6, 2, 6], [0, 0, 2, 6, 7], [10, 7, 2, 4, 7]])
A = sp.Matrix([[-3, 1, -1], [-7, 5, -1], [-6, 6, -2]])
n = A.shape[0]
I = np.eye(n)
B = A - (real + imag * 1j) * I
determinant = B.det()

def fit_fun(x):  # 适应函数

    value = complex(determinant.subs({real: x[0][0], imag: x[0][1]}))
    
    return np.abs(value)


class Particle(object):
    # 初始化
    def __init__(self, x_max, max_vel, dim):
        self.__pos = np.random.uniform(-x_max, x_max, (1, dim))  # 粒子的位置
        self.__vel = np.random.uniform(-max_vel, max_vel, (1, dim))  # 粒子的速度
        self.__bestPos = np.zeros((1, dim))  # 粒子最好的位置
        self.__fitnessValue = fit_fun(self.__pos)  # 适应度函数值

    def set_pos(self, value):
        self.__pos = value

    def get_pos(self):
        return self.__pos

    def set_best_pos(self, value):
        self.__bestPos = value

    def get_best_pos(self):
        return self.__bestPos

    def set_vel(self, value):
        self.__vel = value

    def get_vel(self):
        return self.__vel

    def set_fitness_value(self, value):
        self.__fitnessValue = value

    def get_fitness_value(self):
        return self.__fitnessValue


class PSO(object):
    def __init__(self, dim, size, iter_num, x_max, max_vel, tol, best_fitness_value=float('Inf'), C1=2, C2=2, W=1):
        self.C1 = C1
        self.C2 = C2
        self.W = W
        self.dim = dim  # 粒子的维度
        self.size = size  # 粒子个数
        self.iter_num = iter_num  # 迭代次数
        self.x_max = x_max
        self.max_vel = max_vel  # 粒子最大速度
        self.tol = tol  # 截止条件
        self.best_fitness_value = best_fitness_value
        self.best_position = np.zeros((1, dim))  # 种群最优位置
        self.fitness_val_list = []  # 每次迭代最优适应值

        # 对种群进行初始化
        self.Particle_list = [Particle(self.x_max, self.max_vel, self.dim) for i in range(self.size)]

    def set_bestFitnessValue(self, value):
        self.best_fitness_value = value

    def get_bestFitnessValue(self):
        return self.best_fitness_value

    def set_bestPosition(self, value):
        self.best_position = value

    def get_bestPosition(self):
        return self.best_position

    # 更新速度
    def update_vel(self, part):
        vel_value = self.W * part.get_vel() + self.C1 * np.random.rand() * (part.get_best_pos() - part.get_pos()) \
                    + self.C2 * np.random.rand() * (self.get_bestPosition() - part.get_pos())
        vel_value[vel_value > self.max_vel] = self.max_vel
        vel_value[vel_value < -self.max_vel] = -self.max_vel
        part.set_vel(vel_value)

    # 更新位置
    def update_pos(self, part):
        if part.get_fitness_value() != self.get_bestFitnessValue():
            pos_value = part.get_pos() + part.get_vel()
            print(True)
        else:
            pos_value = 1.5*part.get_pos()
            print(False)
        part.set_pos(pos_value)
        value = fit_fun(part.get_pos())
        if value < part.get_fitness_value():
            part.set_fitness_value(value)
            part.set_best_pos(pos_value)
        if value < self.get_bestFitnessValue():
            self.set_bestFitnessValue(value)
            self.set_bestPosition(pos_value)

    def update_ndim(self):

        for i in range(self.iter_num):
            for part in self.Particle_list:
                self.update_vel(part)  # 更新速度
                self.update_pos(part)  # 更新位置
            self.fitness_val_list.append(self.get_bestFitnessValue())  # 每次迭代完把当前的最优适应度存到列表
            print('第{}次最佳适应值为{}'.format(i, self.get_bestFitnessValue()))
            if self.get_bestFitnessValue() < self.tol:
                break

        return self.fitness_val_list, self.get_bestPosition()


if __name__ == '__main__':
    
    pso = PSO(2, 60, 100, 30, 60, 1e-5, C1=1.2, C2=1.2, W=0.5)
    fit_var_list, best_pos = pso.update_ndim()
    print("最优位置:" + str(best_pos))
    print("最优解:" + str(fit_var_list[-1]))
    plt.plot(range(len(fit_var_list)), fit_var_list, alpha=0.5)

