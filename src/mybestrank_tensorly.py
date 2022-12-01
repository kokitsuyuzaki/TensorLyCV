# -*- coding: utf-8 -*-

import sys
import numpy as np
import tensorly.decomposition as tsd
import pickle as pkl

# Arguments
args = sys.argv
infile1 = args[1]
infile2 = args[2]
outfile1 = args[3]
outfile2 = args[4]
outfile3 = args[5]
outfile4 = args[6]
outfile5 = args[7]
n_iter_max = int(args[8])

# Loading Data Tensor
tnsr = np.load(infile1)
cp_rank = int(np.loadtxt(infile2))

# Non-negative CP Decomposition
res = tsd.non_negative_parafac(tensor=tnsr, n_iter_max=n_iter_max,
    rank=cp_rank, return_errors=True, verbose=True)

# Output Objects
factor1 = res[0][1][0]
factor2 = res[0][1][1]
factor3 = res[0][1][2]
error = res[1][-1]

# Save
np.savetxt(outfile1, factor1, delimiter=",")
np.savetxt(outfile2, factor2, delimiter=",")
np.savetxt(outfile3, factor3, delimiter=",")
np.savetxt(outfile4, [error])

with open (outfile5, 'wb') as f:
    pkl.dump(res, f)
