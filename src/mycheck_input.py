# -*- coding: utf-8 -*-

import sys
import numpy as np

# Arguments
args = sys.argv
infile = args[1]

# Loading Data Tensor
tnsr = np.load(infile)

if len(tnsr.shape) != 3:
    print("The dimension of data tensor must be 3 for now")
    quit()