import os
import sys
import glob as glob
import numpy as np
from optparse import OptionParser
from search_utils import *

try:
    source_name = glob.glob('guppi_*_*_????_0001.fits')[0].split('_')[2]
except IndexError:
    source_name = ' '

parser = OptionParser()
parser.add_option("-s", "--srcname", dest="srcname", type="string", help="Name of source, in guppi filenames", default=source_name)
parser.add_option("-d", "--datadir", dest="datadir", type="string", help="Directory containing data files", default=".")
parser.add_option("-r", "--run", dest="run", type="int", help="If you do not want to print but not run the commands, use -r 0", default=1)
#parser.add_option("-i", "--ignorechan", dest="ignorechan", type="string", help="string of frequency channels to zap manually with -ignorechan", default="")

(options, args) = parser.parse_args()
srcname=options.srcname
datadir=options.datadir
run=options.run
#ignorechan=options.ignorechan


datafiles = sorted(glob.glob(datadir+'/guppi_?????_'+srcname+'_????_0001.fits'))  # Prevents the inclusion of any previously-made guppi*subs*fits files.
if run==1:
    log = open('setup_search_log.txt','a')

for i in range(0,len(datafiles)):
    basename = datafiles[i]
    basename=basename[:-10].split('/')[-1]

    # Find numout
    all_datafiles = sorted(glob.glob(basename+'_????.fits'))
#    cmds_rfifind = []
#    cmds_stats = []
#    for f in all_datafiles:
#        cmd_rfifind = 'rfifind -time 1.0 -o %s %s' % (f[:-5], f)
#        cmds_rfifind.append(cmd_rfifind)
#        cmd_stats = 'rfifind_stats.py %s_rfifind.stats' % f[:-5]
#        cmds_stats.append(cmd_stats)
#    # Combine weights from all datafiles
#    cmd_weights = 'python combine_weights.py *.weights'
#    # Use weights_to_ignorechan.py to get list of each channel to zap with -ignorechan
#    cmd_ignorechan = 'weights_to_ignorechan.py guppi_weights.txt > ignorechan.txt'
    nspec = get_nspec(all_datafiles)
    numout = get_numout(nspec)
    print('\nProcessing %s, with %d total data files: numout = %s\n' % (basename, len(all_datafiles), numout))
    os.system('rm readfile_temp.out')
    ignorechan = np.loadtxt('ignorechan.txt',delimiter=None,dtype=str,usecols=[0])[0]
    # Run prepdata -nobary -dm 0.0
#    cmd_prepdata = 'prepdata -numout %s -nobary -dm 0.0 -ignorechan %s -o %s_DM0.0_topo %s_*.fits' % (numout, ignorechan, basename, basename)
    cmd_prepdata = 'prepdata -numout %s -nobary -dm 0.0 -ignorechan %s -o %s_DM0.0_topo %s_*.fits' % (numout, ignorechan, basename, basename)
    # Run realfft on topocentric, DM=0 time series
    cmd_realfft='realfft %s_DM0.0_topo.dat' % (basename)

    # Run accelsearch to get info for .birds file
    cmd_accelsearch = 'accelsearch -zmax 0 %s_DM0.0_topo.fft' % basename

    # Run prepdata with barycentering to get barycentric velocity (baryv)
    cmd_prepdata_bary = 'prepdata -numout 8 -dm 0.0 -o test %s_*.fits > baryv.txt; rm test.dat test.inf' % (basename)
    
    # Print out commands that will be run (in case user wants to run them manually)
    print('The commands that will be run are:')
#    for cmd_rfifind, cmd_stats in zip(cmds_rfifind, cmds_stats):
#        print('  '+cmd_rfifind)
#        print('  '+cmd_stats)
#    print('  '+cmd_weights)
#    print('  '+cmd_ignorechan)
    print('  '+cmd_prepdata)
    print('  '+cmd_realfft)
    print('  '+cmd_accelsearch)
    print('  '+cmd_prepdata_bary)
    
    # Run the commands
    if run==1:
        print('\n\nNow running the following commands:\n')
        
#        for cmd_rfifind, cmd_stats in zip(cmds_rfifind, cmds_stats):
#            print('  '+cmd_rfifind)
#            log.write(cmd_rfifind+'\n')
#            os.system(cmd_rfifind)
#
#            print('  '+cmd_stats)
#            log.write(cmd_stats+'\n')
#            os.system(cmd_stats)
#
#        print('  '+cmd_weights)
#        log.write(cmd_weights+'\n')
#        os.system(cmd_weights)
#
#        print('  '+cmd_ignorechan)
#        log.write(cmd_ignorechan+'\n')
#       os.system(cmd_ignorechan)
#
#        cmd_prepdata = 'prepdata -numout %s -nobary -dm 0.0 -ignorechan %s -o %s_DM0.0_topo %s_*.fits' % (numout, ignorechan, basename, basename)
        
        print(cmd_prepdata+'\n')
        log.write(cmd_prepdata+'\n')
        os.system(cmd_prepdata)
    
        print(cmd_realfft+'\n')
        log.write(cmd_realfft+'\n')
        os.system(cmd_realfft)
    
        print(cmd_accelsearch+'\n')
        log.write(cmd_accelsearch+'\n')
        os.system(cmd_accelsearch)
        
        print(cmd_prepdata_bary+'\n')
        log.write(cmd_prepdata_bary+'\n')
        os.system(cmd_prepdata_bary)
    
    print('\n*** Next, make your .birds file, edit your .sh file, and submit the .sh file to the cluster. ***\n')
    
if run==1:
    log.close()
