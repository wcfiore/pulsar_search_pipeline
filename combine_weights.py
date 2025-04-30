import numpy as np
from matplotlib import pyplot as plt
import glob

weights = np.zeros(2048)
infiles = glob.glob("*.weights")
for filenm in infiles:
    weights += np.loadtxt(filenm, usecols=[1], unpack=1)
avgwgt = weights / len(infiles)

# explicitly set end channels to 0
avgwgt[0] = 0.0
avgwgt[-1] = 0.0
threshwgt = (avgwgt > 0.8).astype(np.int)

# set neighboring bad channels to zero also
bad = np.where(threshwgt==0)[0][1:-1]  # ignore ends since we know they are bad
threshwgt[bad+1] = 0
threshwgt[bad-1] = 0

#plt.plot(threshwgt, 'x')
#plt.show()

outfile = open("guppi_weights.txt", "w")
for ii, wgt in enumerate(threshwgt):
    outfile.write("%d  %d\n" % (ii, wgt))
outfile.close()

