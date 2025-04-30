~~ Steps to run a pulsar search (this is an evolving document) ~~
(Last updated: 2018 Nov 12)

1) Run search_setup.py

python search_setup.py -s <sourcename> -d <datadir> -r <0 or 1>

You don't need to input options if the defaults are what you want.

Defaults are:
  - source name is taken from data files
  - datadir is '.'
  - '-r 1', meaning commands will be run
  - If you just want to print out the commands, but not run them, then use "-r 0"

A file called baryv.txt will be output, containing the barycentric velocity
for accelsearch.  The other output file is a log containing all the commands
that were run.  ** Need to write script to gather all needed info from these
files and put into the .sh file that gets submitted to the cluster. **

2) Make .birds file

3) Run DDplan.py to make a dedispersion plan.

4) Make .sh file to run mpiprepsubband.  Remember to change numout and other
inputs in .sh file before submitting the job.  Numout will have been given
by search_setup.py. The baryv for accelsearch is in baryv.txt.  Currently I
am using zmax=4, 50, and 200 for accelsearch, but you can change this (this
is set in full_analysis_nimrod2_zmax4_50_200.py).

5) Make singlepulse and zmax directories and move files to appropriate directories:

mkdir singlepulse
mv *.singlepulse singlepulse

mkdir zmax4 zmax50 zmax200    # or whatever zmax values you used
Move _ACCEL_* files to zmax*

Make symbolic links to *.inf in zmax*
Copy ACCEL_sift.py to each zmax* directory and edit for your particular search

6) Run ACCEL_sift.py in zmax*.  E.g., for zmax=4:

cd zmax4
python ACCEL_sift.py > zmax4.sifted


~~ End here for now. ~~

~~ I've written more scripts that are used after the dedispersion and
acceleration searches have been done.  Still need to review them before
describing them in detail here.  (I've pieced some info together below but
haven't checked it over yet.) ~~

Note to self: For do.foldcands, might want to use 5 instead of 6 sigma
because of some candidates that are below 6 sigma

In main dir:
Run write_nodelist.py

Copy gotocand_newnimrod.py, run_gotocand.py, nodelist.txt into zmax*

ssh-add ~/.ssh/id_dsa

python run_gotocand.py
 - There is some issue where showcol is not recognized when running from a
python script, but when I copy-paste the command, then showcol is recognized
and gotocand_newnimrod.py will run.  So for now, just copy-paste the command
that is output from the python script, and run gotocand_newnimrod.py on the
command line.

Make do.foldcands.zmax?.snr?.?.sh; edit as needed for the particular search
Run fold_snrcut.py
Run do.foldcands.zmax?.snr?.?.sh

(Note:  Used snr=6.0 for P86Y0740, but dropped to 5.0 for P86Y1452; will
probably stick with 5.0 just to avoid having to redo things.)

Once rawfolds are ready:
- Copy zmax*/*rawfold*png* to laptop and then to google drive in folders like
those for P86Y0740 and P86Y1452.
- Choose good candidates, put into GoodCands
- Copy .dat files corresponding to GoodCands from nimrod?? to working dir
- Refold or search for them in other pointing(s) to confirm or deny
pulsar-ness
- If a cand is found to not be a pulsar, move from GoodCands back to zmax*
folder on google drive.

To make singlepulse plot:
Make sure you have all .inf files copied into singlepulse directory.
 >> single_pulse_search.py *.singlepulse
