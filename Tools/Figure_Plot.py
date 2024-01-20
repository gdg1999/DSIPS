# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 20:22:09 2023

@author: Gregory_Guo
"""

"""
Plot figure for check
"""

import matplotlib.pyplot as plt
# plt.style.use( ['science',"grid","ieee"])


# this is for state blcok
def test_fig(Model,x_train,u_train,Data_length,dt,t_test):
    if (x_train.shape[1]!=1):  # more than one picture
        # Predict derivatives using the learned model
        x_dot_test_predicted = Model.predict(x_train[0:Data_length,:], u=u_train[0:Data_length,:])  
    
        # Compute derivatives with a finite difference method, for comparison
        x_dot_test_computed = Model.differentiate(x_train[0:Data_length,:], t=dt)
    
        fig, axs = plt.subplots(x_train.shape[1], 1, sharex=True, figsize=(18, 20))
        for i in range(x_train.shape[1]):
            axs[i].plot(t_test[0:Data_length], x_dot_test_computed[: , i],
                        'k', label='numerical derivative')
            axs[i].plot(t_test[0:Data_length], x_dot_test_predicted[: , i],
                        'r--', label='model prediction')
            axs[i].legend()
            axs[i].set(xlabel='t',ylabel='$\dot x_{}$'.format(i+1))
        fig.show()
    
    else:  # only one picture
        # Predict derivatives using the learned model
        x_dot_test_predicted = Model.predict(x_train[0:Data_length,:], u=u_train[0:Data_length,:])

        # Compute derivatives with a finite difference method, for comparison
        x_dot_test_computed = Model.differentiate(x_train[0:Data_length,:], t=dt)

        fig, axs = plt.subplots(x_train.shape[1], 1, sharex=True, figsize=(18, 10))
        axs.plot(t_test[0:Data_length], x_dot_test_computed[: , 0],
                    'k', label='numerical derivative')
        axs.plot(t_test[0:Data_length], x_dot_test_predicted[: , 0],
                    'r--', label='model prediction')
        axs.legend()
        axs.set(xlabel='t',ylabel='$\dot x_{}$'.format(1))
        fig.show()
      
        
# plot for the algebra block
def test_algebraic(Model, x_train, dot_x, Data_length,t_test):
    if (dot_x.shape[1]!=1):
        # Predict derivatives using the learned model
        x_dot_test_predicted = Model.predict(x_train[0:Data_length,:])  
    
        fig, axs = plt.subplots(dot_x.shape[1], 1, sharex=True, figsize=(18, 20))
        for i in range(dot_x.shape[1]):
            axs[i].plot(t_test[0:Data_length], dot_x[0:Data_length , i],
                        'k', label='numerical derivative')
            axs[i].plot(t_test[0:Data_length], x_dot_test_predicted[: , i],
                        'r--', label='model prediction')
            axs[i].legend()
            axs[i].set(xlabel='t',ylabel='$\dot x_{}$'.format(i+1))
        fig.show()
        
    else:
        # Predict derivatives using the learned model
        x_dot_test_predicted = Model.predict(x_train[0:Data_length,:])
        
        fig, axs = plt.subplots(dot_x.shape[1], 1, sharex=True, figsize=(18, 10))
        axs.plot(t_test[0:Data_length], dot_x[0:Data_length , 0],
                    'k', label='numerical derivative')
        axs.plot(t_test[0:Data_length], x_dot_test_predicted[: , 0],
                    'r--', label='model prediction')
        axs.legend()
        axs.set(xlabel='t',ylabel='$\dot x_{}$'.format(1))
        fig.show()

    
