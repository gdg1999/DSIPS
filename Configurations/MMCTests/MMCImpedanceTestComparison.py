# -*- coding: utf-8 -*-
"""
Created on Mon May  6 08:56:15 2024

@author: Gregory_Guo
"""

import pysindy as ps
from scipy.io import loadmat
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use( ['science',"grid","ieee"])

color_dict = {
    "classic":[(205/255,92/255,92/255),(60/255,179/255,113/255),(65/255,105/255,225/255)],
    "千里江山":[(117/255,159/255,107/255),(189/255,144/255,43/255),(70/255,141/255,165/255)],
    "琉璃":[(145/255,187/255,221/255),(33/255,65/255,107/255),(172/255,75/255,71/255)],
    "天青":[(70/255,128/255,139/255),(143/255,209/255,225/255),(194/255,225/255,230/255)],
    "玄泽":[(143/255,110/255,103/255),(220/255,169/255,104/255),(56/255,5/255,9/255)]
    }



sim_step = 1       # simulation max step size
dt = sim_step





MMC_Mag = r"G:\project\MMC_HVDC\MMC_Positive_data\Mag_scan_Yap_MMC.mat"
MMC_Mag_data = loadmat(MMC_Mag)

f_can_MMC = r"G:\project\MMC_HVDC\MMC_Positive_data\f_scan_MMC.mat"
f_MMC = loadmat(f_can_MMC)

MMC_Mag_data = MMC_Mag_data['Mag_scan_Yap']
f_data_MMC = f_MMC['f_scan']

plt.plot(np.squeeze(f_data_MMC)[1:117], np.squeeze(MMC_Mag_data)[1:117], label='Real')
Length = len(f_data_MMC)

# sindy_library1 = ps.PolynomialLibrary(degree=10, include_bias=True)
# model_Block1 = ps.SINDy(feature_library = sindy_library1)
# model_Block1.fit(np.squeeze(MMC_Mag_data), t = dt)

# predicted = model_Block1.predict(np.squeeze(MMC_Mag_data).reshape(-1))

x1, y1 = 400, -9
x2, y2 = 0, -29

plt.plot(np.squeeze(f_data_MMC)[1:117], np.squeeze(MMC_Mag_data)[1:117], label='Identification')

plt.plot([x1, x2], [y1, y2], color='b', linestyle='-.', label='Grid Impedance')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Frequency Response (dB)')
plt.legend()


MMC_Pha = r"G:\project\MMC_HVDC\MMC_Positive_data\Pha_scan_Yap_MMC.mat"
MMC_Pha_data = loadmat(MMC_Pha)

f_can_MMC = r"G:\project\MMC_HVDC\MMC_Positive_data\f_scan_MMC.mat"
f_MMC = loadmat(f_can_MMC)

MMC_Pha_data = MMC_Pha_data['Pha_scan_Yap']
f_data_MMC = f_MMC['f_scan']

plt.plot(np.squeeze(f_data_MMC)[1:110], np.squeeze(MMC_Pha_data)[1:110], label='Real')
Length = len(f_data_MMC)

sindy_library1 = ps.PolynomialLibrary(degree=10, include_bias=True)
model_Block1 = ps.SINDy(feature_library = sindy_library1)
model_Block1.fit(np.squeeze(MMC_Pha_data), t = dt)

predicted = model_Block1.predict(np.squeeze(MMC_Pha_data).reshape(-1))

# x1, y1 = 105, -50
# x2, y2 = 0, -60


plt.plot(np.squeeze(f_data_MMC)[1:110], np.squeeze(MMC_Pha_data)[1:110], label='Identification')

# plt.plot([x1, x2], [y1, y2], color='b', linestyle='-.')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase Response')
plt.legend()



MMC_Mag_scan_Ycp = r"G:\project\MMC_HVDC\MMC_Positive_data\Mag_scan_Ycp.mat"
MMC_Mag_scan_Ycp_data = loadmat(MMC_Mag_scan_Ycp)

f_can_MMC = r"G:\project\MMC_HVDC\MMC_Positive_data\f_scan_MMC.mat"
f_MMC = loadmat(f_can_MMC)

MMC_Mag_scan_Ycp_data = MMC_Mag_scan_Ycp_data['Mag_scan_Ycp']
f_data_MMC = f_MMC['f_scan']

plt.plot(np.squeeze(f_data_MMC), np.squeeze(MMC_Mag_scan_Ycp_data), label='Real')

plt.plot(np.squeeze(f_data_MMC), np.squeeze(MMC_Mag_scan_Ycp_data), label='Identification')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Frequency Response (dB)')
plt.legend()




MMC_Pha_scan_Ycp = r"G:\project\MMC_HVDC\MMC_Positive_data\Pha_scan_Ycp.mat"
MMC_Pha_scan_Ycp_data = loadmat(MMC_Pha_scan_Ycp)

f_can_MMC = r"G:\project\MMC_HVDC\MMC_Positive_data\f_scan_MMC.mat"
f_MMC = loadmat(f_can_MMC)

MMC_Pha_scan_Ycp_data = MMC_Pha_scan_Ycp_data['Pha_scan_Ycp']
f_data_MMC = f_MMC['f_scan']

plt.plot(np.squeeze(f_data_MMC), np.squeeze(MMC_Pha_scan_Ycp_data), label='Real')

plt.plot(np.squeeze(f_data_MMC), np.squeeze(MMC_Pha_scan_Ycp_data), label='Identification')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase Response')
plt.legend(loc='best');




Mag_scan_Yap_Grid = r"G:\project\Grid_Positive_data2\Mag_scan_Yap_Grid.mat"
Mag_scan_Yap_Grid_data = loadmat(Mag_scan_Yap_Grid)


f_can_Grid = r"G:\project\Grid_Positive_data2\f_can_Grid.mat"
f_data_Grid = loadmat(f_can_Grid)


Mag_scan_Yap_Grid_data = Mag_scan_Yap_Grid_data['Mag_scan_Yap']
f_data_Grid = f_data_Grid['f_scan']

plt.plot(np.squeeze(f_data_Grid), np.squeeze(Mag_scan_Yap_Grid_data), label='Real')

plt.plot(np.squeeze(f_data_Grid), np.squeeze(Mag_scan_Yap_Grid_data), label='Identification')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Frequency Response (dB)')
plt.legend()


Pha_scan_Yap_Grid = r"G:\project\Grid_Positive_data2\Pha_scan_Yap_Grid.mat"
Pha_scan_Yap_Grid_data = loadmat(Pha_scan_Yap_Grid)


f_can_Grid = r"G:\project\Grid_Positive_data2\f_can_Grid.mat"
f_data_Grid = loadmat(f_can_Grid)


Pha_scan_Yap_Grid_data = Pha_scan_Yap_Grid_data['Pha_scan_Yap']
f_data_Grid = f_data_Grid['f_scan']

plt.plot(np.squeeze(f_data_Grid), np.squeeze(Pha_scan_Yap_Grid_data), label='Real')

plt.plot(np.squeeze(f_data_Grid), np.squeeze(Pha_scan_Yap_Grid_data), label='Identification')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase Response')
plt.legend()



