# -*- coding: utf-8 -*-

import sys
import matplotlib.pyplot as plt
import pandas as pd

# Arguments
args = sys.argv
infile = args[1]
outfile = args[2]

# Loading Data Tensor
df = pd.read_csv(infile)

# Save
plt.figure()
df.boxplot()
plt.savefig(outfile)
plt.close('all')
