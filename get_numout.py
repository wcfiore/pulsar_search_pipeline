import os
import sys
import glob as glob
import numpy as np
from optparse import OptionParser
from search_utils import *


## User-specified values ##    
parser = OptionParser()
parser.add_option("-s", "--srcname", dest="srcname", type="string", help="Name of source, in guppi filenames")
parser.add_option("-d", "--datadir", dest="datadir", type="string", help="Directory containing data files", default=".")

(options, args) = parser.parse_args()
srcname=options.srcname
datadir=options.datadir
    
## This will not need to be changed unless you have non-standard or non-GUPPI file names ##
datafiles = sorted(glob.glob(datadir+'/guppi_?????_'+srcname+'_????_0001.fits'))  # Prevents the inclusion of any previously-made guppi*subs*fits files.
print('Scans: ', datafiles)
    
for i in range(0,len(datafiles)):
    
    basename = datafiles[i]
    basename=basename[:-10].split('/')[-1]
    all_datafiles = glob.glob(basename+'_????.fits')
    nspec = get_nspec(all_datafiles)
    numout = get_numout(nspec)

    print('\n%s, with %d total data files: numout = %s\n' % (basename, len(all_datafiles), numout))

    print('Prepdata commands:\n')
    print('   prepdata -numout %s -nobary -dm 0.0 -mask %s_rfifind.mask -o %s_DM0.0_topo %s_*.fits\n' % (numout, basename, basename, basename))
    print('   prepdata -numout %s -dm 0.0 -mask %s_rfifind.mask -o %s_DM0.0_bary %s_DM0.0_topo.dat\n' % (numout, basename, basename, basename))

os.system('rm readfile_temp.out')
