# -*- coding: utf-8 -*-

# Package Loading
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Arguments passed by Snakemake
args = sys.argv
infile1 = args[1]
infile2 = args[2]
outfile = args[3]

# Bar Plot Function for large data (No. of data > 50)
def BarPlotLarge(factor, outfile):
	sns.set(font_scale=4)
	plt.figure()
	g = sns.catplot(data=factor, x="id", y="value", kind="bar", row="variable", height=10, aspect=4, linewidth=0, color = "black")
	g.set(xticklabels=[])
	plt.savefig(outfile, dpi=300)
	plt.close('all')

# Bar Plot Function for small data (No. of data <= 50)
def BarPlotSmall(factor, outfile):
	sns.set(font_scale=4)
	plt.figure()
	sns.catplot(data=factor, x="id", y="value", kind="bar", row="variable", height=10, aspect=4)
	plt.savefig(outfile, dpi=300)
	plt.close('all')

# Main Bar Plot Function
def BarPlot(factor, outfile):
	# Reshaping a matrix data to tidy data by Pandas DataFrame
	column_name = ["dim" + str(x) for x in range(1, factor.shape[1]+1)]
	id = pd.DataFrame(list(range(1, factor.shape[0]+1)))
	factor = pd.concat([factor, id], axis=1)
	column_name.append("id")
	factor.columns = column_name
	factor = pd.melt(factor, id_vars="id")
	# Plot
	large = factor.shape[0] > 50
	if large:
		BarPlotLarge(factor, outfile)
	else:
		BarPlotSmall(factor, outfile)

# Loading a Numpy array from a Numpy's Binary file
tnsr = np.load(infile1)

# Plot Factor matrix
indir = infile2.replace('FINISH', '')
for i in range(len(tnsr.shape)):
	# Input CSV file name (e.g., factor1.csv)
	factor_infile = indir + "factor" + str(i+1) + ".csv"
	# Output figure file name (e.g., factor1.png)
	factor_outfile = outfile.replace("FINISH", "factor" + str(i+1) + ".png")
	# Loading a CSV file
	factor = pd.read_csv(factor_infile, header=None)
	# Plot Bar plot
	print(BarPlot(factor, factor_outfile))
