# -*- coding: utf-8 -*-

# Package Loading
import sys
import numpy as np

# Arguments passed by Snakemake
args = sys.argv
infile = args[1]
outfile = args[2]

# Loading Data Tensor (NumPy array)
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

# Convert Int => Float
tnsr = 1.0 * tnsr

# Saving a Numpy array into a Numpy's Binary file
np.save(outfile, tnsr)
