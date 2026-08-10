#!/usr/bin/env python

import torch
from torch_geometric.data import Data
import pandas as pd
import numpy as np
import glob
import os
import shutil

# edges = pd.read_csv('edge.tsv', sep='\t')
# edges = np.array(edges)

# vertices = pd.read_csv('vert.tsv', sep='\t')
# vertices = np.array(vertices)

path_edges = "edge_dir"
files_edges = glob.glob(os.path.join(path_edges, "*.tsv"))

path_vertices = "feature_files"
files_vertices = glob.glob(os.path.join(path_vertices, "*.npy"))


# for f in files_edges:
# 	edge = pd.read_csv(f, sep="\t", header=None)
# 	print(edge)
edge_indices = []
for file_e in files_edges:
	f = pd.read_csv(file_e, sep="\t", header=None)
	edge_idx = np.array(f)
	edge_index = torch.tensor(edge_idx)
	edge_indices.append(edge_index)

vertices = []
for file_vert in files_vertices:
	# vf = pd.read_csv(file_vert, sep="\t", header=None)
	vf = np.load(file_vert)
	# vert_idx = np.array(vf)
	vert = torch.tensor(vf)
	vertices.append(vert)

xs = []
for e in vertices:
	# x = torch.tensor(e, dtype=torch.float)
	x = e.detach().clone().requires_grad_(True)
	xs.append(x)

datas = []
for x, y in zip(xs, edge_indices):
	data = Data(x=x, edge_index=y)
	datas.append(data)

for idx, d in enumerate(datas):
	torch.save(d, f"file{idx}.npy")


directory_name = "npy_files"
try:
    os.mkdir(directory_name)
    print(f"Directory '{directory_name}' created successfully.")
except FileExistsError:
    print(f"Directory '{directory_name}' already exists.")
except PermissionError:
    print(f"Permission denied: Unable to create '{directory_name}'.")
except Exception as e:
    print(f"An error occurred: {e}")

destination = './npy_files'

for c in glob.glob("*.npy"):
    shutil.copy(c, destination)

for name in glob.glob("*.npy"):
    os.remove(name)


pt_files = glob.glob(os.path.join("npy_files", "*.npy"))

for p in pt_files:
	load = torch.load(p, weights_only=False)
	# print(load['x'])
	print(load.num_node_features)