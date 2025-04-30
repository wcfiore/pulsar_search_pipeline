#!/usr/bin/python
from os import system, chdir, remove, environ
from sys import stdout, argv, exit
from glob import glob
from optparse import OptionParser
from fcntl import *

def myexecute(cmd):
    stdout.write("\n'"+cmd+"'\n")
    stdout.flush()
    system(cmd)

def main():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-f", "--fft", action="store_true", dest="fft", default=0,
                      help="Calculate (and later remove) the .fft files")
    parser.add_option("-v", "--baryvel", type="float", dest="baryv", default=0.0,
                      help="Barycentric velocity in units of c")
    parser.add_option("-o", "--outdir", type="string", dest="outdir", default=".",
                      help="Output directory to store results")
    parser.add_option("-w", "--workdir", type="string", dest="workdir", default=".",
                      help="Working directory for search")
    parser.add_option("-l", "--flo", type="float", dest="flo", default=1.0,
                      help="Low frequency (Hz) to search")
    parser.add_option("-x", "--fhi", type="float", dest="fhi", default=10000.0,
                      help="High frequency (Hz) to search")
    parser.add_option("-z", "--zmax", type="int", dest="zmax", default=170,
                      help="Maximum fourier drift (bins) to search")
    parser.add_option("-a", "--numharm", type="int", dest="numharm", default=8,
                      help="Number of harmonics to sum when searching")
    parser.add_option("-s", "--sigma", type="float", dest="sigma", default=2.0,
                      help="Cutoff sigma to consider a candidate")
    parser.add_option("-p", "--pmax", type="int", dest="pmax", default=6,
                      help="Maximum # of harmonics to sum in sideband search")
    parser.add_option("-n", "--nruns", type="int", dest="N", default=1,
                      help="Will submit this script # times")
    parser.add_option("-r", "--run", type="int", dest="run", default=1,
                      help="This is the #-th time submitting this script")
    (options, args) = parser.parse_args()
    if (options.outdir[-1]!="/"):
        options.outdir = options.outdir+"/"
    if (options.workdir!='.'):
        chdir(options.workdir)

    # Get the datafiles and determine their DMs from their names
    datanames = glob('*.dat')
    if (len(datanames)==0):
        exit(0)

    dms = []
    for dataname in datanames:
        loptr = dataname.find("_DM")+3
        hiptr = dataname.find(".dat")
        dms.append(float(dataname[loptr:hiptr]))
    dms.sort()

    # The basename of the data files
    basename = datanames[0][:loptr-3]

    # Get the bird file (the first birdie file in the directory!)
    birdnames = glob("*.birds")
    if birdnames:
        birdname = birdnames[0]

    for ii in range(len(dms)):
        dm = dms[ii]
        # Assign particular DMs to this run
        if ii%options.N == options.run: 
            filenamebase = basename+'_DM%.2f'%dm
            outnamebase = options.outdir+filenamebase
            if options.fft:
                 myexecute('realfft '+filenamebase+'.dat')
            myexecute('cp '+birdname+' '+filenamebase+'.birds')
            myexecute('makezaplist.py '+filenamebase+'.birds')
            myexecute('rm '+filenamebase+'.birds')
            myexecute('zapbirds -zap -zapfile '+filenamebase+ \
                    '.zaplist -baryv %g '%options.baryv+filenamebase+'.fft')
            myexecute('rm '+filenamebase+'.zaplist')
            #myexecute('search_bin -flo 80 -ncand 200 -harmsum 1 '+filenamebase+'.fft')
            #myexecute('search_bin -flo 80 -ncand 200 -harmsum %d '%options.pmax+filenamebase+'.fft')
            #myexecute('cp '+filenamebase+'_bin* '+options.outdir)
            ### zmax = 4 ###
            myexecute('accelsearch -sigma %f -zmax 4 -numharm %i -flo %f -fhi %f ' % \
                    (options.sigma, options.numharm, options.flo, options.fhi)+filenamebase+'.fft')
            myexecute('cp '+filenamebase+'_ACCEL_4 '+outnamebase + '_ACCEL_4')
            myexecute('cp '+filenamebase+'_ACCEL_4.cand '+outnamebase + '_ACCEL_4.cand')
            myexecute('cp '+filenamebase+'.inf '+outnamebase + '.inf')
            if options.fft:
                myexecute('rm '+filenamebase+'.fft')
        else: pass
    for ii in range(len(dms)):
        dm = dms[ii]
        if ii%options.N == options.run:
            filenamebase = basename+'_DM%.2f'%dm
            outnamebase = options.outdir+filenamebase
            if options.fft:
                 myexecute('realfft '+filenamebase+'.dat')
            myexecute('cp '+birdname+' '+filenamebase+'.birds')
            myexecute('makezaplist.py '+filenamebase+'.birds')
            myexecute('rm '+filenamebase+'.birds')
            myexecute('zapbirds -zap -zapfile '+filenamebase+ \
                    '.zaplist -baryv %g '%options.baryv+filenamebase+'.fft')
            myexecute('rm '+filenamebase+'.zaplist')
            ### zmax = 200 ###
            myexecute('accelsearch -sigma %f -zmax 200 -numharm %i -flo %f -fhi %f ' % \
                    (options.sigma, options.numharm, options.flo, options.fhi)+filenamebase+'.fft')
            myexecute('cp '+filenamebase+'_ACCEL_200 '+outnamebase + '_ACCEL_200')
            myexecute('cp '+filenamebase+'_ACCEL_200.cand '+outnamebase + '_ACCEL_200.cand')
            myexecute('cp '+filenamebase+'.inf '+outnamebase + '.inf')
            ### manual zmax ###
            #myexecute('accelsearch -sigma %f -zmax %d -numharm %d -flo %f -fhi %f ' % \
            #       (options.sigma, options.zmax, options.numharm, options.flo, options.fhi)+filenamebase+'.fft')
            #myexecute('cp '+filenamebase+'_ACCEL_%d '%options.zmax+options.outdir)
            #myexecute('cp '+filenamebase+'_ACCEL_%d.cand '%options.zmax+options.outdir)
            if options.fft:
                myexecute('rm '+filenamebase+'.fft')
        else: pass
    for ii in range(len(dms)):
        dm = dms[ii]
        if ii%options.N == options.run:
            filenamebase = basename+'_DM%.2f'%dm
            outnamebase = options.outdir+filenamebase
            myexecute('single_pulse_search.py -f -p '+filenamebase+'.dat')
            myexecute('cp '+filenamebase+'.singlepulse '+outnamebase+'.singlepulse')
        else: pass


if __name__ == "__main__":
      main()

