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

# Functions
def BarPlotLarge(factor, outfile):
	sns.set(font_scale=4)
	plt.figure()
	g = sns.catplot(data=factor, x="id", y="value", kind="bar", row="variable", height=10, aspect=4, linewidth=0, color = "black")
	g.set(xticklabels=[])
	plt.savefig(outfile, dpi=300)
	plt.close('all')

def BarPlotSmall(factor, outfile):
	sns.set(font_scale=4)
	plt.figure()
	sns.catplot(data=factor, x="id", y="value", kind="bar", row="variable", height=10, aspect=4)
	plt.savefig(outfile, dpi=300)
	plt.close('all')

def BarPlot(factor, outfile):
	# Reshape to Tidy data
	large = factor.shape[0] > 50
	column_name = ["dim" + str(x) for x in range(1, factor.shape[1]+1)]
	id = pd.DataFrame(list(range(1, factor.shape[0]+1)))
	factor = pd.concat([factor, id], axis=1)
	column_name.append("id")
	factor.columns = column_name
	factor = pd.melt(factor, id_vars="id")
	# Plot
	if large:
		BarPlotLarge(factor, outfile)
	else:
		BarPlotSmall(factor, outfile)

# Loading
best_trial = int(np.loadtxt(infile))
factor_file1 = outdir + "/tensorly/bestrank/" + str(best_trial) + "/factor1.csv"
factor_file2 = outdir + "/tensorly/bestrank/" + str(best_trial) + "/factor2.csv"
factor_file3 = outdir + "/tensorly/bestrank/" + str(best_trial) + "/factor3.csv"
factor1 = pd.read_csv(factor_file1, header=None)
factor2 = pd.read_csv(factor_file2, header=None)
factor3 = pd.read_csv(factor_file3, header=None)

# Plot Factor matrix
BarPlot(factor1, outfile1)
BarPlot(factor2, outfile2)
BarPlot(factor3, outfile3)
