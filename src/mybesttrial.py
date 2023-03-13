# -*- coding: utf-8 -*-

# Package Loading
import sys
from distutils.dir_util import copy_tree
import glob
import numpy as np
import pandas as pd

# Arguments passed by Snakemake
args = sys.argv
c_rank = args[1]
outfile1 = args[2]
outfile2 = args[3]

# Loading multiple text files (errors.txt) at once
infiles = glob.glob(outfile2.replace('besttrial', '*'))
error = [pd.read_csv(x, header=None)[0][0] for x in infiles]

# Minimum index corresponds the best trial in the rank
best_trial = str(np.argmin(error) + 1)

# A directory corresponding to the best trial
# is copied as a besttrial/
to_dir = outfile1.replace('/FINISH', '')
from_dir = to_dir.replace('besttrial', best_trial)
copy_tree(from_dir, to_dir)
