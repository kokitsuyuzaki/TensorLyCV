# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd

# Arguments
args = sys.argv
cp_min_rank = int(args[1])
cp_max_rank = int(args[2])
trials = int(args[3])
indir = args[4]
outfile = args[5]

# Loading all the files
errors = []
for i in list(range(1, trials+1)):
    errors2 = []
    for j in list(range(cp_min_rank, cp_max_rank+1)):
        filename = indir + "/tensorly/" + str(j) + "/wo_mask/" + str(i) + "/error.txt"
        errors2.append(np.loadtxt(filename))
    errors.append(errors2)
df = pd.DataFrame(errors, index=range(1, trials+1), columns=range(cp_min_rank, cp_max_rank+1))

# Save
df.to_csv(outfile, index=False)
