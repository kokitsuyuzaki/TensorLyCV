# -*- coding: utf-8 -*-

import sys
from distutils.dir_util import copy_tree
import glob
import numpy as np
import pandas as pd

# Arguments
args = sys.argv
c_rank = args[1]
outfile1 = args[2]
outfile2 = args[3]

# Loading
infiles = glob.glob(outfile2.replace('besttrial', '*'))
error = [pd.read_csv(x, header=None)[0][0] for x in infiles]

# Minimum index
best_trial = str(np.argmin(error) + 1)

# Save
to_dir = outfile1.replace('/FINISH', '')
from_dir = to_dir.replace('besttrial', best_trial)
copy_tree(from_dir, to_dir)
