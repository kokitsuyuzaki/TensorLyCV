from snakemake.utils import min_version

#################################
# Setting
#################################
# Minimum Version of Snakemake
min_version("7.1.0")

# Required Arguments
INPUT = config["input"]
OUTDIR = config["outdir"]

# Optional Arguments
RANK_MIN = int(config["rank_min"])
RANK_MAX = int(config["rank_max"])
CP_RANKS = [str(x) for x in list(range(RANK_MIN, RANK_MAX + 1))]
TRIALS = int(config["trials"])
TRIAL_INDEX = [str(x) for x in list(range(1, TRIALS+1))]
N_ITER_MAX = int(config["n_iter_max"])
RATIO = int(config["ratio"])

# Docker Container
container: 'docker://koki/tensorlycv_component:latest'

# All Rules
rule all:
	input:
		OUTDIR + '/plot/test_errors.png',
		OUTDIR + '/plot/rec_errors.png',
		expand(OUTDIR + '/plot/barplot/{cp_rank}/FINISH', cp_rank=CP_RANKS),
		expand(OUTDIR + '/plot/pairplot/{cp_rank}/FINISH', cp_rank=CP_RANKS),
		OUTDIR + '/plot/barplot/bestrank/FINISH',
		OUTDIR + '/plot/pairplot/bestrank/FINISH'

#############################################################
# Checks for non-zero or non-empty tensor data
#############################################################
rule check_input:
	input:
		INPUT
	output:
		OUTDIR + '/FLOAT_DATA.npy'
	benchmark:
		OUTDIR + '/benchmarks/check_input.txt'
	log:
		OUTDIR + '/logs/check_input.log'
	shell:
		'src/check_input.sh {input} {output} >& {log}'

#############################################################
# TensorLyCV with mask tensor
#############################################################
rule tensorly_w_mask:
	input:
		OUTDIR + '/FLOAT_DATA.npy'
	output:
		OUTDIR + '/tensorly/{cp_rank}/w_mask/{t}/error.txt'
	wildcard_constraints:
		cp_rank='|'.join([re.escape(x) for x in CP_RANKS])
	benchmark:
		OUTDIR + '/benchmarks/tensorly/{cp_rank}/w_mask/{t}.txt'
	log:
		OUTDIR + '/logs/tensorly/{cp_rank}/w_mask/{t}.log'
	shell:
		'src/tensorly_w_mask.sh {input} {output} {wildcards.cp_rank} {N_ITER_MAX} {RATIO} > {log}'

#############################################################
# TensorLyCV without mask tensor
#############################################################
rule tensorly_wo_mask:
	input:
		OUTDIR + '/FLOAT_DATA.npy'
	output:
		OUTDIR + '/tensorly/{cp_rank}/wo_mask/{t}/FINISH',
		OUTDIR + '/tensorly/{cp_rank}/wo_mask/{t}/error.txt',
		OUTDIR + '/tensorly/{cp_rank}/wo_mask/{t}/tensorly.pkl'
	wildcard_constraints:
		t='|'.join([re.escape(x) for x in TRIAL_INDEX])
	benchmark:
		OUTDIR + '/benchmarks/tensorly/{cp_rank}/wo_mask/{t}.txt'
	log:
		OUTDIR + '/logs/tensorly/{cp_rank}/wo_mask/{t}.log'
	shell:
		'src/tensorly_wo_mask.sh {input} {output} {wildcards.cp_rank} {N_ITER_MAX} {RATIO} > {log}'

#############################################################
# Aggregation of the results of tensorly_w_mask to CSV
#############################################################
rule aggregate_tensorly_w_mask:
	input:
		expand(OUTDIR + '/tensorly/{cp_rank}/w_mask/{t}/error.txt',
			cp_rank=CP_RANKS, t=TRIAL_INDEX)
	output:
		OUTDIR + '/tensorly/test_errors.csv'
	benchmark:
		OUTDIR + '/benchmarks/aggregate_tensorly_w_mask.txt'
	log:
		OUTDIR + '/logs/aggregate_tensorly_w_mask.log'
	shell:
		'src/aggregate_tensorly_w_mask.sh {RANK_MIN} {RANK_MAX} {TRIALS} {OUTDIR} {output} > {log}'

#############################################################
# Aggregation of the results of tensorly_wo_mask to CSV
#############################################################
rule aggregate_tensorly_wo_mask:
	input:
		expand(OUTDIR + '/tensorly/{cp_rank}/wo_mask/{t}/error.txt',
			cp_rank=CP_RANKS, t=TRIAL_INDEX)
	output:
		OUTDIR + '/tensorly/rec_errors.csv'

	benchmark:
		OUTDIR + '/benchmarks/aggregate_tensorly_wo_mask.txt'
	log:
		OUTDIR + '/logs/aggregate_tensorly_wo_mask.log'
	shell:
		'src/aggregate_tensorly_wo_mask.sh {RANK_MIN} {RANK_MAX} {TRIALS} {OUTDIR} {output} > {log}'

#############################################################
# Selection of the trial with the smallest
# reconstruction error for each rank
#############################################################
def aggregate_trials(cp_rank):
	out = []
	for j in range(len(TRIAL_INDEX)):
		out.append(OUTDIR + '/tensorly/' + cp_rank[0] + '/wo_mask/' + TRIAL_INDEX[j] + '/error.txt')
	return(out)

rule besttrial:
	input:
		aggregate_trials
	output:
		OUTDIR + '/tensorly/{cp_rank}/wo_mask/besttrial/FINISH',
		OUTDIR + '/tensorly/{cp_rank}/wo_mask/besttrial/error.txt',
		OUTDIR + '/tensorly/{cp_rank}/wo_mask/besttrial/tensorly.pkl'
	benchmark:
		OUTDIR + '/benchmarks/besttrial_{cp_rank}.txt'
	log:
		OUTDIR + '/logs/besttrial_{cp_rank}.log'
	shell:
		'src/besttrial.sh {wildcards.cp_rank} {output} > {log}'

#############################################################
# Selection of the rank with the smallest
# test error out of all ranks
#############################################################
rule bestrank:
	input:
		OUTDIR + '/tensorly/test_errors.csv',
		expand(OUTDIR + '/tensorly/{cp_rank}/wo_mask/besttrial/FINISH',
			cp_rank=CP_RANKS),
		expand(OUTDIR + '/tensorly/{cp_rank}/wo_mask/besttrial/error.txt',
			cp_rank=CP_RANKS),
		expand(OUTDIR + '/tensorly/{cp_rank}/wo_mask/besttrial/tensorly.pkl',
			cp_rank=CP_RANKS)
	output:
		OUTDIR + '/tensorly/bestrank/wo_mask/besttrial/FINISH',
		OUTDIR + '/tensorly/bestrank/wo_mask/besttrial/error.txt',
		OUTDIR + '/tensorly/bestrank/wo_mask/besttrial/tensorly.pkl',
		OUTDIR + '/tensorly/bestrank.txt'
	benchmark:
		OUTDIR + '/benchmarks/bestrank.txt'
	log:
		OUTDIR + '/logs/bestrank.log'
	shell:
		'src/bestrank.sh {input} {output} > {log}'

#############################################################
# Plot of test errors at all ranks and all trials
#############################################################
rule plot_test_error:
	input:
		OUTDIR + '/tensorly/test_errors.csv'
	output:
		OUTDIR + '/plot/test_errors.png'
	benchmark:
		OUTDIR + '/benchmarks/plot_test_error.txt'
	log:
		OUTDIR + '/logs/plot_test_error.log'
	shell:
		'src/plot_tensorly.sh {input} {output} > {log}'

#############################################################
# Plot of reconstuction errors at all ranks and all trials
#############################################################
rule plot_rec_error:
	input:
		OUTDIR + '/tensorly/rec_errors.csv'
	output:
		OUTDIR + '/plot/rec_errors.png'
	benchmark:
		OUTDIR + '/benchmarks/plot_rec_error.txt'
	log:
		OUTDIR + '/logs/plot_rec_error.log'
	shell:
		'src/plot_tensorly.sh {input} {output} > {log}'

#############################################################
# Pairplots of factor matrices at all ranks
#############################################################
rule pairplot_allranks:
	input:
		OUTDIR + '/FLOAT_DATA.npy',
		OUTDIR + '/tensorly/{cp_rank}/wo_mask/besttrial/FINISH'
	output:
		OUTDIR + '/plot/pairplot/{cp_rank}/FINISH'
	benchmark:
		OUTDIR + '/benchmarks/pairplot_allranks_{cp_rank}.txt'
	log:
		OUTDIR + '/logs/pairplot_allranks_{cp_rank}.log'
	shell:
		'src/pairplot.sh {input} {output} > {log}'

#############################################################
# Pairplots of factor matrices at optimal rank
#############################################################
rule pairplot_bestrank:
	input:
		OUTDIR + '/FLOAT_DATA.npy',
		OUTDIR + '/tensorly/bestrank/wo_mask/besttrial/FINISH'
	output:
		OUTDIR + '/plot/pairplot/bestrank/FINISH'
	benchmark:
		OUTDIR + '/benchmarks/pairplot_bestrank.txt'
	log:
		OUTDIR + '/logs/pairplot_bestrank.log'
	shell:
		'src/pairplot.sh {input} {output} > {log}'

#############################################################
# Bar charts of factor matrices at all ranks
#############################################################
rule barplot_allranks:
	input:
		OUTDIR + '/FLOAT_DATA.npy',
		OUTDIR + '/tensorly/{cp_rank}/wo_mask/besttrial/FINISH'
	output:
		OUTDIR + '/plot/barplot/{cp_rank}/FINISH'
	benchmark:
		OUTDIR + '/benchmarks/barplot_allranks_{cp_rank}.txt'
	log:
		OUTDIR + '/logs/barplot_allranks_{cp_rank}.log'
	shell:
		'src/barplot.sh {input} {output} > {log}'

#############################################################
# Bar charts of factor matrices at optimal rank
#############################################################
rule barplot_bestrank:
	input:
		OUTDIR + '/FLOAT_DATA.npy',
		OUTDIR + '/tensorly/bestrank/wo_mask/besttrial/FINISH'
	output:
		OUTDIR + '/plot/barplot/bestrank/FINISH'
	benchmark:
		OUTDIR + '/benchmarks/barplot_bestrank.txt'
	log:
		OUTDIR + '/logs/barplot_bestrank.log'
	shell:
		'src/barplot.sh {input} {output} > {log}'
