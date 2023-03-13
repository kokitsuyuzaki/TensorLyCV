# -*- coding: utf-8 -*-

# Package Loading
import sys
import numpy as np
import tensorly.decomposition as tsd
import tensorly.cp_tensor as tsc
import pickle as pkl

# Arguments passed by Snakemake
args = sys.argv
infile = args[1]
outfile1 = args[2]
outfile2 = args[3]
outfile3 = args[4]
cp_rank = int(args[5])
n_iter_max = int(args[6])
ratio = int(args[7])

# Function to return reconstruction error
def rec_error(tensor, rec_tensor):
    return np.sum((tensor - rec_tensor)**2) / np.size(tensor)

# Loading Data Tensor
tnsr = np.load(infile)

# Assign 0 to nan
tnsr = np.nan_to_num(tnsr, nan = 0)

# Non-negative CP Decomposition (NTF) by TensorLy
res = tsd.non_negative_parafac(tensor=tnsr, n_iter_max=n_iter_max, rank=cp_rank, init='svd', verbose=True)

# Save CSV files
for i in range(len(res[1])):
    outfile = outfile1.replace("FINISH", "factor" + str(i+1) + ".csv")
    np.savetxt(outfile, res[1][i], delimiter=",")

# Save Pickle file
with open (outfile3, 'wb') as f:
    pkl.dump(res, f)

# Save reconstuction error into a text file
res = tsc.cp_to_tensor(res)
error = rec_error(tnsr, res)
np.savetxt(outfile2, [error])
