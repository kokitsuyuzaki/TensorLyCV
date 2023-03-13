# -*- coding: utf-8 -*-

# Package Loading
import sys
import numpy as np
import pandas as pd

# Arguments passed by Snakemake
args = sys.argv
cp_min_rank = int(args[1])
cp_max_rank = int(args[2])
trials = int(args[3])
indir = args[4]
outfile = args[5]

# for all the trials (e.g., 50)
errors = []
for i in list(range(1, trials+1)):
    errors2 = []
    # for all the rank (e.g., 1 to 10)
    for j in list(range(cp_min_rank, cp_max_rank+1)):
        # Loading a error value from error.txt to error2
        filename = indir + "/tensorly/" + str(j) + "/wo_mask/" + str(i) + "/error.txt"
        errors2.append(np.loadtxt(filename))
    # error2 is then append into an vector (errors)
    errors.append(errors2)
# Finally, errors are reshaped into a pandas DataFrame
df = pd.DataFrame(errors, index=range(1, trials+1), columns=range(cp_min_rank, cp_max_rank+1))

# Save a pandas DataFrame to CSV
df.to_csv(outfile, index=False)
