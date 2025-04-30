import os, sys

jobfile = sys.argv[1]
os.system('grep ^nimrod %s > nodelist.txt' % jobfile)
