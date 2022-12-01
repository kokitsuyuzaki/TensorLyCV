# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd

# Arguments
args = sys.argv
infile = args[1]
outfile = args[2]

# Loading
df = pd.read_csv(infile)

# Minimum median index
error = int(df.median().idxmin())

# Save
np.savetxt(outfile, [error], fmt="%d")
