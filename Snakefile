from snakemake.utils import min_version

#################################
# Setting
#################################
# Minimum Version of Snakemake
min_version("6.0.5")

# Required Arguments
INPUT = config["input"]
OUTDIR = config["outdir"]

# Optional Arguments
CP_MAX_RANK = int(config["rank"])
CP_RANKS = [str(x) for x in list(range(1, CP_MAX_RANK + 1))]
TRIALS = int(config["trials"])
TRIAL_INDEX = [str(x) for x in list(range(1, TRIALS+1))]
ITERS = int(config["iters"])
RATIO = int(config["ratio"])

# Docker Container
container: 'docker://koki/tensorlycv_component:20221202'

#################################
# Rules
#################################
rule all:
	input:
		OUTDIR + '/plot/test_errors.png',
		OUTDIR + '/plot/bestrank_besttrial_factor1.png',
		OUTDIR + '/plot/bestrank_besttrial_factor2.png',
		OUTDIR + '/plot/bestrank_besttrial_factor3.png'

rule check_input:
	input:
		INPUT
	output:
		OUTDIR + '/CHECK_INPUT'
	benchmark:
		OUTDIR + '/benchmarks/check_input.txt'
	log:
		OUTDIR + '/logs/check_input.log'
	shell:
		'src/check_input.sh {input} {output} >& {log}'

rule tensorly:
	input:
		OUTDIR + '/CHECK_INPUT',
		INPUT
	output:
		OUTDIR + '/tensorly/{cp_rank}/{t}.txt'
	wildcard_constraints:
		cp_rank='|'.join([re.escape(x) for x in CP_RANKS])
	benchmark:
		OUTDIR + '/benchmarks/tensorly/{cp_rank}/{t}.txt'
	log:
		OUTDIR + '/logs/tensorly/{cp_rank}/{t}.log'
	shell:
		'src/tensorly.sh {input} {output} {wildcards.cp_rank} {ITERS} {RATIO} > {log}'

rule aggregate_tensorly:
	input:
		expand(OUTDIR + '/tensorly/{cp_rank}/{t}.txt',
			cp_rank=CP_RANKS, t=TRIAL_INDEX)
	output:
		OUTDIR + '/tensorly/test_errors.csv'
	benchmark:
		OUTDIR + '/benchmarks/aggregate_tensorly.txt'
	log:
		OUTDIR + '/logs/aggregate_tensorly.log'
	shell:
		'src/aggregate_tensorly.sh {CP_MAX_RANK} {TRIALS} {OUTDIR} {output} > {log}'

rule plot_tensorly:
	input:
		OUTDIR + '/tensorly/test_errors.csv'
	output:
		OUTDIR + '/plot/test_errors.png'
	benchmark:
		OUTDIR + '/benchmarks/plot_tensorly.txt'
	log:
		OUTDIR + '/logs/plot_tensorly.log'
	shell:
		'src/plot_tensorly.sh {input} {output} > {log}'

rule bestrank:
	input:
		OUTDIR + '/tensorly/test_errors.csv'
	output:
		OUTDIR + '/tensorly/bestrank.txt'
	benchmark:
		OUTDIR + '/benchmarks/bestrank.txt'
	log:
		OUTDIR + '/logs/bestrank.log'
	shell:
		'src/bestrank.sh {input} {output} > {log}'

rule bestrank_tensorly:
	input:
		INPUT,
		OUTDIR + '/tensorly/bestrank.txt'
	output:
		OUTDIR + '/tensorly/bestrank/{t}/factor1.csv',
		OUTDIR + '/tensorly/bestrank/{t}/factor2.csv',
		OUTDIR + '/tensorly/bestrank/{t}/factor3.csv',
		OUTDIR + '/tensorly/bestrank/{t}/error.txt',
		OUTDIR + '/tensorly/bestrank/{t}/tensorly.pkl'
	benchmark:
		OUTDIR + '/benchmarks/bestrank_tensorly_{t}.txt'
	log:
		OUTDIR + '/logs/bestrank_tensorly_{t}.log'
	shell:
		'src/bestrank_tensorly.sh {input} {output} {ITERS} > {log}'

rule bestrank_bestrial:
	input:
		expand(OUTDIR + '/tensorly/bestrank/{t}/error.txt',
			t=TRIAL_INDEX)
	output:
		OUTDIR + '/tensorly/bestrank/besttrial.txt'
	benchmark:
		OUTDIR + '/benchmarks/bestrank_bestrial.txt'
	log:
		OUTDIR + '/logs/bestrank_bestrial.log'
	shell:
		'src/bestrank_bestrial.sh {OUTDIR} {output} > {log}'

rule plot_bestrank_besttrial:
	input:
		OUTDIR + '/tensorly/bestrank/besttrial.txt'
	output:
		OUTDIR + '/plot/bestrank_besttrial_factor1.png',
		OUTDIR + '/plot/bestrank_besttrial_factor2.png',
		OUTDIR + '/plot/bestrank_besttrial_factor3.png'
	benchmark:
		OUTDIR + '/benchmarks/plot_bestrank_besttrial.txt'
	log:
		OUTDIR + '/logs/plot_bestrank_besttrial.log'
	shell:
		'src/plot_bestrank_besttrial.sh {input} {output} {OUTDIR} > {log}'
