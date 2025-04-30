import os, sys
import glob

sourcename = 'P86Y1373'
MJD = '57950'
scannumber = '0002'

basename = 'guppi_%s_%s_%s' % (MJD, sourcename, scannumber)
scratchdir = '/hyrule/data/scratch/wcfiore/Fermi_%s_%s' % (sourcename, MJD)
Nscratch = len(scratchdir)+1
resultsdir = '/hyrule/results/wcfiore/fermi_searches/%s/%s' % (sourcename, MJD)
Nresults = len(scratchdir)+1
scratchfiles = glob.glob('%s/%s_DM*.*.dat' % (scratchdir, basename)) + glob.glob('%s/%s_DM*.*.inf' % (scratchdir, basename)) + glob.glob('%s/%s_DM*.*.singlepulse' % (scratchdir, basename)) + glob.glob('%s/%s_DM*.*_ACCEL_4' % (scratchdir, basename)) + glob.glob('%s/%s_DM*.*_ACCEL_4.cand' % (scratchdir, basename)) + glob.glob('%s/%s_DM*.*_ACCEL_200' % (scratchdir, basename)) + glob.glob('%s/%s_DM*.*_ACCEL_200.cand' % (scratchdir, basename))
scratchfiles = [x[Nscratch:] for x in scratchfiles]
resultsfiles = glob.glob('%s/%s_DM*.*.dat' % (resultsdir, basename)) + glob.glob('%s/%s_DM*.*.inf' % (resultsdir, basename)) + glob.glob('%s/%s_DM*.*.singlepulse' % (resultsdir, basename)) + glob.glob('%s/%s_DM*.*_ACCEL_4' % (resultsdir, basename)) + glob.glob('%s/%s_DM*.*_ACCEL_4.cand' % (resultsdir, basename)) + glob.glob('%s/%s_DM*.*_ACCEL_200' % (resultsdir, basename)) + glob.glob('%s/%s_DM*.*_ACCEL_200.cand' % (resultsdir, basename))
resultsfiles = [x[Nresults:] for x in resultsfiles]
copyfiles = []
for f in scratchfiles:
    if f not in resultsfiles:
        print(f)
        sys.exit()
        cmd = 'cp %s/%s %s' % (scratchdir, f, resultsdir)
        print(cmd)
        os.system(cmd)
