# -*- coding: utf-8 -*-

import sys
import numpy as np
import tensorly.decomposition as tsd
import tensorly.cp_tensor as tsc

# Arguments
args = sys.argv
infile = args[1]
outfile = args[2]
cp_rank = int(args[3])
n_iter_max = int(args[4])
ratio = int(args[5])

# Functions
def rec_error(tensor, rec_tensor):
    return np.sum((tensor - rec_tensor)**2) / np.size(tensor)

# Loading Data Tensor
tnsr = np.load(infile)

# Non-negative CP Decomposition
res = tsd.non_negative_parafac(tensor=tnsr, n_iter_max=n_iter_max, rank=cp_rank, init='svd', verbose=True)
res = tsc.cp_to_tensor(res)
error = rec_error(tnsr, res)

# Save
np.savetxt(outfile, [error])
