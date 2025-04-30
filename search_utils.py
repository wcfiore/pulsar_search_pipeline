import subprocess
import numpy as np

sdir = "/lorule/scratch/wcf0002/AGBT24B_393/scripts"


def my_cmd(cmd, message, run=True, log=False):
    # Execute command and print explanation text
    if type(message) == list:  # Print multiple lines of explanation text
        for line in message:
            print(line)
    else:
        print(message)
    print(f"> {cmd}")  # Print command
    if run:
        if log:
            log.write(f"{cmd}\n")
        subprocess.run(cmd, shell=True)  # Execute command
        print("Complete \n")


def get_nspec(filenames):
    subprocess.run(
        f"rm -rf readfile_temp.out; readfile {filenames[0]} > readfile_temp.out",
        shell=True,
    )
    infile = open("readfile_temp.out", "r")
    for line in infile:
        line = line.strip("\n").strip(" ")
        if line.startswith("Spectra per file"):
            line = line.split("=")
            N1 = int(float(line[1]))
    infile.close()

    subprocess.run(
        f"rm -rf readfile_temp.out; readfile {filenames[len(filenames) - 1]} > readfile_temp.out",
        shell=True,
    )
    infile = open("readfile_temp.out", "r")
    for line in infile:
        line = line.strip("\n").strip(" ")
        if line.startswith("Spectra per file"):
            line = line.split("=")
            N2 = int(float(line[1]))
    infile.close()

    N = N1 * (len(filenames) - 1) + N2

    return N


def get_numout(N):
    gf = open(f"{sdir}/goodfactors.txt", "r")
    Nstring = str(N)
    N4 = int(Nstring[0:4])

    diff = 1e6
    bestnum = 0

    for line in gf:
        number = int(line[0:4])
        tempdiff = np.abs(number - N4)
        if (tempdiff < diff) and (number <= N4):
            diff = tempdiff
            bestnum = number

    bestnum = str(bestnum)
    for i in range(0, len(Nstring) - 4):
        bestnum = bestnum + "0"

    return int(bestnum)

