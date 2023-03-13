# -*- coding: utf-8 -*-

# Package Loading
import sys
import numpy as np
import tensorly.decomposition as tsd
import math
import random as rd
import tensorly.cp_tensor as tsc

# Arguments passed by Snakemake
args = sys.argv
infile = args[1]
outfile = args[2]
cp_rank = int(args[3])
n_iter_max = int(args[4])
ratio = int(args[5])

# Function to return test error
def test_error(tensor, mask_tensor, rec_tensor):
    x = (1 - mask_tensor) * tensor
    y = (1 - mask_tensor) * rec_tensor
    return np.sum((x - y)**2) / np.sum(mask_tensor)

# Loading Data Tensor
tnsr = np.load(infile)

# Mask Tensor
mask_tnsr = np.copy(tnsr)
mask_tnsr = np.where(np.isnan(mask_tnsr), 0, 1)

# Setting for Random Sampling
indices = np.where((tnsr != 0) & ~np.isnan(tnsr))
sample_loc = list(range(len(indices[0])))
no_sample = math.floor(len(indices[0]) * ratio / 100)

# Add Noise to Mask Tensor
mask_tnsr2 = np.copy(mask_tnsr)
target = rd.sample(sample_loc, no_sample)

cmd = "mask_tnsr2["
for i in range(len(tnsr.shape)-1):
    cmd = cmd + "indices[" + str(i) + "][target],"

cmd = cmd + "indices[" + str(len(tnsr.shape)-1) + "][target]] = 0"
exec(cmd)

# Assign 0 to nan
tnsr = np.nan_to_num(tnsr, nan = 0)

# Non-negative CP Decomposition (NTF) by TensorLy
res = tsd.non_negative_parafac(tensor=tnsr, mask=mask_tnsr2, n_iter_max=n_iter_max, rank=cp_rank, init='svd', verbose=True)
res = tsc.cp_to_tensor(res)

# Save test error into a text file
mask_tnsr3 = 1 - mask_tnsr + mask_tnsr2
error = test_error(tnsr, mask_tnsr3, res)
np.savetxt(outfile, [error])
