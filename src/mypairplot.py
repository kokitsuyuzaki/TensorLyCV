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
	g.map_lower(sns.scatterplot)
	g.add_legend()
	plt.savefig(outfile)
	plt.close('all')

# Loading
tnsr = np.load(infile1)

# Setting Color
indir = infile2.replace('FINISH', '')
factor_infile = indir + "factor1.csv"
factor1 = pd.read_csv(factor_infile, header=None)
mycolor = dict(zip(
	list(range(0, factor1.shape[1])),
	sns.color_palette("Dark2", factor1.shape[1]),))

# Plot Factor matrix
for i in range(len(tnsr.shape)):
	factor_infile = indir + "factor" + str(i+1) + ".csv"
	factor_outfile = outfile.replace("FINISH", "factor" + str(i+1) + ".png")
	factor = pd.read_csv(factor_infile, header=None)
	factor_cluster = assign_cluster(factor)
	print(PairPlot(factor_cluster, mycolor, factor_outfile))
