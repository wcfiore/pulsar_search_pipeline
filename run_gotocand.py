import os, sys
import glob as glob

basename = sys.argv[1]

siftfile = glob.glob('*.sifted')
if len(siftfile) > 1:
    print('There is more than one .sifted file.  Make a single .sifted file before running gotocand.')
    sys.exit()
elif len(siftfile) == 0:
    print('There is no .sifted file.  Make a .sifted file before running gotocand.')
else:
    siftfile = siftfile[0]
    print('grep ^%s* %s | showcol 1 | xargs -n 1 python gotocand_newnimrod.py' % (basename, siftfile))
    os.system('grep ^%s* %s | showcol 1 | xargs -n 1 python gotocand_newnimrod.py' % (basename, siftfile))
