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
n_iter_max = int(args[6])

# Loading Data Tensor
tnsr = np.load(infile1)
cp_rank = int(np.loadtxt(infile2))

# Non-negative CP Decomposition
res = tsd.non_negative_parafac(tensor=tnsr, n_iter_max=n_iter_max, init='svd', rank=cp_rank, return_errors=True, verbose=True)

# Save
for i in range(len(res[0][1])):
    outfile = outfile1.replace("FINISH", "factor" + str(i+1) + ".csv")
    np.savetxt(outfile, res[0][1][i], delimiter=",")

error = res[1][-1]
np.savetxt(outfile2, [error])

with open (outfile3, 'wb') as f:
    pkl.dump(res, f)
