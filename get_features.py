#!/usr/bin/env python

from read_data_from_surface import read_data_from_surface
import glob
import os
import torch
import numpy as np

path = "ply_files"

files = glob.glob(os.path.join(path, "*.ply"))
for i in files:
	print("Ply files:", i)

features = []
for f in files:
	input_feat, rho, theta, mask, neigh_indices, copy = read_data_from_surface(f)
	feature = np.concatenate([input_feat, rho, theta], axis=1)	
	features.append(feature)

for feat in features:
	print(feat.shape)