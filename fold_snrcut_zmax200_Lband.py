import os, sys
import numpy as np
import glob as glob

snrcut = 4.0
zmax = 200

mydir = os.getcwd()
#print(mydir)
foldscript = 'do.foldcands.snr%s.sh' % str(snrcut)
#rfimask = glob.glob('%s/*rfifind.mask' % mydir)[0]
#print(rfimask)

ignorechan = np.loadtxt('%s/ignorechan.txt' % mydir,delimiter=None,dtype=str,usecols=[0])[0] 

#if not os.path.isfile(foldscript):
#    print('%s does not exist!' % foldscript)
#    sys.exit()

#basename = rfimask.strip('_rfifind.mask').split('/')[-1]
#print(basename)

datafiles=sorted(glob.glob('*.fits'))
#print(datafiles)

datapath = mydir
#print(datapath)

basename = datafiles[0].strip('.fits')[:-5].split('/')[-1]

inffile_path = '/hyrule/results/wcfiore/fermi_searches/%s/%s' % (mydir.split('/')[-2], mydir.split('/')[-1])
inffile_basename = glob.glob('%s/*.inf' % inffile_path)[0].split('/')[-1].split('_DM')[0]

candsdir = '%s/cands_%s' % (inffile_path, zmax)
resultspath = '/hyrule/results/wcfiore/working'
#####

output = ""
output += '#!/bin/bash\n\n'
output += 'datapath=%s\n' % datapath
#output += 'rfipath=%s\n' % mydir
output += 'resultspath=%s\n' % resultspath
output += 'datafiles=%s_*.fits\n' % basename
#output += 'maskfile=%s\n' % rfimask.split('/')[-1]
output += 'ignorechan=%s\n' % ignorechan
output += 'basename=%s\n' % inffile_basename
output += 'outfilebase=%s\n' % inffile_basename[:-5]
output += 'inffilepath=%s\n' % inffile_path
output += 'zmax=%s\n\n' % zmax
output += 'fold () {\n\n'
output += '    candnum=$1\n'
output += '    DM=$2\n\n'
output += '    prepfold -noxwin -accelcand $1 -accelfile ${inffilepath}/${basename}_DM$2_ACCEL_${zmax}.cand -dm $2 -ignorechan ${ignorechan} ${datapath}/${datafiles} -o ${resultspath}/${outfilebase}_raw_DM$2\n\n'
output += '}\n\n'

#print(output)

#sys.exit()
os.chdir(candsdir)

if os.path.isfile(foldscript):
    print('%s already exists. Please remove it before rerunning.' % foldscript)
    sys.exit()

bestprofs = sorted(glob.glob('*.bestprof'))

for bp in bestprofs:
    bpsplit = bp.strip('.pfd.bestprof').split('_')
    accelcandnum = bpsplit[-1]
    for ii in bpsplit:
        if ii.startswith('DM'):
            dm = ii.strip('DM')
    with open(bp, 'r') as FILE:
        lines = FILE.readlines()
    FILE.close()
    for line in lines:
        if line.startswith('# Prob(Noise)'):
            snr = float(line.split('~')[-1].split(' ')[0])
    #print(bp, accelcandnum, dm, snr)
    if snr >= snrcut:
        output += 'fold %s %s #snr=%.2f\n' % (accelcandnum, dm, snr)

#prepfold_command = "prepfold -noxwin -ncpus 11 -accelcand %s -accelfile %s/%s_DM%s_ACCEL_%s.cand -dm %s -mask %s/%s %s/%s -o %s/%s_rawfold_DM%s" % (accelcandnum, inffile_path, inffile_basename, dm, zmax, dm, mydir, rfimask.split('/')[-1], datapath, basename + '_*.fits', resultspath, inffile_basename, dm)
#print(prepfold_command)

with open(foldscript, 'a') as FILE:
    FILE.write(output)
FILE.close()

os.system('chmod u+x %s' % foldscript)

print('Now, run this command from the directory where the original folded candidates are, making sure the .sh file is in the same directory:')
print('sbatch -J fold<pointing name> %s' % foldscript)
print('After that finishes, move all the resulting pfd files to the cands_NNN directory from the working directory.')
print('You can view all prepfold plots by using the following command from the same directory:')
print('gvall *rawfold*.ps')
