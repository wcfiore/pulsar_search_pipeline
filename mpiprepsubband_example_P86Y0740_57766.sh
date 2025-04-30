#!/bin/bash
#PBS -M mdecesar@nrao.edu
#PBS -m ae
#PBS -V
#PBS -N P86Y0740_57766
#PBS -l nodes=nimrod:ppn=1+5:new:ppn=10

NUMCPUS=10
SOURCE=P86Y0740
MJD=57766
SCAN=0839
BASEFILE=puppi_${MJD}_${SOURCE}_${SCAN}
PROJECTNM=Fermi_${SOURCE}_${MJD}
SCRATCHDIR=/scratch/${PROJECTNM}
INDIR=/data1/people/mdecesar/data/Fermi_Srcs/AO/P3133/PUPPI/${SOURCE}/${MJD}
OUTDIR=/data1/people/mdecesar/results/Fermi_Srcs/AO/P3133/PUPPI/${SOURCE}/${MJD}
RAWFILES=${INDIR}/${BASEFILE}_????.fits
MASKFILE=${OUTDIR}/puppi_${MJD}_${SOURCE}_${SCAN}_rfifind.mask
BIRDSFILE=${OUTDIR}/puppi_${MJD}_${SOURCE}_${SCAN}_topo.birds

BARYV=8.884865e-05
NUMHARM=8
SIGMA=1.6
FLO=2.0
#ZMAX=50

# The following are executed by each node
pbsdsh -u -- mkdir -m 1775 -p ${SCRATCHDIR}
# Copy the analysis script to each node
pbsdsh -u -- cp /data1/people/mdecesar/scripts/full_analysis_nimrod2_zmax4_50_200.py ${SCRATCHDIR}
# We need one .birds file
pbsdsh -u -- cp -f ${BIRDSFILE} ${SCRATCHDIR}

# Parallel de-dispersion
# Good full-res length for 855-sec files is 10400000

NUMOUT=17500000
LODM=0.0
DMSTEP=0.03
NUMDMS=2050
PREPOPTS="-nsub 64"
mpiexec mpiprepsubband -o ${SCRATCHDIR}/${PROJECTNM} -lodm ${LODM} -dmstep ${DMSTEP} -numdms ${NUMDMS} -numout ${NUMOUT} -mask ${MASKFILE} ${PREPOPTS} ${RAWFILES}

NUMOUT=17500000
LODM=61.5
DMSTEP=0.03
NUMDMS=2050
PREPOPTS="-nsub 64"
mpiexec mpiprepsubband -o ${SCRATCHDIR}/${PROJECTNM} -lodm ${LODM} -dmstep ${DMSTEP} -numdms ${NUMDMS} -numout ${NUMOUT} -mask ${MASKFILE} ${PREPOPTS} ${RAWFILES}

NUMOUT=8750000
LODM=123.0
DMSTEP=0.05
NUMDMS=1500
PREPOPTS="-nsub 64 -downsamp 2"
mpiexec mpiprepsubband -o ${SCRATCHDIR}/${PROJECTNM} -lodm ${LODM} -dmstep ${DMSTEP} -numdms ${NUMDMS} -numout ${NUMOUT} -mask ${MASKFILE} ${PREPOPTS} ${RAWFILES}

NUMOUT=4375000
LODM=198.0
DMSTEP=0.1
NUMDMS=1800
PREPOPTS="-nsub 64 -downsamp 4"
mpiexec mpiprepsubband -o ${SCRATCHDIR}/${PROJECTNM} -lodm ${LODM} -dmstep ${DMSTEP} -numdms ${NUMDMS} -numout ${NUMOUT} -mask ${MASKFILE} ${PREPOPTS} ${RAWFILES}

NUMOUT=2187500
LODM=378.0
DMSTEP=0.3
NUMDMS=1800
PREPOPTS="-nsub 64 -downsamp 8"
mpiexec mpiprepsubband -o ${SCRATCHDIR}/${PROJECTNM} -lodm ${LODM} -dmstep ${DMSTEP} -numdms ${NUMDMS} -numout ${NUMOUT} -mask ${MASKFILE} ${PREPOPTS} ${RAWFILES}

# Now the searches
#pbsdsh -- python ${SCRATCHDIR}/full_analysis_nimrod2_med.py --fft --numcpus ${NUMCPUS} --workdir ${SCRATCHDIR} --zmax ${ZMAX} --flo ${FLO} --sigma ${SIGMA} --baryv ${BARYV} --outdir ${OUTDIR} --numharm ${NUMHARM}
pbsdsh -- python ${SCRATCHDIR}/full_analysis_nimrod2_zmax4_50_200.py --fft --numcpus ${NUMCPUS} --workdir ${SCRATCHDIR} --flo ${FLO} --sigma ${SIGMA} --baryv ${BARYV} --outdir ${OUTDIR} --numharm ${NUMHARM}
