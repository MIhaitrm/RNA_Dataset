#!/usr/bin/env python

import glob
import os
import numpy as np
import pickle
from prody import *
import subprocess
from subprocess import Popen, PIPE
import shutil
from protonated import *
from extract_pdb import pdb_files


ids = pdb_files

def compute_xyz(in_file, out_file):
	args = ["pdb_to_xyzr", in_file, out_file]
	p2 = Popen(args, stdout=PIPE, stderr=PIPE)
	stdout, stderr = p2.communicate()
	outfile = open(out_file, "w")
	outfile.write(stdout.decode('utf-8'))
	outfile.close()

path = "protonated"
files = glob.glob(os.path.join(path, "*.pdb"))
print(files)

prefix = []
for i in files:
	if i.startswith("protonated/"):
		i = i[-9:]
		prefix.append(i)


suffix = []	
for j in prefix:
	if j.endswith("H.pdb"):
		j = j[:-5]
		suffix.append(j)

xyzr_files = []
for x in suffix:
	xyzr_file = x + ".xyzr"
	xyzr_files.append(xyzr_file)
	print(xyzr_files)

for f, i in zip(files, xyzr_files):
	compute_xyz(f, i)

directory_name = "xyzr_files"
try:
    os.mkdir(directory_name)
    print(f"Directory '{directory_name}' created successfully.")
except FileExistsError:
    print(f"Directory '{directory_name}' already exists.")
except PermissionError:
    print(f"Permission denied: Unable to create '{directory_name}'.")
except Exception as e:
    print(f"An error occurred: {e}")

destination = './xyzr_files'

for c in xyzr_files:
	shutil.copy(c, destination)

for filename in glob.glob("*.xyzr"):
    os.remove(filename)

