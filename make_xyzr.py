#!/usr/bin/env python

import pandas as pd
import glob
import os
import shutil

def read_xyzr(file):
	data = pd.read_csv(file, sep='\t', header=None, index_col=None)
	# data = data[0].str.split(n=-1, expand=True)

	data.columns = [['pos_x', 'pos_y', 'pos_z', 'radius', 'labels']]
	xyz_file = data.sort_index(axis=1).drop(['labels'], axis=1)
	return xyz_file


# read_xyzr('file0.pdb')
# file = read_xyzr('xyzr_files/1asy.xyzr')
# print(file)

# files = glob.glob("*.pdb")
files = glob.glob(os.path.join("temp_fragments", "*.pdb"))
print(files)

# def make_xyzr(file):
# 	data = pd.read_csv(file, sep='\t', header=None)
# 	# data = data[0].str.split(n=-1, expand=True)
# 	return data

xyzr_files = []
for f in files:
	xyz_files = read_xyzr(f)
	xyzr_files.append(xyz_files)

# print(xyzr_files)

for idx, x in enumerate(xyzr_files):
	x.to_csv("fragment"+str(idx)+".xyzr", sep='\t', index=None)

directory_name = "fragments"
try:
    os.mkdir(directory_name)
    print(f"Directory '{directory_name}' created successfully.")
except FileExistsError:
    print(f"Directory '{directory_name}' already exists.")
except PermissionError:
    print(f"Permission denied: Unable to create '{directory_name}'.")
except Exception as e:
    print(f"An error occurred: {e}")

destination = './fragments'

for c in glob.glob("*.xyzr"):
    shutil.copy(c, destination)

# for name in glob.glob("*.xyzr"):
#     os.remove(name)