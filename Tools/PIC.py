# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 08:38:54 2023

@author: Gregory_Guo
"""

import numpy as np
import matplotlib.pyplot as plt
# plt.style.use( ['science',"grid","ieee"])


color_dict = {
    "classic":[(205/255,92/255,92/255),(60/255,179/255,113/255),(65/255,105/255,225/255)],
    "千里江山":[(117/255,159/255,107/255),(189/255,144/255,43/255),(70/255,141/255,165/255)],
    "琉璃":[(145/255,187/255,221/255),(33/255,65/255,107/255),(172/255,75/255,71/255)],
    "天青":[(70/255,128/255,139/255),(143/255,209/255,225/255),(194/255,225/255,230/255)],
    "玄泽":[(143/255,110/255,103/255),(220/255,169/255,104/255),(56/255,5/255,9/255)]
    }


def generate_subplots(rows, cols, subplot_data, Length):
    xmin = 0.5*Length*1e-5
    xmax = Length*1e-5
    fig, axs = plt.subplots(rows, cols, figsize=(20, 8), sharex=True, layout='constrained')
    for ax, Data in zip(axs.flat, subplot_data):
        x, y, title, color, linestyle, linewidth, xlabel, ylabel = Data
        # ax.set_title(title)
        ax.set_ylabel(ylabel,fontsize=25)
        ax.tick_params('y', labelsize=23)
        ax.tick_params('x', labelsize=23)
        ax.ticklabel_format(style='sci', scilimits=(-1,2),axis='y')
        ax.yaxis.get_offset_text().set_fontsize(23)
        # ax.set_xlabel("t(s)",fontsize=22)
        # if you wanna dash line to seperate the training data and the test data, use this:
        # ax.axvspan(xmin=xmin,xmax=xmax,facecolor=color_dict["琉璃"][0],alpha=0.2)
        # ax.axvline(x=xmin, ls='-.')
        ax.set_xlim(0, xmax)
        label_ = ['Real','Identified']
        for len_y in range(len(y)):
            ax.plot(x, y[len_y],
                    color=color[len_y],
                    linestyle=linestyle[len_y],
                    linewidth=linewidth[len_y],
                    label=label_[len_y]
                    )
        # if you wanna legend at a specific location, use this:
        # axs[1,2].legend(fontsize=25, frameon=False)


        fig.supxlabel('Time(s)',fontsize=25)
        fig.tight_layout()
        # plt.savefig ( "test.svg", format = "svg")
        # fig.supylabel('XLAgg',fontsize=20)

    
    
    
    