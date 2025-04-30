import subprocess
import glob
import argparse
from search_utils import *


try:
    source_name = glob.glob("vegas_?????_?????_*_????_0001.fits")[0].split("_")[3]
except IndexError:
    source_name = " "

parser = argparse.ArgumentParser(
    description="Print or run pulsar searching commands for a given set of files."
)
parser.add_argument(
    "-s",
    "--srcname",
    type=str,
    help="Name of source, in fits filenames",
    default=source_name,
)
parser.add_argument(
    "-d", "--datadir", type=str, help="Directory containing data files", default="."
)
parser.add_argument(
    "-p",
    "--print",
    action="store_true",
    help="Use if you want to print but not run the commands",
)
parser.add_argument(
    "-t",
    "--rfifindtime",
    type=float,
    help="Value to give rfifind's --time option",
    default=1.0,
)
parser.add_argument(
    "-J",
    "--jobname",
    type=str,
    help="Addition to jobnames",
    default=""
)

args = parser.parse_args()
srcname = args.srcname
datadir = args.datadir
rfifindtime = args.rfifindtime
jobname = args.jobname
run = not args.print

if jobname != "":
    jobname = f"_{jobname}"

datafiles = sorted(
    glob.glob(datadir + f"/vegas_?????_?????_{srcname}_????_0001.fits")
)  # Prevents the inclusion of any previously-made vegas*subs*fits files.
Nbasefiles = len(datafiles)
if run:
    log = open("setup_search_log.txt", "a")

for i in range(Nbasefiles):
    basename = datafiles[i][:-10].split("/")[-1]

    exp_rfifind = "Run rfifind"
    cmd_rfifind = f'sbatch -J setup_search_rfifind{jobname} -W -o setup_search_rfifind.out --wrap="rfifind -time {rfifindtime} -o {basename} {basename}_*.fits"'

    # Find numout
    all_datafiles = sorted(glob.glob(f"{basename}_????.fits"))
    Nfiles = len(all_datafiles)
    nspec = get_nspec(all_datafiles)
    numout = get_numout(nspec)
    my_cmd(
        "rm readfile_temp.out",
        f"Processing {basename}, with {Nfiles} total data files: numout = {numout}",
    )

    exp_prepdata_topo = "Run prepdata -nobary -dm 0.0"
    cmd_prepdata_topo = f'sbatch -J setup_search_prepdata_topo{jobname} -W -o setup_search_prepdata_topo.out --wrap="prepdata -numout {numout} -nobary -dm 0.0 -mask {basename}_rfifind.mask -o {basename}_DM0.0_topo {basename}_*.fits"'

    exp_realfft = "Run realfft on topocentric, DM=0 time series"
    cmd_realfft = f'sbatch -J setup_search_realfft{jobname} -W -o setup_search_realfft.out --wrap="realfft {basename}_DM0.0_topo.dat"'

    exp_accelsearch = "Run accelsearch to get info for .birds file"
    cmd_accelsearch = f'sbatch -J setup_search_accelsearch{jobname} -W -o setup_search_accelsearch.out --wrap="accelsearch -zmax 0 {basename}_DM0.0_topo.fft"'

    exp_prepdata_bary = (
        "Run prepdata with barycentering to get barycentric velocity (baryv)"
    )
    cmd_prepdata_bary = f'sbatch -J setup_search_prepdata_bary{jobname} -W -o setup_search_prepdata_bary.out --wrap="prepdata -numout 8 -dm 0.0 -o test {basename}_*.fits > baryv.txt"'

    # Print the commands and run if --print wasn't used
    my_cmd(cmd_rfifind, exp_rfifind, run=run, log=log)

    my_cmd(cmd_prepdata_topo, exp_prepdata_topo, run=run, log=log)

    my_cmd(cmd_realfft, exp_realfft, run=run, log=log)

    my_cmd(cmd_accelsearch, exp_accelsearch, run=run, log=log)

    my_cmd(cmd_prepdata_bary, exp_prepdata_bary, run=run, log=log)

    my_cmd("rm test.dat test.inf", "")

print(
    "\n*** Next, make your .birds file, edit your .sh file, and submit the .sh file to the cluster. ***\n"
)

if run:
    log.close()
