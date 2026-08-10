#!/usr/bin/env python

from subprocess import Popen, PIPE
import msms
from xyzr import compute_xyz
from read_msms import read_msms
import os
import random
import glob
import subprocess
from extract_pdb import pdb_files


def computeMSMS(xyzr_file,  protonate=True):
    file_base = xyzr_file
    #print(i)
    out_xyzr = file_base
    # if protonate:        
    #     compute_xyz(pdb_file, out_xyzr)
    # else:
    #     print("Error - pdb2xyzrn is deprecated.")
    #     sys.exit(1)

    FNULL = open(os.devnull, 'w')
    args = ['msms', "-density", "3.0", "-hdensity", "3.0", "-probe",\
    			"1.5", "-if",out_xyzr,"-of", file_base, "-af", file_base]
    p2 = Popen(args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p2.communicate()
    vertices, faces, normals, names = read_msms(file_base)
    return vertices, faces, normals, names


path = "fragments"
files = glob.glob(os.path.join(path, "*.xyzr"))
for f in files:
    computeMSMS(f, protonate=True)

# for f in glob.glob(os.path.join(path, "*")):
#     print(f)
#     if f.endswith(".area"):
#         os.remove(f)
#     elif f.endswith(".vert"):
#         os.remove(f)
#     elif f.endswith(".face"):
#         os.remove(f)
#     print(f"Deleted: {f}")