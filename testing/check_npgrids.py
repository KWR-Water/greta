# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 11:02:42 2021

@author: rosst
"""
import numpy as np
import os

parms = ["material","hk","vani","porosity","recharge"]
for iParm in parms:
    # material = np.load(r"d:\Greta_tool\greta\testing\test_files\material_phrea.npy", allow_pickle = True)
    globals()[iParm] = np.load(r"d:\Greta_tool\greta\testing\test_files" + "\\" + iParm + "_phrea.npy", allow_pickle = True)