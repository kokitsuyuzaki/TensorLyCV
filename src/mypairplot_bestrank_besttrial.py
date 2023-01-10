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
def assign_cluster(factor):
	factor = pd.concat([factor, factor.idxmax(axis=1)], axis=1)
	column_name1 = ["dim" + str(x) for x in range(1, factor.shape[1])]
	column_name1.append("cluster")
	factor.columns = column_name1
	return(factor)

def PairPlot(factor, mycolor, outfile):
	plt.figure()
	g = sns.PairGrid(factor, hue="cluster", palette=mycolor)
	g.map_diag(sns.histplot)
	g.map_upper(sns.scatterplot)
	g.map_lower(sns.kdeplot)
	g.add_legend()
	plt.savefig(outfile)
	plt.close('all')

# Loading
best_trial = int(np.loadtxt(infile))
factor_file1 = outdir + "/tensorly/bestrank/" + str(best_trial) + "/factor1.csv"
factor_file2 = outdir + "/tensorly/bestrank/" + str(best_trial) + "/factor2.csv"
factor_file3 = outdir + "/tensorly/bestrank/" + str(best_trial) + "/factor3.csv"
factor1 = pd.read_csv(factor_file1, header=None)
factor2 = pd.read_csv(factor_file2, header=None)
factor3 = pd.read_csv(factor_file3, header=None)

# Setting Color
mycolor = dict(zip(
	list(range(0, factor1.shape[1])),
	sns.color_palette("Dark2", factor1.shape[1]),))

# Assign Cluster Label
factor_cluster1 = assign_cluster(factor1)
factor_cluster2 = assign_cluster(factor2)
factor_cluster3 = assign_cluster(factor3)

# Plot Factor matrix 1
PairPlot(factor_cluster1, mycolor, outfile1)
PairPlot(factor_cluster2, mycolor, outfile2)
PairPlot(factor_cluster3, mycolor, outfile3)
