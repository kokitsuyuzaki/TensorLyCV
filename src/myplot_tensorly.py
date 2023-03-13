# -*- coding: utf-8 -*-

# Package Loading
import sys
import matplotlib.pyplot as plt
import pandas as pd

# Arguments passed by Snakemake
args = sys.argv
infile = args[1]
outfile = args[2]

# Loading a CSV file (test_errors.csv or rec_errors.csv)
df = pd.read_csv(infile)

# Save Box Plot
# x-axis: Rank
# y-axis: Test Error or Reconst. Error
plt.figure()
df.boxplot()
plt.savefig(outfile)
plt.close('all')
