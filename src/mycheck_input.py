# -*- coding: utf-8 -*-

import sys
import numpy as np

# Arguments
args = sys.argv
infile = args[1]
outfile = args[2]

# Loading Data Tensor
tnsr = np.load(infile)

# Non-empty Check
if np.count_nonzero(tnsr) == 0:
    print("The data tensor is empty...")
    quit()

# Non-negative Check
booltnsr = tnsr < 0
if booltnsr.sum() != 0:
    print("The data tensor contains negative elements...")
    quit()

# Int => Float
tnsr = 1.0 * tnsr

# Save
np.save(outfile, tnsr)
