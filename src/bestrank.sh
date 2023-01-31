#!/bin/bash
#$ -l nc=4
#$ -p -50
#$ -r yes
#$ -q node.q

#SBATCH -n 4
#SBATCH --nice=50
#SBATCH --requeue
#SBATCH -p node03-06
SLURM_RESTART_COUNT=2

python src/mybestrank.py $1 ${@: -1}

OUTDIR=`echo $1 | sed -e "s|/tensorly/test_errors.csv||"`
BESTRANK=`cat ${@: -1}`

rm -rf $OUTDIR"/tensorly/bestrank"
cp -rf $OUTDIR"/tensorly/"$BESTRANK $OUTDIR"/tensorly/bestrank"
