import os

# To use this script to help you dedisperse a bunch of time series, first
# run DDplan.py with appropriate values for your data to generate a
# dedispersion plan:
#
#[wcfiore@bowser 57955]$ DDplan.py -l 0.0 -d 500.0 -f 820.0 -b 200.0 -n 2048 -t 40.96e-6 -s 512
#
#Minimum total smearing     : 0.0598 ms
#--------------------------------------------
#Minimum channel smearing   : 0 ms
#Minimum smearing across BW : 0.0151 ms
#Minimum sample time        : 0.041 ms
#
#Setting the new 'best' resolution to : 0.041 ms
#Best guess for optimal initial dDM is 0.027
#
#  Low DM    High DM     dDM  DownSamp  dsubDM   #DMs  DMs/call  calls  WorkFract
#    0.000    111.000    0.03       1   11.10    3700     370      10    0.7362
#  111.000    192.600    0.05       2   20.40    1632     408       4    0.1624
#  192.600    355.800    0.10       4   40.80    1632     408       4    0.08118
#  355.800    519.000    0.20       8   81.60     816     408       2    0.02029
#
# Now with that plan, fill in the lists below and appropriate variables
# for your data and you can then generate the subbands and time series
# using "python dedisp.py"
#


def myexecute(cmd):
    print "'%s'"%cmd
    os.system(cmd)


# dDM steps from DDplan.py
dDMs      = [0.03, 0.05, 0.10, 0.20]
# dsubDM steps
dsubDMs   = [11.10, 20.40, 40.80, 81.60]
# downsample factors
downsamps = [1, 2, 4, 8]
# number of calls per set of subbands
subcalls  = [10, 4, 4, 2]
# The low DM for each set of DMs 
startDMs  = [0.0, 111.0, 192.6, 355.8]
# DMs/call
numDMs = [370, 408, 408, 408]
# Number of subbands
nsub = 512
# The number of points in the least-downsampled time series
numout = 21780000
# The basename of the output files you want to use
basename = "guppi_57955_P86Y1380_0005"
# The name of the raw data file (or files if you use wildcards) to use
rawfiles = "/hyrule/data/users/wcfiore/fermi_searches/P86Y1380/57955/"+basename+"*.fits"
# The name of the maskfile to apply (if no mask, use None)
maskfile = "/hyrule/data/users/wcfiore/fermi_searches/P86Y1380/57955/"+basename+"_rfifind.mask"

# Loop over the DDplan plans
for dDM, dsubDM, downsamp, subcall, startDM, numDM in \
        zip(dDMs, dsubDMs, downsamps, subcalls, startDMs, numDMs):
    # Get our downsampling right
    subdownsamp = downsamp/2
    datdownsamp = 2
    if downsamp < 2: subdownsamp = datdownsamp = 1
    # Loop over the number of calls
    for ii in range(subcall):
        subDM = startDM + (ii+0.5)*dsubDM
        # First create the subbands
        if maskfile:
            myexecute("prepsubband -ncpus 12 -mask %s -sub -subdm %.2f -nsub %d -downsamp %d -o %s %s" %
                      (maskfile, subDM, nsub, subdownsamp, basename, rawfiles))
        else:
            myexecute("prepsubband -ncpus 12 -sub -subdm %.2f -nsub %d -downsamp %d -o %s %s" %
                      (subDM, nsub, subdownsamp, basename, rawfiles))
        # And now create the time series
        loDM = startDM + ii*dsubDM
        subnames = basename+"_DM%.2f.sub[0-9]*"%subDM
        myexecute("prepsubband -ncpus 12 -numout %d -lodm %.2f -dmstep %.2f -numdms %d -downsamp %d -o %s %s" %
                  (numout/downsamp, loDM, dDM, numDM, datdownsamp, basename, subnames))
