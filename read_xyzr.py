#!/usr/bin/env python

import pandas as pd
from extract_pdb import pdb_files
import glob
import os
import shutil

def read_xyzr(file):
	data = pd.read_csv(file, sep='\t', header=None)
	data = data[0].str.split(n=-1, expand=True)
	data.columns = [['pos_x', 'pos_y', 'pos_z', 'radius']]
	# xyz_file = data.drop(['radius'], axis=1)
	# return xyz_file
	return data

path = './xyzr_files'
files = glob.glob(os.path.join(path, "*.xyzr"))


names = [x + '.xyz' for x in pdb_files]

xyz_files = []
for f in files:
	xyz_file = read_xyzr(f)
	xyz_files.append(xyz_file)

print(xyz_files)