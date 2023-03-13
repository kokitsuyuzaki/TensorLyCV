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

# Function to assign color
# In each data, the dimension with the highest value is selected (e.g., 3)
# and then the corresponding color code (mycolor) is assigned
def assign_cluster(factor):
	factor = pd.concat([factor, factor.idxmax(axis=1)], axis=1)
	column_name1 = ["dim" + str(x) for x in range(1, factor.shape[1])]
	column_name1.append("cluster")
	factor.columns = column_name1
	return(factor)

# Main Pair Plot Function
def PairPlot(factor, mycolor, outfile):
	plt.figure()
	g = sns.PairGrid(factor, hue="cluster", palette=mycolor)
	g.map_diag(sns.histplot)
	g.map_upper(sns.scatterplot)
	g.map_lower(sns.scatterplot)
	g.add_legend()
	plt.savefig(outfile)
	plt.close('all')

# Loading a Numpy array from a Numpy's Binary file
tnsr = np.load(infile1)

# Color palette to color the data points
indir = infile2.replace('FINISH', '')
factor_infile = indir + "factor1.csv"
factor1 = pd.read_csv(factor_infile, header=None)
mycolor = dict(zip(
	list(range(0, factor1.shape[1])),
	sns.color_palette("Dark2", factor1.shape[1]),))

# Plot Factor matrix
for i in range(len(tnsr.shape)):
	# Input CSV file name (e.g., factor1.csv)
	factor_infile = indir + "factor" + str(i+1) + ".csv"
	# Output figure file name (e.g., factor1.png)
	factor_outfile = outfile.replace("FINISH", "factor" + str(i+1) + ".png")
	# Loading a CSV file
	factor = pd.read_csv(factor_infile, header=None)
	# Setting Color according to the factor matrix values
	factor_cluster = assign_cluster(factor)
	# Plot Pair plot
	print(PairPlot(factor_cluster, mycolor, factor_outfile))
