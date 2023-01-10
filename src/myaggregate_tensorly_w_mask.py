# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd

# Arguments
args = sys.argv
cp_max_rank = int(args[1])
trials = int(args[2])
indir = args[3]
outfile = args[4]

# Loading all the files
errors = []
for i in list(range(1, trials+1)):
    errors2 = []
    for j in list(range(1, cp_max_rank+1)):
        filename = indir + "/tensorly/" + str(j) + "/w_mask/" + str(i) + ".txt"
        errors2.append(np.loadtxt(filename))
    errors.append(errors2)
df = pd.DataFrame(errors, index=range(1, trials+1), columns=range(1, cp_max_rank+1))

# Save
df.to_csv(outfile, index=False)
