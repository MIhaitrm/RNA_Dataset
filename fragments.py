#!/usr/bin/env python

from cluster import hlabs
import sys
import glob
import os
import pandas as pd
from read_xyzr import read_xyzr
import numpy as np
import shutil

path = "xyzr_files"
atoms = glob.glob(os.path.join(path, "*.xyzr"))
print(atoms)

data = []
for a in atoms:
	a = read_xyzr(a)
	a = pd.DataFrame(a)
	data.append(a)

files = []
for i, j in zip(data, hlabs):
	j = pd.Series(j)
	f = pd.concat([i, j], axis=1)
	# f.columns = [['pos_x', 'pos_y', 'pos_z', 'radius', 'labels']]
	files.append(f)

fragments = []
for file in files:
	fragment = file.groupby(0)	
	fragments.append(fragment)

groups = []
for fragment in fragments:
	for n, g in fragment:
		groups.append(g)		

for index, g in enumerate(groups):
	g.to_csv("file" + str(index) + ".pdb", sep='\t', index=False)

directory_name = "temp_fragments"
try:
    os.mkdir(directory_name)
    print(f"Directory '{directory_name}' created successfully.")
except FileExistsError:
    print(f"Directory '{directory_name}' already exists.")
except PermissionError:
    print(f"Permission denied: Unable to create '{directory_name}'.")
except Exception as e:
    print(f"An error occurred: {e}")

destination = './temp_fragments'

for c in glob.glob("*.pdb"):
    shutil.copy(c, destination)

for name in glob.glob("*.pdb"):
    os.remove(name)
