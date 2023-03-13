# -*- coding: utf-8 -*-

# Package Loading
import sys
import numpy as np
import pandas as pd

# Arguments passed by Snakemake
args = sys.argv
infile = args[1]
outfile = args[2]

# Loading a CSV file (output/2/wo_mask/1/test_errors.csv)
df = pd.read_csv(infile)

# In each rank, the median is calculated,
# and then the minimum value of the median
# is returned as the best rank
best_rank = int(df.median().idxmin())

# Saving the best rank in a text file
np.savetxt(outfile, [best_rank], fmt="%d")
