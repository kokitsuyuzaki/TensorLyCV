# -*- coding: utf-8 -*-

import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Arguments
args = sys.argv
infile1 = args[1]
infile2 = args[2]
outfile = args[3]
outdir = args[4]

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
tnsr = np.load(infile1)
best_trial = int(np.loadtxt(infile2))

# Plot Factor matrix
for i in range(len(tnsr.shape)):
	factor_infile = outdir + "/tensorly/bestrank/" + str(best_trial) + "/factor" + str(i+1) + ".csv"
	factor_outfile = outfile.replace("FINISH", "factor" + str(i+1) + ".png")
	factor = pd.read_csv(factor_infile, header=None)
	print(BarPlot(factor, factor_outfile))
