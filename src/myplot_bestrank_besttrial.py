# -*- coding: utf-8 -*-

import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Arguments
args = sys.argv
infile = args[1]
outfile1 = args[2]
outfile2 = args[3]
outfile3 = args[4]
outdir = args[5]

# Loading
best_rank = int(np.loadtxt(infile))
factor_file1 = outdir + "/tensorly/bestrank/" + str(best_rank) + "/factor1.csv"
factor_file2 = outdir + "/tensorly/bestrank/" + str(best_rank) + "/factor2.csv"
factor_file3 = outdir + "/tensorly/bestrank/" + str(best_rank) + "/factor3.csv"
factor1 = pd.read_csv(factor_file1, header=None)
factor2 = pd.read_csv(factor_file2, header=None)
factor3 = pd.read_csv(factor_file3, header=None)

# Save
plt.figure()
g = sns.PairGrid(factor1)
g.map_diag(sns.histplot)
g.map_upper(sns.scatterplot)
g.map_lower(sns.kdeplot)
plt.savefig(outfile1)
plt.close('all')

plt.figure()
g = sns.PairGrid(factor2)
g.map_diag(sns.histplot)
g.map_upper(sns.scatterplot)
g.map_lower(sns.kdeplot)
plt.savefig(outfile2)
plt.close('all')

plt.figure()
g = sns.PairGrid(factor3)
g.map_diag(sns.histplot)
g.map_upper(sns.scatterplot)
g.map_lower(sns.kdeplot)
plt.savefig(outfile3)
plt.close('all')
